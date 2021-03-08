import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('line-itsupport-firebase-firebase-adminsdk-fvrmd-69aedaa3b9.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# # Write Data to Firebase
# doc_ref = db.collection(u'users').document(u'Name')
# doc_ref.set({
#     u'first': u'Jirayu',
#     u'last': u'Chaimeeboon',
# })

# # Read Data from Firebase
# users_ref = db.collection(u'users')
# docs = users_ref.stream()

# for doc in docs:
#     print(u'{} => {}'.format(doc.id, doc.to_dict()))