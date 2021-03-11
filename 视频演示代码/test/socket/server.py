import socket
import time
import cv2
 
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()   #读取一帧视频
    while _ :
        print(frame.shape)
        cv2.imshow("1", frame)
    key = cv2.waitKey()