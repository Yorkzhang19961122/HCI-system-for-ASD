import socket
import time
import cv2
import threading
import sys
import numpy
import PWMServo
import Serial_Servo_Running as SSR
import cv2
import time
import math
import sys
import socket
import signal
import threading
import PWMServo
import numpy as np
from cv_ImgAddText import *
from config import color_range


PWMServo.setServo(1, 1000, 1000)
PWMServo.setServo(2, 1450, 1000)

SSR.runAction('0')
SSR.start_action_thread()

stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"
cap = cv2.VideoCapture(stream)
cap.release()

cap = cv2.VideoCapture(stream)
HOST = '192.168.149.1'
PORT = 8001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind((HOST, PORT))

sock.listen(5)  
connection, address = sock.accept()
print('connect succese')
orgFrame = None
ret = False
Running = True
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), 15]


# find line part


c = 80
width, height = c*4, c*3
ori_width  =  int(4*160)#原始图像640x480
ori_height =  int(3*160)
line_color     = (255, 0, 0)#图像显示时，画出的线框颜色
line_thickness = 2         #图像显示时，画出的线框的粗细
roi = [ # [ROI, weight]
        (0,  40,  0, 160, 0.5), 
        (40, 80,  0, 160, 0.3), 
        (80, 120,  0, 160, 0.2)
       ]



def leMap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def picture_circle(orgimage, x, y, r, resize_w, resize_h, l_c = line_color, l_t = line_thickness):
    global ori_width
    global ori_height
    
    x = int(leMap(x, 0, resize_w,  0, ori_width))
    y = int(leMap(y, 0, resize_h,  0, ori_height))
    r = int(leMap(r, 0, resize_w,  0, ori_width))   
    cv2.circle(orgimage, (x, y), r, l_c, l_t)
    
    
def getAreaMaxContour(contours,area=1):
        contour_area_max = 0
        area_max_contour = None

        for c in contours :
            contour_area_temp = math.fabs(cv2.contourArea(c))
            if contour_area_temp > contour_area_max : 
                contour_area_max = contour_area_temp
                if contour_area_temp > area:#面积大于1
                    area_max_contour = c
        return area_max_contour

def find_line(orgimage, r_w, r_h, flag,r = roi, l_c = line_color, l_t = line_thickness):
    state = [0,0,0,0,0,0]
    global ori_width, ori_height
    global img_center_x, img_center_y
    deflection_angle = 0
    global get_line
    #图像缩小，加快处理速度
    orgframe = cv2.resize(orgimage, (r_w, r_h), interpolation = cv2.INTER_LINEAR)
    
    Frame = cv2.GaussianBlur(orgframe, (3, 3), 0)
    Frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2LAB) #将图像转换到LAB空间
    Frame = cv2.inRange(Frame, color_range['black'][0], color_range['black'][1]) #根据hsv值对图片进行二值化 
    opened = cv2.morphologyEx(Frame, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))#开运算
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))#闭运算

    
    centroid_x_sum = 0
    area_sum = 0
    n = 0
    weight_sum = 0
    center_ = []
    max_area = 0
    n = 0
    x_indx = 0
    y_indx = 1
    for r in roi:
        n += 1
        blobs = closed[r[0]:r[1], r[2]:r[3]]
        img, cnts, _  = cv2.findContours(blobs , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)#找出所有轮廓
        cnt_large  = getAreaMaxContour(cnts)#找到最大面积的轮廓

        if cnt_large is not None:
            rect = cv2.minAreaRect(cnt_large)#最小外接矩形
            box = np.int0(cv2.boxPoints(rect))#最小外接矩形的四个顶点
            box[0, 1], box[1, 1], box[2, 1], box[3, 1] = box[0, 1] + (n - 1)*r_w/4, box[1, 1] + (n - 1)*r_w/4, box[2, 1] + (n - 1)*r_w/4, box[3, 1] + (n - 1)*r_w/4
            box[1, 0] = int(leMap(box[1, 0], 0, r_w, 0, ori_width))
            box[1, 1] = int(leMap(box[1, 1], 0, r_h, 0, ori_height))
            box[3, 0] = int(leMap(box[3, 0], 0, r_w, 0, ori_width))
            box[3, 1] = int(leMap(box[3, 1], 0, r_h, 0, ori_height))
            box[0, 0] = int(leMap(box[0, 0], 0, r_w, 0, ori_width))
            box[0, 1] = int(leMap(box[0, 1], 0, r_h, 0, ori_height))
            box[2, 0] = int(leMap(box[2, 0], 0, r_w, 0, ori_width))
            box[2, 1] = int(leMap(box[2, 1], 0, r_h, 0, ori_height))
            pt1_x, pt1_y = box[0, 0], box[0, 1]
            pt3_x, pt3_y = box[2, 0], box[2, 1]
            area = cv2.contourArea(box)
            
            if flag:
                cv2.drawContours(frame, [box], -1, (0,0,255,255), 2)#画出四个点组成的矩形            
            center_x, center_y = (pt1_x + pt3_x) / 2, (pt1_y + pt3_y) / 2#中心点
            center_.append([center_x,center_y])            
            if flag:
                cv2.circle(frame, (int(center_x), int(center_y)), 10, (0,0,255), -1)#画出中心点
            centroid_x_sum += center_x * r[4]
            weight_sum += r[4]
            
            state[x_indx] = int(center_x)
            state[y_indx] = int(center_y)
            x_indx += 2
            y_indx += 2
    if weight_sum is not 0:
        center_x_pos = centroid_x_sum / weight_sum
        #中间公式
        deflection_angle = 0.0
        deflection_angle = -math.atan((center_x_pos - img_center_x/2)/(img_center_y/2))
        deflection_angle = deflection_angle*180.0/math.pi
        #print(center_x_pos)
         #框中心画十字
        #cv2.line(orgimage, (img_center_x/2, img_center_y), (int(center_x_pos), img_center_y/2), l_c, l_t)         
    get_line = True       
    
    #t2 = cv2.getTickCount()
    #time_r = (t2 - t1) / cv2.getTickFrequency()               
    #fps = 1.0/time_r
    #cv2.putText(frame, "FPS:" + str(int(fps)),
    #        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)   #(0, 0, 255)BGR                     
    #cv2.imshow('orgframe', frame) #显示图像
    #cv2.waitKey(1)
    return state, deflection_angle

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
                time.sleep(0.01)
        else:
            time.sleep(0.01)

th1 = threading.Thread(target = get_image)
th1.setDaemon(False)
th1.start()

stringData1=[]
while True:
    # ret = True
    '''
    if orgFrame is not None and ret:
        #result , imgencode = cv2.imencode('.jpg', orgFrame, encode_param)
        imgencode = []
        # state = find_line()
        data = numpy.array(imgencode)
        stringData = data.tostring()
        stringData1 = stringData
    '''    
    # time.sleep(0.05)
    # cv2.waitKey(1)
        # connection.settimeout(10)  
    buf = connection.recv(4)
    # buf = Fals
    if buf:  
        print(buf)
        if buf == b'rset':
            img_center_x = orgFrame.shape[:2][1]
            img_center_y = orgFrame.shape[:2][0]
            state,angle  = find_line(orgFrame, 160, 120, False)
            print('state : {}'.format(state))
            time.sleep(1)
            # send state
            for i in range(0, len(state)):
                connection.send(str.encode(str(state[i])).ljust(8))
                
        if buf == b'move':
            action = connection.recv(6)
            print('action : {}'.format(action))    
            if action == b'goforw':
                SSR.runAction('go')
            if action == b'goleft':
                SSR.runAction('left_move_one_step')
            if action == b'gorigh':
                SSR.runAction('right_move_one_step')
            if action == b'restar':
                SSR.runAction('0')
                
            time.sleep(1)
            # send next state
            frame = orgFrame.copy()
            state,angle  = find_line(orgFrame, 160, 120, False)
    
            print('next state {}: '.format(state))
            print('angle : {}'.format(angle))
            # send state
            for i in range(0, len(state)):
                connection.send(str.encode(str(state[i])).ljust(8))
            connection.send(str.encode(str(int(angle))).ljust(8))  # state angle as reward
        
    else:  
        # connection.send(b'please go out!')
        pass
    
cap.release()
connection.close()  
