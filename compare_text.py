from sklearn.metrics import pairwise
from nltk.stem import PorterStemmer
from etl import cleanText,tokenization2
import pickle
from use_model import lamda_l

def match_menu(def_msg,user_msg):
    d_msg = change_before_match(def_msg)
    u_msg = change_before_match(user_msg)
    result = pairwise.cosine_similarity(d_msg,u_msg,dense_output=True)
    print(result[0][0])
    if(result[0][0]>=0.55):
        return True
    else: return False
    
def change_before_match(meg):
    X= [meg]
    documents = []
    for sen in range(0,len(X)):
        document = X[sen]
        stemmer = PorterStemmer()

        # document = document.split()
        document = tokenization2(document,"attacut")
        document = [stemmer.stem(word) for word in document]
        documents.append(document)
        tokens_list_j = [','.join(tkn) for tkn in documents]
        with open('feature.pkl', 'rb') as handle:
            vectorizer = pickle.load(handle)
    return vectorizer.transform(tokens_list_j).toarray()