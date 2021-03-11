import socket
import time
import cv2
import threading
import sys
import numpy
import Serial_Servo_Running as SSR
import PWMServo
   
def yaotou():
    PWMServo.setServo(2, 1500, 400)
    time.sleep(0.4)
    PWMServo.setServo(2, 1900, 400)
    time.sleep(0.4)
    PWMServo.setServo(2, 1500, 400)
    time.sleep(0.4)
    PWMServo.setServo(2, 1100, 400)
    time.sleep(0.4)
    PWMServo.setServo(2, 1500, 400)
    time.sleep(0.4)
    PWMServo.setServo(2, 1900, 400)
    time.sleep(0.4)
    PWMServo.setServo(2, 1500, 400)
 
    
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
        if buf == b'walk':
            time.sleep(2)
            SSR.runAction('go')
            SSR.runAction('go')
            SSR.runAction('go')
            SSR.runAction('go')
            SSR.runAction('go')
            SSR.runAction('go')
            SSR.runAction('go')
            SSR.runAction('go')
            SSR.runAction('0')
            
        if buf == b'kick':
            time.sleep(2.5)
            SSR.runAction('53')
            
        if buf == b'wave':
            time.sleep(1.5)
            SSR.runAction('yds_skleft')
            
        if buf == b'punch':
            yaotou()
            yaotou()
            yaotou()
        
        if buf == b'squat':
            time.sleep(2)
            SSR.runAction('14')
            time.sleep(3)
            SSR.runAction('0')
    
connection.close()  


