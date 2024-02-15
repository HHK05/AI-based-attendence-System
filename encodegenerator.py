import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("C:/Users/Harsh/OneDrive/Desktop/hackathin/DBMS project/serviceaccountkey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendencesystem005-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendencesystem005.appspot.com"
})


#importing student images to list 
image_path="C:/Users/Harsh/OneDrive/Desktop/hackathin/DBMS project/Images"
pathlist=os.listdir(image_path)
print(pathlist)
img_list=[]
student_ids=[]
for path in pathlist:
    img_list.append(cv2.imread(os.path.join(image_path,path)))
    student_ids.append(os.path.splitext(path)[0])

    fileName=f'{image_path}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    #print(path)
    #print(os.path.splitext(path)[0])
    #print(len(img_list))
print(student_ids)



def findEncoding(img_list):
    encodelist=[]
    for img in img_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    
    return encodelist
print('encoding started')
encodelistknown=findEncoding(img_list)
encodelistknownwithids=[encodelistknown,student_ids]
print('encoding completed')

file=open('encodeing.p','wb')
pickle.dump(encodelistknownwithids,file)
file.close()