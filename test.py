#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nl8590687
用于测试整个一套语音识别系统的程序
语音模型 + 语言模型
"""
import platform as plat

from SpeechModel251 import ModelSpeech
#from LanguageModel2 import ModelLanguage
from LanguageModel3 import ModelLanguage
#from LanguageModel import ModelLanguage
from keras import backend as K

datapath = ''
modelpath = 'model_speech'

system_type = plat.system() # 由于不同的系统的文件路径表示不一样，需要进行判断
if(system_type == 'Windows'):
	datapath = 'D:\\语音数据集'
	modelpath = modelpath + '\\'
elif(system_type == 'Linux'):
	#datapath = 'dataset'
	datapath = './'
	modelpath = modelpath + '/'
else:
	print('*[Message] Unknown System\n')
	datapath = 'dataset'
	modelpath = modelpath + '/'

ms = ModelSpeech(datapath)

#ms.LoadModel(modelpath + 'm251_20210419/speech_model251_e_0_step_39500.model')
#ms.LoadModel(modelpath + 'm251_20210425/speech_model251_e_0_step_20000.model')
ms.LoadModel(modelpath + 'm251_20210813/speech_model251_e_0_step_41000.model')

#ms.TestModel(datapath, str_dataset='test', data_count = 64, out_report = True)

#r = ms.RecognizeSpeech_FromFile('/opt/git/ASRT_SpeechRecognition/ASR_cantonese/dataset/zh-HK/clips/common_voice_zh-HK_23385878.wav')
#r = ms.RecognizeSpeech_FromFile('/opt/git/ASRT_SpeechRecognition/ASR_cantonese/try/006.wav')
#r = ms.RecognizeSpeech_FromFile('/opt/git/cantonest_ASR/test/common_voice_zh-HK_24020802.wav')
r = ms.RecognizeSpeech_FromFile('/opt/git/cantonest_ASR/test/common_voice_zh-HK_23734008.wav')


K.clear_session()

print('*[提示] 语音识别结果：\n',r)


ml = ModelLanguage('model_language')
ml.LoadModel()

#str_pinyin = ['zhe4','zhen1','shi4','ji2', 'hao3','de5']
#str_pinyin = ['jin1', 'tian1', 'shi4', 'xing1', 'qi1', 'san1']
#str_pinyin = ['ni3', 'hao3','a1']
str_pinyin = r
#str_pinyin =  ['su1', 'bei3', 'jun1', 'de5', 'yi4','xie1', 'ai4', 'guo2', 'jiang4', 'shi4', 'ma3', 'zhan4', 'shan1', 'ming2', 'yi1', 'dong4', 'ta1', 'ju4', 'su1', 'bi3', 'ai4', 'dan4', 'tian2','mei2', 'bai3', 'ye3', 'fei1', 'qi3', 'kan4', 'zhan4']
r = ml.SpeechToText(str_pinyin)
print('语音转文字结果：\n',r)














