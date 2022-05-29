from flask import Flask,render_template,request
import cv2
import numpy as np
import face_recognition
from datetime import datetime,date
import os
import pandas as pd





app = Flask(__name__)

#training images directory
UPLOAD_FOLDER = 'attendance_images'

app.config['SECRET_KEY'] = 'dineshchakri'
app.config['UPLOAD_PATH'] = 'attendance_images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}




@app.route('/show_data',  methods=("POST", "GET"))
def showData():
    df = pd.read_csv('attendance.csv')
    # Convert pandas dataframe to html table flask
    df_html = df.to_html()
    return render_template('index.html', data=df_html)


@app.route('/', methods=["GET"])
def home():
     return render_template('index.html')


@app.route('/Upload',methods=["GET","POST"])
def upload_file():
    if request.method == 'POST' :
        f = request.files['file-name']
        #adding images to the training images directory
        f.save(os.path.join(app.config['UPLOAD_PATH'],f.filename))
        return render_template('index.html' , msg="file uploaded successfully")
    return render_template('index.html',msg="please choose a file")

@app.route('/detection')
def Attendance():
    #the folder attendance_images has chosen as path of training images
    path = 'attendance_images'
    images = []
    classNames = []
    x = " "

    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        #the images are appended to "images" numpy array
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    #encodings of faces of images specified in particular directory is found
    def findEncodings(image):
        encodeList = []
        for img in image:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    #if the webcam captured face match with images in directory then the attendance of particular student is  recorded with his name and time of marking attendance

    def mark_attendance(name):
        with open('attendance.csv','r+') as f:
            myDataList = f.readlines()
            namelist = []
            for line in myDataList:
                entry = line.split(',')
                namelist.append(entry[0])
            #the name is recorded in the list if the attendance is not marked already this will avoid multiple entries
            if name not in namelist:
                #the time of particular moment is captured using datetime library
                now = datetime.now()
                today = date.today()
                dtString = now.strftime('%H:%M:%S')
                dString = today.strftime('%d/%m/%Y')
                f.writelines(f'\n{name},{dtString},{dString}')

    #function findEncodings is called
    encodeListKnown = findEncodings(images)
    print('encoding complete')
    #the webcam is opened to capture the image of student to mark attendance
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
            success, img = cap.read()
            if img is None:
                print('Wrong path:')
            else:
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            #face encodings of captured image is found
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                #the captured image is compared with training images
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                #the face distance is found with compared preloaded images of students
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                print(faceDis)
                #the index of minimum face distance is assigned to matchIndex
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    #the name of matchIndex is obtained by names list
                    name = classNames[matchIndex].upper()
                    x = name

                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
                    #the mark_attendance function called
                    mark_attendance(name)
                cv2.imshow('webcam', img)
                cv2.waitKey(1)

            return render_template('index.html', check=x)

if __name__ == '__main__':
    app.run(debug=True)
