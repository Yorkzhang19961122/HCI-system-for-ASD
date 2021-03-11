'''
1、运行程序后，输入需要采集图像的表情名emotion_name,
2、建立该表情名的文件夹，路径为img_path，
3、采集到一定数量图像并保存到img_path
'''

import cv2
import os


# 调用笔记本内置摄像头(参数为0)，如果有其它的摄像头可以调整参数为1，2
cap = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier('/home/admin1/Projects/02_Emotion_Classifier/Opencv_Classifier/haarcascade_frontalface_default.xml')

emotion_name = input('\nEnter emotion name:')
os.mkdir('/home/admin1/Projects/02_Emotion_Classifier/emotion_data/raw_data/'+str(emotion_name))
img_path = os.path.dirname('/home/admin1/Projects/02_Emotion_Classifier/emotion_data/raw_data/'+str(emotion_name)+'/')
print('\nInitializing face emotion capture. Look at the camera and wait ...')
# 初始化采集面部表情图像的数量
count = 0

while True:

    # 从摄像头读取图片

    ret, img = cap.read()

    # 转为灰度图片

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 检测人脸

    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+w), (0, 0, 255), 4)
        count += 1
        print('Now collecting img: %s' %count)
        # 保存图像到img_path路径
        img_gray = gray[y: y + h, x: x + w]
        img_gray_resize = cv2.resize(img_gray,(100,100))
        # cv2.imwrite(str(img_path) +'/' + str(count) + '.jpg', gray[y: y + h, x: x + w])
        cv2.imwrite(str(img_path) +'/' + str(count) + '.jpg', img_gray_resize)
        cv2.imshow('image', img)


    k = cv2.waitKey(1)
    if k == 27:   # 按'ESC'键退出摄像
        break
    elif count >= 1000:  # 得到count个样本后退出摄像
        break
print('Ending!')
print('\nExiting program!')
cap.release()
cv2.destroyAllWindows()
