import socket
import time
import cv2
import threading
import sys
import numpy
import Serial_Servo_Running as SSR
import PWMServo

SSR.runAction('0')
HOST = '172.20.10.2'

PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind((HOST, PORT))  
sock.listen(5)  
connection, address = sock.accept()
print('connect success')

while True:
    
    buf = connection.recv(10)  
    if buf:  
        print(buf)
        
        if buf == b'hello':
            time.sleep(6)
            PWMServo.setServo(2, 1100, 500)
            SSR.runAction('9')
            PWMServo.setServo(2, 1500, 500)
            
        if buf == b'happy':
            time.sleep(1)
            SSR.runAction('yds_happy1')
            
        if buf == b'surprise':
            time.sleep(1)
            SSR.runAction('13')
            
        if buf == b'sad':
            time.sleep(14)
            SSR.runAction('15')
        
        if buf == b'skhand':
            time.sleep(0.5)
            SSR.runAction('yds_skright')
            time.sleep(1.5)
            SSR.runAction('yds_skleft')
        
        if buf == b'squat':
            time.sleep(2)
            SSR.runAction('14')
            time.sleep(5)
            SSR.runAction('0')
    
connection.close()  


