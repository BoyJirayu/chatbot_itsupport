import numpy as np
import pandas as pd
import re
import nltk
from sklearn.datasets import load_files
nltk.download('stopwords')
# import dill
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
import json 
from etl import cleanText,tokenization2
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,precision_score,recall_score
## Replace path of Sample Data
# csv = 'C:\\compare algorithm\\test3.csv'
csv = 'C:\\compare algorithm\\TestTest.csv'
## ##
my_df = pd.read_csv(csv, nrows=300)
texts = my_df['Question']
labels = my_df['Type']

newLabel = []
for label in labels:
  if label=="ทักทาย" or label=='"ทักทาย"':
    newLabel.append(1)
  elif label=="เสร็จสิ้นและขอบคุณ" or label=='"เสร็จสิ้นและขอบคุณ"':
    newLabel.append(2)
  elif label=="ข้อความทั่วไป" or label=='"ข้อความทั่วไป"':
    newLabel.append(3)
  elif label=="ขอใช้งาน Zoom Conference" or label=='"ขอใช้งาน Zoom Conference"':
    newLabel.append(4)
  elif label=="สอบถามเกี่ยวกับ Zoom" or label=='"สอบถามเกี่ยวกับ Zoom"':
    newLabel.append(5)
  elif label=="ขอไฟล์บันทึกการประชุม Zoom" or label=='"ขอไฟล์บันทึกการประชุม Zoom"':
    newLabel.append(6)
  elif label=="ขอใช้งานอุปกรณ์ conference" or label=='"ขอใช้งานอุปกรณ์ conference"':
    newLabel.append(7)
  elif label=="นำอุปกรณ์มาติดต่อเจ้าหน้าที่" or label=='"นำอุปกรณ์มาติดต่อเจ้าหน้าที่"':
    newLabel.append(8)
  elif label=="สอบถามทั่วไป" or label=='"สอบถามทั่วไป"':
    newLabel.append(9)
  elif label=="สอบถามความต้องการใช้งานระบบสารบรรณ" or label=='"สอบถามความต้องการใช้งานระบบสารบรรณ"':
    newLabel.append(10)
  elif label=="สอบถามเบอร์ติดต่อผู้ตรวจสอบสิทธิ์ ERP" or label=='"สอบถามเบอร์ติดต่อผู้ตรวจสอบสิทธิ์ ERP"':
    newLabel.append(11)
  elif label=="ปัญหาการเชื่อมต่ออินเทอร์เน็ต" or label=='"ปัญหาการเชื่อมต่ออินเทอร์เน็ต"':
    newLabel.append(12)
  elif label=="ปัญหาการใช้งานอินเทอร์เน็ต" or label=='"ปัญหาการใช้งานอินเทอร์เน็ต"':
    newLabel.append(13)
  elif label=="ปัญหาเครื่องปริ้น" or label=='"ปัญหาเครื่องปริ้น"':
    newLabel.append(14)
  elif label=="ปัญหาทั่วไป (Onsite)" or label=='"ปัญหาทั่วไป (Onsite)"':
    newLabel.append(15)
  elif label=="ปัญหาเครื่องคอมพิวเตอร์" or label=='"ปัญหาเครื่องคอมพิวเตอร์"':
    newLabel.append(16)
  elif label=="ปัญหาการใช้งานคอมพิวเตอร์" or label=='"ปัญหาการใช้งานคอมพิวเตอร์"':
    newLabel.append(17)
  elif label=="ปัญหาการเข้าเว็ป" or label=='"ปัญหาการเข้าเว็ป"':
    newLabel.append(18)
  elif label=="ปัญหาเว็บจองห้องประชุม" or label=='"ปัญหาเว็บจองห้องประชุม"':
    newLabel.append(19)
  elif label=="ปัญหาอีเมล" or label=='"ปัญหาอีเมล"':
    newLabel.append(20)
  elif label=="ปัญหาการใช้งานระบบหนังสือเวียน" or label=='"ปัญหาการใช้งานระบบหนังสือเวียน"':
    newLabel.append(21)
  elif label=="ปัญหาการใช้งานระบบใบลา & สแกนนิ้ว" or label=='"ปัญหาการใช้งานระบบใบลา & สแกนนิ้ว"':
    newLabel.append(22)
  elif label=="ปัญหาการใช้งานระบบ VPN" or label=='"ปัญหาการใช้งานระบบ VPN"':
    newLabel.append(23)
  elif label=="ปัญหาการใช้งานระบบ E-Budget" or label=='"ปัญหาการใช้งานระบบ E-Budget"':
    newLabel.append(24)
  elif label=="ปัญหาการใช้งาน Drive กลาง" or label=='"ปัญหาการใช้งาน Drive กลาง"':
    newLabel.append(25)
  elif label=="ปัญหาโปรแกรม ERP" or label=='"ปัญหาโปรแกรม ERP"':
    newLabel.append(26)
  elif label=="ติดตั้งโปรแกรม" or label=='"ติดตั้งโปรแกรม"':
    newLabel.append(27)
  elif label=="ขอให้งานระบบสารบรรณ" or label=='"ขอให้งานระบบสารบรรณ"':
    newLabel.append(28)
  elif label=="Add & ติดตั้งเครื่องปริ้น" or label=='"Add & ติดตั้งเครื่องปริ้น"':
    newLabel.append(29)
  elif label=="ขอ Token Line Notify" or label=='"ขอ Token Line Notify"':
    newLabel.append(30)
  elif label=="เดินสาย LAN" or label=='"เดินสาย LAN"':
    newLabel.append(31)
  elif label=="ติดตั้ง VPN" or label=='"ติดตั้ง VPN"':
    newLabel.append(32)
  elif label=="ปัญหา VM และ Server" or label=='"ปัญหา VM และ Server"':
    newLabel.append(33)
  elif label=="ขอใช้บริการ Pocket WIFI" or label=='"ขอใช้บริการ Pocket WIFI"':
    newLabel.append(34)
  elif label=="ขอใช้บริการ Notebook" or label=='"ขอใช้บริการ Notebook"':
    newLabel.append(35)
  else:
    print(label)
    newLabel.append(0)

X= texts
Y= labels
# print(X)
# print(Y)
documents = []

for sen in range(0,len(X)):
  document = cleanText(X[sen])
  stemmer = PorterStemmer()
  document = tokenization2(document)
  document = [stemmer.stem(word) for word in document]
  documents.append(document)

from sklearn.feature_extraction.text import CountVectorizer
tokens_list_j = [','.join(tkn) for tkn in documents]
cvec = CountVectorizer(analyzer=lambda x:x.split(','))
c_feat = cvec.fit_transform(tokens_list_j).toarray()

def lamda_l(text1):
    return text1.split(',')
from sklearn.feature_extraction.text import TfidfVectorizer
tvec = TfidfVectorizer(analyzer=lamda_l)
t_feat = tvec.fit_transform(tokens_list_j).toarray()

## Create Feature Example Data
with open('feature.pkl', 'wb') as picklefile:
    pickle.dump(tvec,picklefile)

## Create Model 
X_train, X_test, y_train, y_test = train_test_split(t_feat, Y)
# classifier = RandomForestClassifier(n_estimators=70, random_state=1)
classifier = RandomForestClassifier()

classifier.fit(X_train, y_train)
with open('classifierRFC1.pkl', 'wb') as picklefile:
    pickle.dump(classifier,picklefile)


y_pred = classifier.predict(X_test)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(accuracy_score(y_test, y_pred))
print(precision_score(y_test, y_pred, average=None))
print(recall_score(y_test, y_pred, average=None))