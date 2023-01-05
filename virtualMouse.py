import cv2
import numpy as np
import handTrackingModule as htm
import time
import autopy
import math


#########################################
wCam, hCam=640,480
frameR=100
smoothening=7
pTime=0
plocX,plocY=0,0
clocX,clocY=0,0
###########################################
cap =cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector=htm.handDetector(maxHands=1)
wScr, hScr=autopy.screen.size()
# print(wScr,hScr)
while True:
    # find the hand landmarks
    success,img=cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    # get the tip of index and middle finger
    if len(lmList)!=0:
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
    # check fingers are up
        fingers=detector.fingersUp()
        # print(fingers)
    # only index finger
        if fingers[1]==1 and fingers[2]==0:
    # convert coordinates

            x3=int(np.interp(x1,(frameR,wCam-frameR),(0,wScr-1)))
            y3=int(np.interp(y1,(frameR,hCam-frameR),(0,hScr-1)))
            # smooth the values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
    # move mouse
            autopy.mouse.move(clocX,clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,plocY=clocX,clocY
    # both index and middle finger up
        if fingers[1] == 1 and fingers[2] == 1:
    # find distance between fingers
            length = math.hypot(x2 - x1, y2 - y1)
            if length < 30:
                cv2.circle(img, (x1, y1), 15, (0, 255,0), cv2.FILLED)
                autopy.mouse.click()
    # frame rate
    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
    # display
    cv2.imshow("Image",img)
    cv2.waitKey(1)

