from firebase import firebase

url = 'https://line-itsupport-firebase-default-rtdb.firebaseio.com/'
messenger = firebase.FirebaseApplication(url)

engineer = {'id':1001,'name':'Uncle Engineer'}
engineer2 = {'id':1002,'name':'Lung Tu'}

result = messenger.put('/user','1',engineer)
result2 = messenger.put('/user','2',engineer2)

print("Engineer 1", result)
print("Engineer 2", result2)


# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# cred = credentials.Certificate('line-itsupport-firebase-firebase-adminsdk-fvrmd-69aedaa3b9.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# # # Write Data to Firebase
# # doc_ref = db.collection(u'users').document(u'Name')
# # doc_ref.set({
# #     u'first': u'Jirayu',
# #     u'last': u'Chaimeeboon',
# # })

# # # Read Data from Firebase
# # users_ref = db.collection(u'users')
# # docs = users_ref.stream()

# # for doc in docs:
# #     print(u'{} => {}'.format(doc.id, doc.to_dict()))