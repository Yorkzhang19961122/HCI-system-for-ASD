import socket
import time
import numpy as np
import cv2 as cv
import sys 
import matplotlib.pyplot as plt
import argparse

HOST = '192.168.149.1'
PORT = 8007
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.connect((HOST, PORT))  
time.sleep(2)
get_time = 0

while True:
    sock.send(b'send')
    # time.sleep(0.05)
    recv_data = b""

    start = time.clock()
    msg = sock.recv(7)
    print(msg)

    if msg == b'sending':
        length = sock.recv(16)
        print(length)
        while len(recv_data) < int(length):
            recv_data += sock.recv(1024*8)
        data = np.frombuffer(recv_data,dtype=np.uint8)
        decodeimg = cv.imdecode(data, cv.IMREAD_COLOR)
    end = time.clock()   
    get_time += 1
    print('get image times : {1} time : {0}'.format(end-start, get_time))
    # fps = (end-start)/60
    key = cv.waitKey(1)

    if key & 0xFF == ord('q'):
    	break

    cv.imshow('img', decodeimg)

sock.close()  
