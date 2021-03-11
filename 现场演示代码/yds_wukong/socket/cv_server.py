#-*- coding: utf-8 -*-

import cv2
import sys
import gc
import json
import numpy as np
import socket
import time


if __name__ == '__main__':
     
    HOST = '192.168.3.100'
    PORT = 8881
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.bind((HOST, PORT))  
    sock.listen(5)  
    cap = cv2.VideoCapture(0)
    connection,address = sock.accept()  
    
    while True:
        _, frame = cap.read()   #读取一帧视频
        if _:
            print(frame.shape)
            # connection.settimeout(10)  
            buf = connection.recv(1024)  
            if buf:  
                print(buf)
                if (buf == b'send'):  
                    print('sending iamge')
                    connection.send(frame)
                    pass
            else:  
                connection.send(b'please go out!')  
        # except socket.timeout:  
        #     print ('time out')
       
        # if k & 0xFF == ord('q'):
        #     break

    #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()
