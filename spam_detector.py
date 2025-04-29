import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

nltk.download('stopwords')

class SpamDetector:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stopwords_set = set(stopwords.words('english'))
        self.vectorizer = CountVectorizer()
        self.model = RandomForestClassifier(n_jobs=-1)

    def preprocess_text(self, text):
        text = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
        text = [self.stemmer.stem(word) for word in text if word not in self.stopwords_set]
        return ' '.join(text)

    def train(self, data_path):
        data = pd.read_csv(data_path)
        data['text'] = data['text'].apply(lambda x: x.replace('\r\n', ' '))
        corpus = [self.preprocess_text(text) for text in data['text']]
        
        x = self.vectorizer.fit_transform(corpus).toarray()
        y = data['label_num']

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)

        print(f"Model Accuracy: {self.model.score(X_test, y_test) * 100:.2f}%")

    def predict(self, email_text):
        processed_text = self.preprocess_text(email_text)
        x_email = self.vectorizer.transform([processed_text])
        prediction = self.model.predict(x_email)
        return prediction[0]  # 0 for ham, 1 for spam
