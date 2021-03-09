from firebase import firebase

url = 'https://line-itsupport-firebase-default-rtdb.firebaseio.com/'
messenger = firebase.FirebaseApplication(url)

engineer = {'id':1001,'name':'Uncle Engineer'}
engineer2 = {'id':1002,'name':'Lung Tu'}

result = messenger.put('/user','1',engineer)
result2 = messenger.put('/user','2',engineer2)

print("Engineer 1", result)
print("Engineer 2", result2)