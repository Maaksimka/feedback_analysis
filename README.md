Задача: анаиз тональности отзывов с маркетплейсов (wildberies).
Релевантных данных не было, поэтому мы парсили их и ручками делали разметку, затем пробовали разные подходы к анализу тональности (многоклассовой классификации: positive, neutral, negative), ну и в конце задеплоили обученную модельку на streamlit чтобы можно было поиграться и посмотреть она оценивает отзывы, вот ссылка:
https://feedback-sentiment-analyz.streamlit.app/

parser.py - парсер отзывов с wildberies по ссылке на товар.
requirements_parser.txt - зависимости для парсера.
feedback_final.csv - размеченные отзывы с wildberies (почтки 9к).
feedback_lema.csv - те же отзывы, но лематизированные (приведены к основе/леме).
logistic_regression_model.joblib - параметры для логистической регрессии.
tfidf_vectorizer.joblib - параметры для логистической регрессии.
nn.ipynb - нейросети для анализа тональности: полносвязные с one hot encoding и embeding, rnn, lstm, gru, cnn.
hebert_sentiment_analyz.ipynb - зафайютюненный transformer avichr/heBERT_sentiment_analysis.
twitter_sentiment_analyz.ipynb - зафайютюненный transformer cardiffnlp/twitter-xlm-roberta-base-sentiment.
web_v2.py - задэплоенный веб-сервис для анализа тональности на streamlit.
