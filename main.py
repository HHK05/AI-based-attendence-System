import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Initialize Firebase Admin SDK with the service account credentials
cred = credentials.Certificate("C:/Users/Harsh/OneDrive/Desktop/hackathin/DBMS project/serviceaccountkey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendencesystem005-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendencesystem005.appspot.com"
})

#storage_client = storage.bucket()
bucket=storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

background_path = "C:/Users/Harsh/OneDrive/Desktop/hackathin/DBMS project/Resources/background.png"
imgBackground = cv2.imread(background_path)
#importing images to list 
modepath="C:/Users/Harsh/OneDrive/Desktop/hackathin/DBMS project/Resources/Modes"
modepathlist=os.listdir(modepath)
imgmodelist=[]
for path in modepathlist:
    imgmodelist.append(cv2.imread(os.path.join(modepath,path)))
    #print(len(imgmodelist))
#print(modepathlist)

#load the encoding file
print("loading encoded file") 
file=open('encodeing.p','rb')
encodelistknownwithids=pickle.load(file)
file.close()
encodelistknown,student_ids=encodelistknownwithids
#print(student_ids)
print("loaded encoded file")

modeType=0
counter=0
id=-1
imgStudent=[]

while True:
    success, img = cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    FaceCurFrame=face_recognition.face_locations(imgS)
    encodecurframe=face_recognition.face_encodings(imgS,FaceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44+633,808:808+414] = imgmodelist[modeType]


    for encodeFace,faceLoc in zip(encodecurframe,FaceCurFrame):
        matches=face_recognition.compare_faces(encodelistknown,encodeFace)
        facedis=face_recognition.face_distance(encodelistknown,encodeFace)
        #print("Matches",matches)
        #print("facedis",facedis)

        matchIndex=np.argmin(facedis)
        #print("MatchIndex",matchIndex)
        if matches[matchIndex]:
            #print("known face detected")
            #print(student_ids[matchIndex])

            y1,x1,y2,x2=faceLoc
            y1,x1,y2,x2=y1*4,x2*4,y2*4,x1*4
            bbox=55+x1,162+y1,x2-x1,y2-y1
            imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0)
            id=student_ids[matchIndex]


            if counter==0:
                counter=1
                modeType=1

    if counter!=0:
        if counter==1:
            #get the data
            studentinfo=db.reference(f'Students/{id}').get()
            print(studentinfo)
            #get the image from the storage 
            '''blob = storage_client.blob(f'Images/{id}')
            if blob.exists():
                array = np.frombuffer(blob.download_as_string(), np.uint8)
            else:
                print("Blob does not exist.")'''

            blob=bucket.get_blob(f'https://console.firebase.google.com/project/faceattendencesystem005/storage/faceattendencesystem005.appspot.com/files/~2FImages/{id}.png')
            array=np.frombuffer(blob.download_as_string(),np.unit8)
            imgStudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

        cv2.putText(imgBackground,str(studentinfo['Total_attendence']), (861, 125),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),1)
        cv2.putText(imgBackground, str(studentinfo['Total_attendence']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(studentinfo['Major']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(studentinfo['Standing']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackground, str(studentinfo['Year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackground, str(studentinfo['Starting_year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

        (w, h), _ = cv2.getTextSize(studentinfo['Name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imgBackground, str(studentinfo['Name']), (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        imgBackground[175:175+216,909:909+216]=imgStudent
        counter+=1
            

    #cv2.imshow("webcam", img)
    cv2.imshow("Face Attendance", imgBackground)

    cv2.waitKey(1) 


