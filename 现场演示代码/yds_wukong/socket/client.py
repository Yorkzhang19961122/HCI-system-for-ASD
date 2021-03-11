import socket
from PIL import Image
from io import StringIO
import time
import numpy as np
import cv2 as cv
import sys 
import matplotlib.pyplot as plt
import argparse



# from keras.applications import VGG16


#image = np.zeros((240,320,3),dtype=np.uint8)
cvimage = np.zeros((480*640*3),dtype=np.uint8)
pltimage = np.zeros((480,640,3),dtype=np.uint8)
HOST = '192.168.3.100'
PORT = 8881


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.connect((HOST, PORT))  
time.sleep(2)
print('connect')
get_time = 0


while True:
    sock.send(b'send')
    recv_data = b""
    start = time.clock()
    while sys.getsizeof(recv_data) < 921600:
        recv_data += sock.recv(1024*8)
    cvimage = np.frombuffer(recv_data,dtype=np.uint8)
    cvimage = cvimage.reshape(480,640,3)   
    
    print('receive image')
    # PLTimage = Image.fromarray(pltimage)
    # PLTimage.resize((418,418))
    # r_image,personinfo = YOLO(**vars(FLAGS)).detect_image(PLTimage)
   
    # plt.imshow(PLTimageBGR)
    # plt.show()
    # print(image2.mode)
    # image2.show()
    end = time.clock()   
    get_time += 1
    print('get image times : {1} time : {0}'.format(end-start, get_time))
    key = cv.waitKey(1)
    if key & 0xFF == ord('q'):
        i = 0
        if i < 100:
            sock.recv(1024*8)
            i = i + 1
            sock.close()
        break
    cv.imshow('0', cvimage)

# print(image.format)
#print(image)
sock.close()  
