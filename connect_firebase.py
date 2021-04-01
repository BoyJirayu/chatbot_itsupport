from firebase import firebase

url = 'https://line-itsupport-firebase-default-rtdb.firebaseio.com/'
messenger = firebase.FirebaseApplication(url)

def post_user_profile(uid,data,firebase_app,db_name):
    res = firebase_app.patch("/"+db_name+"/"+uid,data)
    return res

def post_user_session(uid,data,firebase_app,db_name):
    res = firebase_app.patch("/"+db_name+"/"+uid,data)
    return res

def put_user_session(uid,data,firebase_app,db_name):
    res = firebase_app.put("/"+db_name,uid,data)
    return res

def get(uid,firebase_app,db_name):
    res = firebase_app.get("/"+db_name,uid)
    return res

def put_vcs(uid,data,firebase_app,db_name):
    res = firebase_app.patch("/"+db_name+"/"+uid,data)
    return res

def get_vcs(uid,firebase_app,db_name):
    res = firebase_app.get("/"+db_name,uid)
    return res

def put_problem_for_emp(uid,data,firebase_app,db_name):
    res = firebase_app.patch("/"+db_name+"/"+uid,data)
    return res