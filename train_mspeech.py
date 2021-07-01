#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nl8590687
用于训练语音识别系统语音模型的程序

"""
import platform as plat
import os

import tensorflow as tf

#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()

#windfat hack
#tf.enable_eager_execution() # 关键

from keras.backend.tensorflow_backend import set_session


from SpeechModel251 import ModelSpeech, ModelName
#from SpeechModel261 import ModelSpeech, ModelName

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
#进行配置，使用95%的GPU
#config = tf.compat.v1.ConfigProto()
config = tf.ConfigProto()
#config.gpu_options.per_process_gpu_memory_fraction = 0.95
config.gpu_options.per_process_gpu_memory_fraction = 0.8
#gpus = tf.config.experimental.list_physical_devices('GPU')
#tf.config.experimental.set_memory_growth(gpus[0], True)
#config.gpu_options.allow_growth=True


#windfat hack
#tf.compat.v1.keras.backend.clear_session()

#config.gpu_options.allow_growth=True   #不全部占满显存, 按需分配
#sess = tf.compat.v1.Session(config=config)
#tf.compat.v1.keras.backend.set_session(sess)


datapath = ''
modelpath = 'model_speech'


if(not os.path.exists(modelpath)): # 判断保存模型的目录是否存在
	os.makedirs(modelpath) # 如果不存在，就新建一个，避免之后保存模型的时候炸掉
	os.makedirs(modelpath + '/m' + ModelName)

system_type = plat.system() # 由于不同的系统的文件路径表示不一样，需要进行判断
if(system_type == 'Windows'):
	datapath = 'D:\\SpeechData'
	modelpath = modelpath + '\\'
elif(system_type == 'Linux'):
	datapath = 'dataset'
	modelpath = modelpath + '/'
else:
	print('*[Message] Unknown System\n')
	datapath = 'dataset'
	modelpath = modelpath + '/'

ms = ModelSpeech(datapath)

#ms.LoadModel(modelpath + 'speech_model251_e_0_step_327500.model')
#ms.LoadModel(modelpath + 'm251_backup/speech_model251_e_0_step_12000.model')
#ms.LoadModel(modelpath + 'm251_20210222/speech_model251_e_0_step_14500.model')
#ms.LoadModel(modelpath + 'm251_20210226/speech_model251_e_0_step_17500.model')
#ms.LoadModel(modelpath + 'm251_20210226/speech_model251_e_0_step_18000.model')
#ms.LoadModel(modelpath + 'm251_20210301/speech_model251_e_0_step_5500.model')
#ms.LoadModel(modelpath + 'm251_20210308/speech_model251_e_0_step_10000.model')
ms.LoadModel(modelpath + 'm251_20210407/speech_model251_e_0_step_44000.model')

#ms.TrainModel(datapath, epoch = 50, batch_size = 16, save_step = 500)
#ms.TrainModel(datapath, epoch = 50, batch_size = 16, save_step = 5)
ms.TrainModel(datapath, epoch = 50, batch_size = 8, save_step = 500)
#ms.TrainModel(datapath, epoch = 50, batch_size = 16, save_step = 500)


