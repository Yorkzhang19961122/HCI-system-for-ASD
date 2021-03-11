import keras
from keras.layers import Dense, Dropout, Activation, Flatten,Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
from keras.optimizers import SGD
import matplotlib.pyplot as plt
batch_size = 16
num_classes = 3
nb_epoch = 1
img_size = 100
root_path='/home/admin1/Projects/02_Emotion_Classifier/emotion_data/after_split'

class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch':[], 'epoch':[]}
        self.accuracy = {'batch':[], 'epoch':[]}
        self.val_loss = {'batch':[], 'epoch':[]}
        self.val_acc = {'batch':[], 'epoch':[]}

    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))

    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))

    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        if loss_type == 'epoch':
            # val_acc
            plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
            # val_loss
            plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')
        plt.legend(loc="upper right")
        plt.show()

class Model:
    def __init__(self):
        self.model = None

    def build_model(self):
        self.model = Sequential()

        #self.model.add(Conv2D(32, (1, 1), strides=1, padding='same', input_shape=(img_size, img_size, 1)))
        #self.model.add(Activation('relu'))
        #self.model.add(Conv2D(32, (5, 5), padding='same'))
        #self.model.add(Activation('relu'))
        #self.model.add(MaxPooling2D(pool_size=(2, 2)))

        #self.model.add(Conv2D(32, (3, 3), padding='same'))
        #self.model.add(Activation('relu'))
        #self.model.add(MaxPooling2D(pool_size=(2, 2)))

        #self.model.add(Conv2D(64, (5, 5), padding='same'))
        #self.model.add(Activation('relu'))
        #self.model.add(MaxPooling2D(pool_size=(2, 2)))

        #self.model.add(Flatten())
        #self.model.add(Dense(2048))
        #self.model.add(Activation('relu'))
        #self.model.add(Dropout(0.5))
        #self.model.add(Dense(1024))
        #self.model.add(Activation('relu'))
        #self.model.add(Dropout(0.5))
        #self.model.add(Dense(num_classes))
        #self.model.add(Activation('softmax'))
        #self.model.summary()
# ----------------------------------------------------------------------------------------------------------
        self.model.add(Conv2D(32, (2, 2), strides=1, padding='same', input_shape=(img_size, img_size, 1)))
        self.model.add(Activation('relu'))
        self.model.add(Conv2D(32, (7, 7), padding='same'))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(32, (4, 4), padding='same'))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(64, (5, 5), padding='same'))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(2048))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1024))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(num_classes))
        self.model.add(Activation('softmax'))
        self.model.summary()
# --------------------------------------------------------------------------------------
    def train_model(self):
        # SGD优化算法
        sgd=SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy',
                optimizer=sgd,
                #optimizer='rmsprop',
                metrics=['accuracy'])
        #自动扩充训练样本
        train_datagen = ImageDataGenerator(
        rescale = 1./255, # 归一化训练集，像素值缩放到0-1之间
        shear_range = 0.2, #错切变换
        zoom_range = 0.2, #放大图片
        horizontal_flip=True) # 随机水平翻转
        #归一化验证集
        val_datagen = ImageDataGenerator(
                rescale = 1./255)
        eval_datagen = ImageDataGenerator(
                rescale = 1./255)
        #以文件分类名划分label
        train_generator = train_datagen.flow_from_directory(
                root_path+'/train',
                target_size=(img_size,img_size), # 图像将被resize为该尺寸
                color_mode='grayscale', # 单通道灰度图
                batch_size=batch_size,
                class_mode='categorical') # 返回的one-hot编码后的label
        val_generator = val_datagen.flow_from_directory(
                root_path+'/val',
                target_size=(img_size,img_size),
                color_mode='grayscale',
                batch_size=batch_size,
                class_mode='categorical')
        eval_generator = eval_datagen.flow_from_directory(
                root_path+'/test',
                target_size=(img_size,img_size),
                color_mode='grayscale',
                batch_size=batch_size,
                class_mode='categorical')
        labels = (train_generator.class_indices)
        print('labels:', labels)
        history = LossHistory()
        # early_stopping = EarlyStopping(monitor='loss',patience=3) # 3个epoch内loss没有improvement,则stop
        history_fit=self.model.fit_generator(
                train_generator,
                steps_per_epoch=50/(batch_size/32), # 600 ,将一个epoch分成多少个batch_size
                nb_epoch=nb_epoch,
                validation_data=val_generator,
                validation_steps=8, # 当前epoch结束后进行验证
                callbacks=[history]
                )

        history_predict=self.model.predict_generator(
                eval_generator,
                steps=20)
        history.loss_plot('epoch')


        with open(root_path + '/model' + '/model_fit_log','w') as f:
            f.write(str(history_fit.history))
        with open(root_path + '/model' + '/model_predict_log','w') as f:
            f.write(str(history_predict))
#         print("%s: %.2f%%" % (self.model.metrics_names[1], history_eval[1] * 100))
    def save_model(self):
        model_json=self.model.to_json()
        with open(root_path + '/model' + '/model_json.json', 'w') as json_file:
            json_file.write(model_json)
        self.model.save_weights(root_path + '/model' + '/model_weight.h5')
        self.model.save(root_path + '/model' + '/model.h5')

if __name__=='__main__':
    model=Model()
    model.build_model()
    print('model built')
    model.train_model()
    print('model trained')
    model.save_model()
    print('model saved')
