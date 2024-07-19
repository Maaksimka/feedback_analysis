import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import time

def scroll_to_bottom(driver, pause_time):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def parse_wildberries(url):
    options = Options()
    options.headless = True
    options.add_argument(r'--user-data-dir=C:/Users/maxpa/AppData/Local/Google/Chrome/User Data')
    options.add_argument('--profile-directory=Default')
    options.add_argument('--log-level=3')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    scroll_pause_time = 1
    scroll_to_bottom(driver, scroll_pause_time)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn-base.comments__btn-all'))
        )
    except Exception as e:
        print(f"Ошибка при ожидании элемента: {e}")
        driver.quit()
        return None

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    button = soup.find('a', class_='btn-base comments__btn-all')
    
    if button:
        href = button.get('href')
        parsed_url = urlparse(href)
        query_params = parse_qs(parsed_url.query)
        imt_id = query_params.get('imtId', [None])[0]
        driver.quit()
        return imt_id
    else:
        print('Button not found')
        driver.quit()
        return None

def get_feedbacks(imtId):
    url = f'https://feedbacks2.wb.ru/feedbacks/v1/{imtId}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def parse_feedbacks(json_data):
    feedbacks = json_data.get('feedbacks', [])
    parsed_feedbacks = []

    for feedback in feedbacks:
        feedback_id = feedback.get('id')
        text = feedback.get('text')
        rating = feedback.get('productValuation')
        nmId = feedback.get('nmId')

        parsed_feedbacks.append({
            'nmId': nmId,
            'text': text,
            'rating': rating
        })
    
    return parsed_feedbacks

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_to_excel(data, filename):
    df = pd.DataFrame(data, columns=['nmId', 'text', 'rating'])
    df['mood'] = None
    df.to_excel(filename, index=False, engine='openpyxl')

def main(input_file, json_file, excel_file):
    feedbacks_all = []

    with open(input_file, 'r', encoding='utf-8') as file:
        urls = file.read().split(';')

    for url in urls:
        url = url.strip()
        if url:
            try:
                print(f'Обрабатываем URL: {url}')
                imtId = parse_wildberries(url)
                if imtId:
                    print(f'Получен imtId: {imtId}')
                    json_data = get_feedbacks(imtId)
                    if 'feedbacks' in json_data:
                        feedbacks = parse_feedbacks(json_data)
                        feedbacks_all.extend(feedbacks)
                    else:
                        print(f'Отзывы не найдены для imtId: {imtId}')
                
            except Exception as e:
                print(f'Ошибка обработки URL {url}: {e}')

    save_to_json(feedbacks_all, json_file)
    save_to_excel(feedbacks_all, excel_file)

if __name__ == '__main__':
    input_file = r"C:\Users\maxpa\Desktop\wb_urls.txt"
    json_file = 'feedbacks.json'
    excel_file = 'feedbacks.xlsx'
    main(input_file, json_file, excel_file)
