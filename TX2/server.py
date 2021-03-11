import socket
import time
import cv2
import threading
import sys
import numpy


cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)
HOST = '192.168.3.110'  #wang xian ip
#HOST = '172.20.10.6'	#zykiphone ip
PORT = 8009

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind((HOST,PORT))
sock.listen(5)  
connection, address = sock.accept()

size =(640,480)
fps = 11
print('connect succese')
orgFrame = None
ret = False
Running = True
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), 100]

def get_image():
    global orgFrame
    global ret
    global Running
    global cap
    while True:
        if Running:
            if cap.isOpened():
                ret, orgFrame = cap.read()
                cv2.imshow('1', orgFrame)
                cv2.waitKey(1)
       
            else:
                time.sleep(0.001)
        else:
            time.sleep(0.001)

th1 = threading.Thread(target = get_image)
th1.setDaemon(True)
th1.start()

stringData1=[]
while True:
    
    if ret: 
   
        result , imgencode = cv2.imencode('.jpg', orgFrame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        
        # time.sleep(0.05)
        # cv2.waitKey(1)
            # connection.settimeout(10)  
        buf = connection.recv(1024)  
        if buf:  
            print(buf)
            if buf == b'send':
                connection.send(b'sending')
                connection.send(str.encode(str(len(stringData)).ljust(16)))
                print(len(stringData))
                connection.send(stringData)
                print('Sending image')
                pass
            else:
                print('receive buf error')

    else:
        pass
    
connection.close()  


