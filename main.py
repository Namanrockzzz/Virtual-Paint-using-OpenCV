import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture('http://192.168.1.65:4747/mjpegfeed?640x480')
cap.set(3,frameWidth) # set width (width has id=3)
cap.set(4,frameHeight) # set height (height has id=4)
cap.set(10,150) # set brightness to 100

myColors = [[10,50,138,255,65,255], [0,4,73,255,0,255],[57,100,76,255,0,255],[90,118,48,255,0,255]] # Yellow, Red, Green (used thumpin for objects)
myColorValues = [[51,255,255],[51,51,255],[51,255,153],[255,0,0]]  #BGR format
myPoints = [] #[x,y,colorID]

def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for curr_color in myColors:
        lower = np.array([curr_color[0],curr_color[2],curr_color[4]])
        upper = np.array([curr_color[1],curr_color[3],curr_color[5]])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        # cv2.imshow(str(curr_color[2]),mask)
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            # cv2.drawContours(imgResult, cnt, -1, (255,0,0),3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

def DrawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
         cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)
while True:
    success , img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        DrawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Video", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break