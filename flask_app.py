from flask import Flask, jsonify, request ,redirect , url_for
from flask import render_template, Response
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin 

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pymongo
from attendanceDB import updateAttend


app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] ='mongodb://localhost:27017/StudentDB' 
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)

currentCollection = mongo.db.students

@app.route('/')
@cross_origin()
def home():
    return render_template("index1.html")

# @app.route('/admin')
# @cross_origin()
# def admin():
#     return render_template("admin1.html")

@app.route('/teacher')
@cross_origin()
def teacher():
    return render_template("teacher1.html")


@app.route('/all',methods = ['GET'])
@cross_origin()
def retrieveAll():

    records = list(currentCollection.find().sort("_id"))
    if len(records)==0:
        return render_template('noRecord.html',title="Students") 
    else:
        return render_template('render.html',records=records,title="Students")      
   
@app.route('/Attend/<attend>', methods=['GET'])
@cross_origin()
def retrieveFromAttend(attend):
    records = list(currentCollection.find({"Attendance": attend[0]}).sort("_id"))  
    if len(records)==0:
        return render_template('noRecord.html',title=attend)
    else:
        return render_template("render.html",records=records,title=attend)

@app.route('/postData', methods = ['POST'])
def postData():

    id = request.json['reg']
    name = request.json['name']
    currentCollection.insert_one({'_id':id, 'Name':name, 'Attendance': 'A'})
    
    return jsonify({'_id':id, 'Name':name, 'Attendance': 'A'})

@app.route('/deleteRec/<regno>', methods = ['GET',"DELETE"])
def deleteRec(regno):
    currentCollection.delete_one({'_id':int(regno)})
    records = list(currentCollection.find().sort("_id"))
    if len(records)==0:
        return render_template('noRecord.html',title="Students") 
    else:
        return render_template('render.html',records=records,title="Students")

@app.route('/updateDataA', methods=['GET'])
@cross_origin()
def updateDataA():
    # updatedName = request.json['name']
    currentCollection.update_many({},{"$set":{"Attendance": "A"} })
    records = list(currentCollection.find().sort("_id"))
    if len(records)==0:
        return render_template('noRecord.html',title="Students") 
    else:
        return render_template('render.html',records=records,title="Students")

@app.route('/check/<uid>&<passw>')
@cross_origin()
def loginID(uid,passw):
    # uid = request.json['uid']
    # passw = request.json['pass']
    currentCollectionL = mongo.db.passwords
    # rec = bool(currentCollectionL.find_one({"_id":uid},{"password":passw}))
    # if rec == 1:
    #     return render_template('admin.html')
    # else:
    #     return render_template('noRecord.html',title="Invalid Login")
    rec = currentCollectionL.find_one({"_id":uid},{"password":passw})
    if rec['_id'] == uid and rec['password']== passw:
        return render_template('admin.html')
    else:
        return render_template('noRecord.html',title="Invalid Login")
    
path = "Resources//Faces"
images = []
classNames = []
myList = os.listdir(path)
# print(myList)

for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        imgS = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
        encode = face_recognition.face_encodings(img)[0]  #encode face
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
#mark time
def markDB(name):
    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
    myDB = myClient["StudentDB"]
    myColl = myDB["students"]
    updateAttend(int(name) )

camera = cv2.VideoCapture(0)
def gen_frames():
    while True:
        success, img = camera.read()
        if not success:
            break
        else:
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDist)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    y1,x1,y2,x2 = faceLoc
                    y1,x1,y2,x2 = y1*4,x1*4,y2*4,x2*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0))
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                    markDB(name)
                

            ret, buffer =cv2.imencode('.png',img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/Capture')
def index():
    return render_template('imgCap.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)