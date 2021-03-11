''' 与EAIDK-310,socket通信,取310上的摄像头数据
'''
import asyncio
from mini.apis import errors
from mini.apis.api_expression import ControlBehavior, ControlBehaviorResponse, RobotBehaviorControlType
from mini.apis.api_expression import ControlMouthLamp, ControlMouthResponse
from mini.apis.api_expression import PlayExpression, PlayExpressionResponse, RobotExpressionType
from mini.apis.api_expression import SetMouthLamp, SetMouthLampResponse, MouthLampColor, MouthLampMode
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice

from test_connect import test_connect, shutdown, test_start_run_program
from test_connect import test_get_device_by_name
from test_sound import *
from test_action import *
import socket
import keras
import tensorflow as tf
import time
import cv2
import sys
import numpy as np
from keras.models import model_from_json
#----------------------socket----------------------------------
cvimage = np.zeros((480*640*3),dtype=np.uint8)
pltimage = np.zeros((480,640,3),dtype=np.uint8)
HOST = '192.168.3.100'
PORT = 8881
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print('connet success')
time.sleep(2)
get_time = 0
#-------------------------------------------------------------

#config GPU
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
keras.backend.tensorflow_backend.set_session(tf.Session(config=config))

root_path='/home/zcx/emotion_classifier/pic/'
model_path=root_path+'/model/'
img_size=48
# emo_labels = ['angry','disgust','fear','happy','sad','surprise','neutral']
#load json and create model arch
emo_labels = ['sad', 'neutral', 'neutral', 'happy', 'sad', 'surprise', 'neutral']
num_class = len(emo_labels)
json_file=open(model_path+'model_json.json')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
#load weight
model.load_weights(model_path+'model_weight.h5')


# 测试让眼睛演示个表情
async def test_play_expression():
    """测试播放表情

    让机器人播放一个名为"codemao1"的内置表情，并等待回复结果

    #PlayExpressionResponse.isSuccess : 是否成功

    #PlayExpressionResponse.resultCode : 返回码

    """
    # express_type: INNER 是指机器人内置的不可修改的表情动画, CUSTOM 是放置在sdcard/customize/expresss目录下可被开发者修改的表情
    block: PlayExpression = PlayExpression(express_name="codemao1", express_type=RobotExpressionType.INNER)
    # response: PlayExpressionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_expression result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_play_expression timetout'
    assert response is not None and isinstance(response,
                                               PlayExpressionResponse), 'test_play_expression result unavailable'
    assert response.isSuccess, 'play_expression failed'


# 测试, 让机器人跳舞/停止跳舞
async def test_control_behavior():
    """测试控制表现力

    让机器人开始跳一个名为"dance_0004"的舞蹈，并等待回复结果

    """
    # control_type: START, STOP
    block: ControlBehavior = ControlBehavior(name="013", control_type=RobotBehaviorControlType.START)
    # response ControlBehaviorResponse
    (resultType, response) = await block.execute()

    print(f'test_control_behavior result: {response}')
    print(
        'resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_express_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_control_behavior timetout'
    assert response is not None and isinstance(response,
                                               ControlBehaviorResponse), 'test_control_behavior result unavailable'
    assert response.isSuccess, 'control_behavior failed'

async def test_control_behavior1():
    """测试控制表现力

    让机器人开始跳一个名为"dance_0004"的舞蹈，并等待回复结果

    """
    # control_type: START, STOP
    block: ControlBehavior = ControlBehavior(name="dance_0005", control_type=RobotBehaviorControlType.START)
    # response ControlBehaviorResponse
    (resultType, response) = await block.execute()

    print(f'test_control_behavior result: {response}')
    print(
        'resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_express_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_control_behavior timetout'
    assert response is not None and isinstance(response,
                                               ControlBehaviorResponse), 'test_control_behavior result unavailable'
    assert response.isSuccess, 'control_behavior failed'

# 测试, 设置嘴巴灯颜色为绿色 常亮
async def test_set_mouth_lamp():
    # mode: 嘴巴灯模式，0：普通模式，1：呼吸模式
    # color: 嘴巴灯颜色，1：红色，2：绿色，3：蓝色
    # duration: 持续时间，单位为毫秒，-1表示常亮
    # breath_duration: 闪烁一次时长，单位为毫秒


    block: SetMouthLamp = SetMouthLamp(color=MouthLampColor.GREEN, mode=MouthLampMode.NORMAL,
                                       duration=3000, breath_duration=1000)
    # response:SetMouthLampResponse
    (resultType, response) = await block.execute()

    print(f'test_set_mouth_lamp result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_set_mouth_lamp timetout'
    assert response is not None and isinstance(response, SetMouthLampResponse), 'test_set_mouth_lamp result unavailable'
    assert response.isSuccess or response.resultCode == 504, 'set_mouth_lamp failed'


# 测试,开关嘴巴灯
async def test_control_mouth_lamp():

    # is_open: True,False
    # response :ControlMouthResponse
    (resultType, response) = await ControlMouthLamp(is_open=False).execute()

    print(f'test_control_mouth_lamp result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_control_mouth_lamp timetout'
    assert response is not None and isinstance(response,
                                               ControlMouthResponse), 'test_control_mouth_lamp result unavailable'
    assert response.isSuccess or response.resultCode == 504, 'control_mouth_lamp failed'


# if __name__ == '__main__':
#     device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
#     if device:
#         asyncio.get_event_loop().run_until_complete(test_connect(device))
#         asyncio.get_event_loop().run_until_complete(test_start_run_program())
        #asyncio.get_event_loop().run_until_complete(test_play_expression())
        #asyncio.get_event_loop().run_until_complete(test_set_mouth_lamp())
        #asyncio.get_event_loop().run_until_complete(test_control_mouth_lamp())
        #asyncio.get_event_loop().run_until_complete(test_control_behavior())
        #asyncio.get_event_loop().run_until_complete(shutdown())
async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await test_start_run_program()

        #cv2.setWindowProperty("expression", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        color = (0, 0, 255)
        # cap = cv2.VideoCapture(0)
        cascade_path = root_path + "haarcascade_frontalface_alt.xml"

        last_emotion = ['netrual', 'netrual', 'netrual', 'netrual', 'netrual',
                        'netrual', 'netrual', 'netrual', 'netrual', 'netrual']
        count = 0
        start_flag = False
        flag_happy = True
        flag_happy1 = False
        flag_surprise = True
        flag_sad =True

        while True:
            sock.send(b'send')
            recv_data = b""
            start = time.clock()
            while sys.getsizeof(recv_data) < 921600:
                recv_data += sock.recv(1024*8)
            cvimage = np.frombuffer(recv_data, dtype=np.uint8)
            frame = cvimage.reshape(480, 640, 3)
            print('reveive image')

            # ret, frame = cap.read()  # 读取一帧视频
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cascade = cv2.CascadeClassifier(cascade_path)
            # 利用分类器识别出哪个区域为人脸
            faceRects = cascade.detectMultiScale(frame_gray, scaleFactor=1.1,
                                                 minNeighbors=1, minSize=(100, 100))

            if len(faceRects) > 0:
                for faceRect in faceRects:
                    x, y, w, h = faceRect
                    images = []
                    rs_sum = np.array([0.0] * num_class)
                    # 截取脸部图像提交给模型识别这是谁
                    image = frame_gray[y: y + h, x: x + w]
                    image = cv2.resize(image, (img_size, img_size))
                    image = image * (1. / 255)
                    images.append(image)
                    images.append(cv2.flip(image, 1))
                    images.append(cv2.resize(image[2:45, :], (img_size, img_size)))
                    for img in images:
                        image = img.reshape(1, img_size, img_size, 1)
                        list_of_list = model.predict_proba(image, batch_size=32, verbose=1)  # predict
                        result = [prob for lst in list_of_list for prob in lst]
                        print('result: ', result)
                        rs_sum += np.array(result)
                    print(rs_sum)
                    label = np.argmax(rs_sum)
                    emo = emo_labels[label]
                    index = count % 10
                    last_emotion[index] = emo
                    count += 1
                    #print('Emotion : ', emo)
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, '%s' % emo, (x + 30, y + 30), font, 1, (255, 0, 255), 4)
                    print(last_emotion)
                    #机器人互动
                    if start_flag:
                        if emo=='happy'and flag_happy:
                            if last_emotion.count('happy') == 10:
                                await asyncio.sleep(2)
                                await test_play_tts()
                                # 爱心expression
                                await test_play_expression()
                                await test_play_tts1()
                                # dance_0002功夫,dance_0004小星星
                                await test_control_behavior()
                                flag_happy = False
                        elif emo=='surprise'and flag_surprise:
                            if last_emotion.count('surprise') == 10:
                                await asyncio.sleep(2)
                                # action金鸡独立
                                await test_play_tts2()
                                await test_play_action()
                                flag_surprise = False

                        elif emo=='sad'and flag_sad:
                            if last_emotion.count('sad') == 7:
                                await asyncio.sleep(2)
                                await test_play_tts3()
                                flag_sad = False
                                #await asyncio.sleep(5)

                        elif emo=='happy'and flag_happy1:
                            if last_emotion.count('happy') == 10:
                                await asyncio.sleep(2)
                                await test_play_tts7()
                                flag_happy1 = False

            cv2.namedWindow("expression", cv2.WINDOW_FREERATIO)
            cv2.imshow("expression", frame)

            # 等待10毫秒看是否有按键输入
            k = cv2.waitKey(10)

            #flag
            if k & 0xFF == ord('0'):
                start_flag = True

            if k & 0xFF == ord('1'):
                flag_happy1 = True
                #flag_surprise = True
                #flag_sad = True

            # 如果输入q则退出循环
            if k & 0xFF == ord('q'):
                break


        # 释放摄像头并销毁所有窗口
        #cap.release()
        cv2.destroyAllWindows()

        await shutdown()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
