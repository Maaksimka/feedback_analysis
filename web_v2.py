import subprocess

# Установка необходимых библиотек из requirements.txt
subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import time

# Загрузка предварительно обученной модели и векторизатора
model = joblib.load("logistic_regression_model.joblib")
vectorizer = joblib.load("fidf_vectorizer.joblib")

st.title('Анализ тональности отзывов')

review_text = st.text_area("Введите текст отзыва:")
analyze_button = st.button('Анализировать тональность')

if analyze_button:
    if review_text:
        # Преобразование текста отзыва в признаки
        X_review = vectorizer.transform([review_text])

        # Предсказание тональности отзыва
        mood = model.predict(X_review)

        if mood[0] == 'positive':
            st.markdown('<div style="background-color: green; color: white; padding: 10px; border-radius: 5px;">Положительный отзыв</div>', unsafe_allow_html=True)
            time.sleep(0.5)
            st.empty()
            time.sleep(0.5)
        elif mood[0] == 'neutral':
       
            st.markdown('<div style="background-color: orange; color: white; padding: 10px; border-radius: 5px;">Нейтральный отзыв</div>', unsafe_allow_html=True)
            time.sleep(0.5)
            st.empty()
            time.sleep(0.5)
        else:
            st.markdown('<div style="background-color: red; color: white; padding: 10px; border-radius: 5px;">Негативный отзыв</div>', unsafe_allow_html=True)
            time.sleep(0.5)
            st.empty()
            time.sleep(0.5)
    else:
        st.error('Пожалуйста, введите текст отзыва для анализа')


st.markdown(
    """
    <style>
    body {
        background-image: url('file:///C:/Users/maxpa/Desktop/background.jpg');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

