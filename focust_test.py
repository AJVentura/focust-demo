from pywebio.platform.flask import webio_view
from playsound import playsound
from pywebio.input import *
from pywebio.output import *
from pywebio.input import *
import time
import datetime
import cv2 as cv
from matplotlib import pyplot as plt
import pyqrcode
from cvzone.FaceMeshModule import FaceMeshDetector
from pymongo import MongoClient
from pywebio.session import *
import time
from datetime import date, timedelta
import random
from flask import Flask
import argparse
import re


'''def detect():
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime('%H:%M')
    global duration
    duration = datetime.timedelta(seconds=20)
    endTime = datetime.datetime.now() + duration
    endTime_toStr = endTime.strftime('%H:%M')
  
    put_text('Start studying!').style('font-size:50px').style('font-weight:bold').style('text-align:center')
    put_text('Session started: ', current_time_str).style('font-size:30px').style('font-weight:bold').style('text-align:center')
    put_text('Your session will end in: ', endTime_toStr).style('font-size:30px').style('font-weight:bold').style('text-align:center')
    cap = cv.VideoCapture(0)
    detector = FaceMeshDetector(maxFaces=1)

    faceIdList = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400,
       377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103,67, 109]
    eyeIdList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
    eyeRatioList = []
    faceRatioList = []

    ret, frame = cap.read()

    blinkCounter = 0
    counter = 0
    drowsiness = 0
    distraction = 0

    while True:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img, draw=False)

        if faces:
            face = faces[0]
            leftUpEye = face[159]
            leftDownEye = face[23]
            leftLeftEye = face[130]
            leftRightEye = face[243]
            verLengthEye, _ = detector.findDistance(leftUpEye, leftDownEye)  # vertical length
            horLengthEye, _ = detector.findDistance(leftLeftEye, leftRightEye)  # horizontal length

            UpFace = face[10]
            DownFace = face[152]
            leftFace = face[234]
            rightFace = face[454]
            verLength, _ = detector.findDistance(UpFace, DownFace)  # vertical length
            horLength, _ = detector.findDistance(leftFace, rightFace)  # horizontal length

            cv.line(img, leftUpEye, leftDownEye, (0, 200, 0), 3)
            cv.line(img, leftLeftEye, leftRightEye, (0, 200, 0), 3)

            cv.line(img, UpFace, DownFace, (0, 200, 0), 3)
            cv.line(img, leftFace, rightFace, (0, 200, 0), 3)

            faceRatio = int((verLength / horLength) * 100)
            faceRatioList.append(faceRatio)
            if len(faceRatioList) > 3:
                faceRatioList.pop(0)
            faceRatioAverage = sum(faceRatioList) / len(faceRatioList)

            if faceRatioAverage < 105 or faceRatioAverage > 130:     #from 105<  >120 to 120< >130
                time.sleep(1)
                distraction += 1
                print("Distraction level: ", distraction)
                with use_scope('distract'):
                    put_text("distraction level: ", distraction).style('text-align:center')
                with use_scope('distract', clear=True):  # enter the existing scope and clear the previous content
                    put_text("distraction level: ", distraction).style('text-align:center')

            eyeRatio = int((verLengthEye / horLengthEye) * 100)
            eyeRatioList.append(eyeRatio)
            if len(eyeRatioList) > 2:  #from 3 to 2 gin ubra ko 
                eyeRatioList.pop(0)
            ratioAverage = sum(eyeRatioList) / len(eyeRatioList)
        
            if ratioAverage < 30 and counter == 0:
                blinkCounter += 1
                counter = 1
                print('blink count: ', blinkCounter)
                with use_scope('blink'):
                    put_text('blink count: ', blinkCounter).style('text-align:center')
                with use_scope('blink', clear=True):  # enter the existing scope and clear the previous content
                    put_text('blink count: ', blinkCounter).style('text-align:center')

            if counter != 0:
                counter += 1
                if counter > 10:
                    counter = 0
            if ratioAverage <= 32:
                #time.sleep(1)
                drowsiness += 1
                print("drowsiness level: ", drowsiness)
                with use_scope('drowsy'):
                    put_text("drowsiness level: ", drowsiness).style('text-align:center')
                with use_scope('drowsy', clear=True):  # enter the existing scope and clear the previous content
                    put_text("drowsiness level: ", drowsiness).style('text-align:center')


        #focus score ni
        if datetime.datetime.now() >= endTime:
          divisor = 10
          playsound('./public/alarm.wav')
          blinkRate = blinkCounter/ divisor
          Fscore_i = blinkRate + drowsiness + distraction
          global FsFinal_A
          FsFinal_A = (float(Fscore_i/3))
          toast("session end", color="danger")
          put_text("Session A focus score: ", FsFinal_A).style('text-align:center').style('font-weight:bold')
          focus_scoreA = {
                'focus score A': FsFinal_A
                }
          #coll.insert_one(focus_scoreA)
          time.sleep(10)
          go_app('stroop', new_window=False)
          break'''

def index():
    print('AA')
    
client = MongoClient("mongodb+srv://ashcbrd5:ashcbrd@focust.tl2e9ka.mongodb.net/?retryWrites=true&w=majority")
db = client.Users
coll = db.Credentials

def login():
    
    info = input_group("Login",[
        input('Email', name='email', required=False),
        input('Password', name='password', type=PASSWORD, required=False),
    ],)

    #para ma access mo ang variables

    email = info['email']
    password = info['password']
    
    
    user_found = coll.find_one({"email": email})  # query by specified username
    if user_found:  # user exists
        if password == user_found['password']:
            toast('Login success!')
            go_app('index', new_window=False)
        else:
            toast('Wrong password')
            
            
    else:
        toast("user not found")
        
    put_buttons(['Register'], [lambda: go_app('register', new_window=False)]) # Use  
    
    
def register():
    levelResult = 0
    lvl = 0
    userPts = 0
    currentXP = 0
    divisor = 0
    duration = 0
    
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'  
    def checkValid(x):
        if x['name'] == "" or x['email'] == "" or x['password'] =="":
            toast("All fields required")
            register()
            #for valid email
        elif not (re.search(regex, x['email'])):
            toast('Invalid email!')
            register()
            #for confirm password
        elif x['password'] != x['confirmPassword']:
            toast("Please make sure your passwords match") 
            register()
            #for pass length
        elif len(x['password']) < 8:
            toast("password must be at least 8 characters long")
            register()

        
    info = input_group("Register",[
        input('Email', name='email', required=False),
        input('Name', name='name',type=TEXT, required=False),
        input('Password', name='password', type=PASSWORD, required=False),
        input('Confirm Password', name='confirmPassword', type=PASSWORD, required=False)
    ], cancelable=True, validate=checkValid)

    x = info #para sa checkValid() lang ra
    
    #para ma access mo ang variables
    userName = info['name']
    email = info['email']
    password = info['password']
    
    collection = {
            'name': userName,
            'email': email,
            'password': password,
            'focus_level': levelResult,
            'level': lvl,
            'user_points': userPts,
            'XP': currentXP,
            'divisor': divisor,
            'duration': duration
            }

    coll.insert_one(collection)
    toast("Registration Success")
    login() 
    
login()