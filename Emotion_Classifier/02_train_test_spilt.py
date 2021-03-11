#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# 将一个文件夹下图片按比例分在三个文件夹下
import os
import random
import shutil
from shutil import copy2

curr_dirname = '/home/admin1/Projects/02_Emotion_Classifier/emotion_data/raw_data/' 
print('Choose from these folders:', os.listdir(curr_dirname))

emotion_name = input('Enter the emotion name to split: ')
raw_data_dir = '/home/admin1/Projects/02_Emotion_Classifier/emotion_data/raw_data/'+str(emotion_name)+'/' # 原始图片路径

all_data = os.listdir(raw_data_dir) # 返回原始图片文件夹中文件名称列表
num_all_data = len(all_data) # 原始文件夹中图片数量
print( "num_all_data: " + str(num_all_data) )
index_list = list(range(num_all_data))
#print(index_list)
random.shuffle(index_list)
num = 0

trainDir = '/home/admin1/Projects/02_Emotion_Classifier/emotion_data/after_split/train/' + str(emotion_name) + '/' #（将训练集放在这个文件夹下）
if not os.path.exists(trainDir):
    os.makedirs(trainDir)
        
validDir = '/home/admin1/Projects/02_Emotion_Classifier/emotion_data/after_split/val/' + str(emotion_name) + '/'#（将验证集放在这个文件夹下）
if not os.path.exists(validDir):
    os.makedirs(validDir)
        
testDir = '/home/admin1/Projects/02_Emotion_Classifier/emotion_data/after_split/test/' + str(emotion_name) + '/' #（将测试集放在这个文件夹下）        
if not os.path.exists(testDir):
    os.makedirs(testDir)
        
for i in index_list:
    fileName = os.path.join(raw_data_dir, all_data[i])
    if num < num_all_data*0.8:
        #print(str(fileName))
        copy2(fileName, trainDir)
    elif num>num_all_data*0.8 and num < num_all_data*0.9:
        #print(str(fileName))
        copy2(fileName, validDir)
    else:
        copy2(fileName, testDir)
    num += 1
print('All done!')
