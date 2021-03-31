import numpy as np
import pandas as pd
import re
from etl import cleanText,tokenization2
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
feature_path = 'feature.pkl'
classifier_path = 'classifierRFC.pkl'
model=None
vectorizer=None
def comma(text1):
    return text1.split(',')

def myPredict(input_text):
    X= [input_text]
    documents = []
    for sen in range(0,len(X)):
        document = cleanText(X[sen])
        stemmer = PorterStemmer()

        # document = document.split()
        document = tokenization2(document,"attacut")
        document = [stemmer.stem(word) for word in document]
        # document = ' '.join(document)
        documents.append(document)

    # from sklearn.feature_extraction.text import CountVectorizer
    tokens_list_j = []
    tokens_list_j = [','.join(tkn) for tkn in documents]
    with open(classifier_path, 'rb') as handle:
        model = pickle.load(handle)
    with open(feature_path, 'rb') as handle:
        vectorizer = pickle.load(handle)

    XX = vectorizer.transform(tokens_list_j).toarray()
    # prediction = model.predict_proba(XX)
    prediction = model.predict(XX)
    print(prediction)
    return prediction[0]
    # return {"prediction":prediction[0],"text_token":documents[0]}
