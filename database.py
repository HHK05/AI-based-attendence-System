import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("C:/Users/Harsh/OneDrive/Desktop/hackathin/DBMS project/serviceaccountkey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendencesystem005-default-rtdb.firebaseio.com/"
})
ref=db.reference('Students')
data={
    "321654":
    {
        "Name":"Harshil HK",
        "Major":"Information Science and Engineering",
        "Specialization":"Machine Learning",
        "Starting_year":2021,
        "Total_attendence":10,
        "Standing":"A+",
        "Year":4,
        "Last_attendence_time":"2022-12-11 00:54:34"
    },
    "852741":
    {
        "Name":"Emly Blunt",
        "Major":"Computer Science and Engineering",
        "Specialization":"AI",
        "Starting_year":2021,
        "Total_attendence":10,
        "Standing":"A+",
        "Year":5,
        "Last_attendence_time":"2022-12-12 00:55:56"
    },
    "963852":
    {
        "Name":"Elon Musk",
        "Major":"Automation industry with Space",
        "Specialization":"AIML",
        "Starting_year":2022,
        "Total_attendence":12,
        "Standing":"A++",
        "Year":6,
        "Last_attendence_time":"2022-12-14 00:12:44"
    }
}
for key,value in data.items():
    ref.child(key).set(value) 