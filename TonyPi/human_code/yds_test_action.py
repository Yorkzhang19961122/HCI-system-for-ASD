import socket
import time
import cv2
import threading
import sys
import numpy
import Serial_Servo_Running as SSR
import PWMServo
SSR.runAction('0')

def diantou():
    PWMServo.setServo(1, 1500, 500)
    time.sleep(0.5)
    PWMServo.setServo(1, 1000, 500)
    time.sleep(0.5)
    PWMServo.setServo(1, 1500, 500)
    
    PWMServo.setServo(1, 1500, 500)
    time.sleep(0.5)
    PWMServo.setServo(1, 1000, 500)
    time.sleep(0.5)
    PWMServo.setServo(1, 1500, 500)
    
    PWMServo.setServo(1, 1500, 500)
    time.sleep(0.5)
    PWMServo.setServo(1, 1000, 500)
    time.sleep(0.5)
    PWMServo.setServo(1, 1500, 500)
    
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
    time.sleep(0.4)
    PWMServo.setServo(2, 1100, 400)
    time.sleep(0.4)
    PWMServo.setServo(2, 1500, 400)
    
while True:
    n = input()
    # n =0
    if n == '1':
        SSR.runAction('53')
    if n == '2':
        SSR.runAction('go')
    if n == '3':
        SSR.runAction('15')
        
    if n == '4':
        # yao tou
       diantou()
        
        
    if n == '5':
        yaotou()
        
    if n == '6':
        SSR.runAction('14')
        time.sleep(5)
        SSR.runAction('0')
        
    if n == '7':
        SSR.runAction('8')

        
    
    


