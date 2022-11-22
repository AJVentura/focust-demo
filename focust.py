from pywebio.platform.flask import webio_view
from playsound import playsound
from pywebio.input import *
from pywebio.output import *
import time
import datetime
import cv2 as cv
from matplotlib import pyplot as plt
import pyqrcode
from cvzone.FaceMeshModule import FaceMeshDetector
from pymongo import MongoClient
from pywebio.session import *
from pywebio import *
import time
from datetime import date, timedelta
import random
from flask import Flask
import argparse
import re

app = Flask(__name__)

client = MongoClient("mongodb+srv://ashcbrd5:ashcbrd@focust.tl2e9ka.mongodb.net/?retryWrites=true&w=majority")

db = client.Users
coll = db.Credentials

divisor = 10

#=============LOGIN==================#
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
            index()
            
    else:
        toast("user not found")
        index()
    put_buttons(['Register'], [lambda: go_app('register', new_window=False)]) # Use  
    
#============REGISTER=============#
def register():
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
            'password': password
            }

    coll.insert_one(collection)
    toast("Registration Success")
    index() 

#=============INDEX===============#

def index():
    header()
    name = 'a' #coll.find_one()
    pts = '0' #focus_level.userPts

    lvl = 'foo' #focus_level.lvl
    session = "foo"
    img = open('public/neighbor.jpg', 'rb').read() 
    def redeemPopup():
        popup('Rewards', [
            put_text('Choose your redeemable reward'),
            put_row([
                put_button('10% off', onclick=createQR10, color='success'),
                put_button('15% off', onclick=createQR15, color='success'), 
                put_button('20% off', onclick=createQR20, color='success'),  
            ]),
                
            put_buttons(['close'], onclick=lambda _: close_popup())
            ])
    
    with use_scope():
        put_text('Hi there!').style('font-size:50px').style('font-weight: bold')

    
    put_tabs([
        {'title': 'About👁️','content':[put_text('FocusT uses eye tracking AI technology to monitor you while you study and trains you to improve your focus!'),  put_text('This web app is developed by a group of five third-year college students taking Bachelor of Science in Information Technology in West Visayas State University.')]},
        {'title': 'Dashboard📋','content':[put_tabs([
        
        {'title': 'Start Session', 'content': [ put_text('Press the button to start session'), put_button('Start', onclick=lambda: go_app('detect', new_window=False),  color='success') ]},
        {'title': 'User Level', 'content': [ put_text('Level', lvl).style('font-weight: bold'),put_text('XP to next level: ', lvl ), put_text('Your points: ', pts ).style('font-weight: bold'),]},
        {'title': 'Recent Sessions', 'content':[put_collapse('Session 1',[session]),put_collapse('Session 1',[session]),put_collapse('Session 1',[session])]}
    ])]},
        
        {'title': 'Rewards🎉','content':[ put_text('You can claim rewards in exchange for points here'),   put_tabs([
        {'title':'Neighbor Coffee', 'content':[put_text('Neighbor coffee ☕').style('font-weight: bold'), put_row([put_image(img, height='150px'), put_text('NEIGHBOR COFFEE started as a roadside cafe in our Cagbang neighborhood, January of 2021. we offer manual brews and handcrafted espressos using specialty coffee beans that are both sourced locally and globally. we are a community of slow living and coffee-loving people who are conscious about the traceability, sustainability, and quality of the coffee they consume. we exist to promote traceable, sustainable, and quality coffee so that everyone in the coffee supply chain is empowered and given the value they deserve.')], size='200px'),put_button('Redeem Rewards', onclick=redeemPopup) ]},
        {'title':'Coming Soon', 'content':[put_text('✨Coming Soon✨')]},
        {'title':'Coming Soon', 'content':[put_text('✨Coming Soon✨')]}
    ])]},
        {'title': 'Manual📖', 'content':put_button('Check Manual', onclick=lambda: go_app('manual', new_window=False), color='success')},
        {'title': 'Logout🚪', 'content':put_button('Logout', onclick=lambda: logout(), color='danger')}
        
    ])    
#=====diri gaprint qr code===========
    def createQR10():
        if  userPts >=100:
            userPts-100
            s = date.today() + timedelta(days=2) 
            expiration = "This 10% off coupon is valid until: " + str(s)
            url = pyqrcode.create(expiration)
            url.png('coupon-10.png', scale = 6)
            content = open('coupon-10.png', 'rb').read()
            popup('Download your Coupon',[
                            
            put_file('10% off coupon.png', content, 'Click me')  
                        ])
            toast("Great! coupon created")
        else:
            toast('insufficient points', color='red')

    def createQR15():
        if  userPts >=150:
            userPts-150
            s = date.today() + timedelta(days=2) 
            expiration = "This 15% off coupon is valid until: " + str(s)
            url = pyqrcode.create(expiration)
            url.png('coupon-15.png', scale = 6)
            content = open('coupon-15.png', 'rb').read()
            popup('Download your Coupon',[
                        
            put_file('15% off coupon.png', content, 'Click me')  
                    ])
            toast("Great! coupon created")  
        else:
            toast('insufficient points',color='red')
        

    def createQR20():
        if userPts >=200:
            userPts-200
            s = date.today() + timedelta(days=2) 
            expiration = "This 20% off coupon is valid until: " + str(s)
            url = pyqrcode.create(expiration)
            url.png('coupon-20.png', scale = 6)
            content = open('coupon-20.png', 'rb').read()
            popup('Download your Coupon',[
                        
            put_file('20% off coupon.png', content, 'Click me')  
                    ])
            toast("Great! coupon created")   
        else:
            toast('insufficient points',color='red')


    



#=======LOGOUT==============

def logout():
    toast("you have logged out")

def header():
    content = open('public/mainlogo.png', 'rb').read()
    put_image(content, height='60px')
    
#============DETECT.PY==================
def detect():
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime('%H:%M')
    global duration
    duration = datetime.timedelta(seconds=5)
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
          coll.insert_one(focus_scoreA)
          time.sleep(5)
          go_app('stroop', new_window=False)
          break


#########################################

#======STROOP=============
def stroop():
    with use_scope('stroop', clear=True):
        def remove():
            clear('stroop')
            go_app('detectB', new_window=False)
    
        def countdown():
                duration = 5
                
                while duration > 0:
                    
                    with use_scope('time'):
                        put_text('you can skip this in',duration).style('text-align:center').style('margin-top:100px').style('font-weight:bold')
                        duration -=1
                        time.sleep(1)
                        clear('time')
                    if duration == 0:
                        
                        put_button('Skip', onclick=remove, color="success").style('margin-top:100px').style('align-items: center')


        def stroop():
            
                
            colorNames  = ["red", "green", "blue"]
            colorStyles = ['color:red', 'color:green', 'color:blue']
            clear('color')
            stroop.x =random.choice(colorNames)
            stroop.y = random.choice(colorStyles)
        
            with use_scope('color',clear=True):
                put_row([put_text('What color is this?').style('font-size:30px'),None,
                put_text(stroop.x).style(stroop.y).style('font-size:30px')])
                    
                    
                        
                def red():
                    if stroop.y =="color:red":
                        toast("correct", color='green')
                        clear('color')
                        stroop.x =random.choice(colorNames)
                        stroop.y = random.choice(colorStyles)
                        with use_scope('color',clear=True):
                            put_row([put_text('What color is this?').style('font-size:30px'), None,
                            put_text(stroop.x).style(stroop.y).style('font-size:30px')])
                    else:
                        toast("wrong", color='red') 

                def green():
                    if stroop.y =="color:green":
                        toast("correct", color='green')
                        clear('color')
                        stroop.x =random.choice(colorNames)
                        stroop.y = random.choice(colorStyles)
                        with use_scope('color',clear=True):
                            put_row([put_text('What color is this?').style('font-size:30px'), None,
                            put_text(stroop.x).style(stroop.y).style('font-size:30px')])
                    else:
                        toast("wrong", color='red') 
                        
                def blue():
                    if stroop.y == "color:blue":
                        toast("correct", color='green')
                        clear('color')
                        stroop.x =random.choice(colorNames)
                        stroop.y = random.choice(colorStyles)
                        with use_scope('color',clear=True):
                            put_row([put_text('What color is this?').style('font-size:30px'), None,
                            put_text(stroop.x).style(stroop.y).style('font-size:30px')])
                    else:
                        toast("wrong", color='red')     
                        
                        
            put_column([put_markdown('# Stroop Test').style('font-size: 30px'), put_text('Instructions: choose the button with the correct color the text is diplayed in.').style('font-size: 25px')
                            ])    

                    
            put_row([put_button("red", onclick=red), None,
            put_button("green", onclick=green), None,
            put_button("blue", onclick=blue), None])
        stroop()
        countdown()
#========DETECT_B.PY============== 
#def back():
    #go_app('index', new_window=False)  
       
def detectB():
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime('%H:%M')
    duration = datetime.timedelta(seconds=10)
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
            global divisor
            playsound('./public/alarm.wav')
            blinkRate = blinkCounter/ divisor
            Fscore_i = blinkRate + drowsiness + distraction
            global FsFinal_B
            FsFinal_B = (float(Fscore_i/3)) 
            toast("session end", color="danger")
            put_text("Session B focus score: ", FsFinal_B).style('text-align:center').style('font-weight:bold')
            focus_scoreB = {
                    'focus score B': FsFinal_B
                    }
            coll.insert_one(focus_scoreB)
        #====== focus level na part =====    
            global levelResult  
            if FsFinal_A > FsFinal_B:
                FL =  ((FsFinal_B - FsFinal_A)/FsFinal_A) * 100  
            
                levelResult =abs(float(round(FL,2)))
            else:
                FL =  ((FsFinal_A- FsFinal_B)/FsFinal_A) * 100  
            
                levelResult =float(round(FL,2))
            
            global userPts #ilagay nalang sa DB
            userPts = 0
            global currentXP
            currentXP = 0
            #XPtoLvlUp = 100 #muni baseline
            global lvl
            lvl=1
            currentXP = levelResult + currentXP
            if currentXP >= 100:
                toast('Yay! You levelled up!')
                lvl +=1
                userPts +=200
                divisor +=5
                #coll.insert_one(userPts) # Gchange to update, indi insert
                #duration + datetime.timedelta(minutes=5) # add duration 
                #print(lvl)
                #print("your points",userPts)
                #else:
                    #print('need more XP')
                    #print(currentXP)
                
            
            put_text('your focus level is:', levelResult).style('text-align:center').style('font-weight:bold')
            put_text('current level:', lvl).style('text-align:center').style('font-weight:bold')
            put_text('Xp:', currentXP ).style('text-align:center').style('font-weight:bold')
            time.sleep(10)
            go_app('index', new_window=False)        
            break
      
#========FOCUS LEVEL================= 

'''def focus_level():
    global levelResult
   
    
    if FsFinal_A > FsFinal_B:
        FL =  ((FsFinal_B - FsFinal_A)/FsFinal_A) * 100  #or algo purposes, wala gin sunod ang sa paper na formula ky same angud
        
        levelResult =float(round(FL,2))
    else:
        FL =  ((FsFinal_A- FsFinal_B)/FsFinal_A) * 100  #or algo purposes, wala gin sunod ang sa paper na formula ky same angud
        
        levelResult =float(round(FL,2))
        
    
   
    global currentXP
    currentXP = 0
    XPtoLvlUp = 100 #muni baseline
    global lvl
    lvl=0
    
    
    
    currentXP = levelResult + currentXP
    
    if currentXP >= XPtoLvlUp:
        toast('Yay! You levelled up!')
        lvl +=1
        userPts +=200
        #coll.insert_one(userPts) # Gchange to update, indi insert
        duration + datetime.timedelta(minutes=5) # add duration 
        #print(lvl)
        #print("your points",userPts)
        #else:
            #print('need more XP')
            #print(currentXP)
        
   
    put_text('your focus level is:', levelResult)
    put_text('current level:', lvl)
    put_text('Xp:', currentXP )
    
        
    #print(levelResult)  '''
      
#=========MANUAL====================
def manual():
    put_text('User Manual\n\n').style('font-size:30px').style('font-weight:bold').style('text-align:center')
    put_text('✅ Open Materials of Choice \n Open your learning materials that you will use for studying such as ppt, word documents, pdf, ebooks etc.'),
    put_text('✅ Study Session continues while the application is running in the background \n The first session of the study will stop when the alarm rings. It will be the cue for a 10 minute break. Note: There will be an alert given in every session that is about to end.'),
    put_text('✅ Break Time! \n After your first session, a gamified version of a Stroop Test will show up for you to play.'),
    put_text('✅ Second Session \n After the break, the second session will start.'),
    put_text('✅ Finished! \n you will receive XP based on how you did. Start multiple sessions for you to level up and earn Points!')
    put_button('Back', onclick=lambda: go_app("index", new_window=False), color='danger')
    

app.add_url_rule('/focust', 'web_view', webio_view(index), methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=3000)
    args = parser.parse_args()

start_server([login, index, detect, detectB, stroop, manual,], port=args.port)

