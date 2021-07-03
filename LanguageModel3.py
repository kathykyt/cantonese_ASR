#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nl8590687
语音识别的语言模型

基于马尔可夫模型的语言模型

"""
import platform as plat



initial_table = ["b", "c","d", "f", "g", "gw", "h", "j", "k", "kw", "l", "m", "n", "ng", "p", "s", "t", "w", "z"];

final_table = ["aa", "aai", "aau", "aam", "aan", "aang", "aap", "aat", "aak"];

def getSyllableForAllTones(Insyllable):

   All_list = [];

   if (Insyllable == None):
     return [0, " "];
     
   tmpstr = Insyllable;
   tmptmpstr = "";
   NumOfSyllable = 0;
   lastCharIndex = len(tmpstr);
   
   prefix_syllable = tmpstr[:(lastCharIndex - 1)];
   
   #print(prefix_syllable);
   
   for i in range (10) :
      tmptmpstr = prefix_syllable + str(i)
      #print(tmptmpstr);
      if (i != 0):
        All_list.append(tmptmpstr)
        
        
   #print(All_list)
    
   return All_list

class ModelLanguage(): # 语音模型类
	def __init__(self, modelpath):
		self.modelpath = modelpath
		system_type = plat.system() # 由于不同的系统的文件路径表示不一样，需要进行判断
		
		self.slash = ''
		if(system_type == 'Windows'):
			self.slash = '\\'
		elif(system_type == 'Linux'):
			self.slash = '/'
		else:
			print('*[Message] Unknown System\n')
			self.slash = '/'
		
		if(self.slash != self.modelpath[-1]): # 在目录路径末尾增加斜杠
			self.modelpath = self.modelpath + self.slash
		
		pass
		
	def LoadModel(self):
		self.dict_pinyin = self.GetSymbolDict('dict.txt')
		self.model1 = self.GetLanguageModel(self.modelpath + 'language_model1.txt')
		self.model2 = self.GetLanguageModel(self.modelpath + 'language_model2.txt')
		self.pinyin = self.GetPinyin(self.modelpath + 'dic_pinyin.txt')
		model = (self.dict_pinyin, self.model1, self.model2 )
		return model
		pass
	
	def SpeechToText(self, list_syllable):
		'''
		为语音识别专用的处理函数
		实现从语音拼音符号到最终文本的转换
		'''
		r=''
		length = len(list_syllable)
		if(length == 0): # 传入的参数没有包含任何拼音时
			return ''
		
		# 先取出一个字，即拼音列表中第一个字
		str_tmp = [list_syllable[0]]
		
		processing_word = 0;
		
		for i in range(0, length - 1):
			# 依次从第一个字开始每次连续取两个字拼音
			str_split = list_syllable[i] + ' ' + list_syllable[i+1]
			#print(str_split,str_tmp,r)
			# 如果这个拼音在汉语拼音状态转移字典里的话
			#if(str_split in self.pinyin):
			check_again_match = 0;
			if (processing_word == 0):
				matching1 = [s for s in self.pinyin if str_split in s]
				#print(len(matching1))
				if ((matching1 != None) and (len(matching1) == 1) ):
					#print("matching1:")
					#print(matching1);
				#if (str_split in self.pinyin):
					# 将第二个字的拼音加入
					tmp_split = matching1[0].split(' ');
					NumOfword = len(tmp_split);
					for hh in range(len(tmp_split) - 2):
						#str_tmp.append(list_syllable[i+1]);
						str_tmp.append(tmp_split[hh + 1]);
					processing_word = NumOfword - 2;
				else:
					#check_again_match = 0;
					#check if we have any combination of different tones of words can match the dict list
					firstSyllableList = getSyllableForAllTones(list_syllable[i])
					secondSyllableList = getSyllableForAllTones(list_syllable[i + 1])
					scores = [];
					firstSyllableSelected = 0;
					SecondSyllableSelected = 0;
				
					for k in range( len(firstSyllableList)):
						for j in range(len(secondSyllableList)):
							matching = None;
							str_split = firstSyllableList[k] + ' ' + secondSyllableList[j];
							#print(str_split)
							matching = [s for s in self.pinyin if str_split in s]
							if ((matching != None) and (len(matching) >= 1)):
								print(matching);
				        			#need to check if the first 2 word matches to the matching strings.
								for  ll in range(len(matching)):
									xxx = matching[ll].split(' ');
									#print(len(xxx))
									if  ((firstSyllableList[k] == xxx[0]) and (secondSyllableList[j] == xxx[1])):
										if ((len(xxx) - 1 <= 2) and ((list_syllable[i] == xxx[0]) or (list_syllable[i + 1] == xxx[1]))):
				                    					print(matching[ll])
				                    					check_again_match = 0;
				                    					str_tmp[len(str_tmp) - 1] = xxx[0];
				                    					str_tmp.append(xxx[1]);
				                    					#list_syllable[i + 1] = xxx[1];
				                    					processing_word = 1;
										elif ((len(xxx) - 1 == 3) and ((i + 2) <  length)):
				                
											#only compare the syllable without tone.
											thirdword = list_syllable[i + 2];
											tmpxxx = xxx[2];
											if (thirdword[:(len(thirdword) - 1)] == tmpxxx[:(len(tmpxxx) - 1)] ):
												#print(matching[ll])
												str_tmp[len(str_tmp) - 1] = xxx[0];
												str_tmp.append(xxx[1]);
												str_tmp.append(xxx[2]);
												list_syllable[i + 1] = xxx[1];
												list_syllable[i + 2] = xxx[2];
												processing_word = 2;

										elif ((len(xxx) - 1 == 4) and ((i + 3) <  length)):  
											#compare the syllable without tone.
											forthword = list_syllable[i + 3];
											tmpxxx = xxx[3];
											if (forthword[:(len(forthword) - 1)] == tmpxxx[:(len(tmpxxx) - 1)] ):
												print(matching[ll])
				                   
				
				if (check_again_match == 0 ):
				    		# 否则不加入，然后直接将现有的拼音序列进行解码
				    		str_decode = self.decode(str_tmp, 0.0000)
				    		#print('decode ',str_tmp,str_decode)
				    		if(str_decode != []):
					    		r += str_decode[0][0]
				    			# 再重新从i+1开始作为第一个拼音
				    			str_tmp = [list_syllable[i+1]]
			
			else:
				processing_word = processing_word - 1;    	
				str_tmp = [list_syllable[i+1]];
		
		#print('最后：', str_tmp)
		if processing_word == 0:
			str_decode = self.decode(str_tmp, 0.0000)
		
			#print('剩余解码：',str_decode)
		
			if(str_decode != []):
				r += str_decode[0][0]
		
		return r
	
	def decode(self,list_syllable, yuzhi = 0.0001):
		'''
		实现拼音向文本的转换
		基于马尔可夫链
		'''
		#assert self.dic_pinyin == null or self.model1 == null or self.model2 == null
		list_words = []
		
		num_pinyin = len(list_syllable)
		
		#print('decode function: list_syllable\n',list_syllable)
		#print(num_pinyin)
		# 开始语音解码
		for i in range(num_pinyin):
			#print(i)
			ls = ''
			if(list_syllable[i] in self.dict_pinyin): # 如果这个拼音在汉语拼音字典里的话
				# 获取拼音下属的字的列表，ls包含了该拼音对应的所有的字
				ls = self.dict_pinyin[list_syllable[i]]
			else:
				break
			
			
			if(i == 0):
				# 第一个字做初始处理
				num_ls = len(ls)
				for j in range(num_ls):
					tuple_word = ['',0.0]
					# 设置马尔科夫模型初始状态值
					# 设置初始概率，置为1.0
					tuple_word = [ls[j], 1.0]
					if (ls[j] in self.model1):
						#print(self.model1[ls[j]])
						tuple_word[1]  = tuple_word[1] *float(self.model1[ls[j]])
					
					# 添加到可能的句子列表
					list_words.append(tuple_word)
				
				#print(list_words)
				continue
			else:
				# 开始处理紧跟在第一个字后面的字
				if i == 2:
				   continue
				   
				#print(i)
				list_words_2 = []
				num_ls_word = len(list_words)
				#print('ls_wd: ',list_words)
				for j in range(0, num_ls_word):
					
					num_ls = len(ls)
					for k in range(0, num_ls):
						tuple_word = ['',0.0]
						tuple_word = list(list_words[j]) # 把现有的每一条短语取出来
						#print('tw1: ',tuple_word)
						tuple_word[0] = tuple_word[0] + ls[k] # 尝试按照下一个音可能对应的全部的字进行组合
						#print('ls[k]  ',ls[k])
						
						#if there is a 3 words, extract all possible words
						if ((num_pinyin == 3) and (i == 1)):
							lss = self.dict_pinyin[list_syllable[i + 1]]
							num_lss = len(lss);
							for m in range(0, num_lss):
								tuple_word_tmp = tuple_word[0] + lss[m]
								#print(tuple_word[0][-3:])
								tmp_words = tuple_word_tmp[-3:]
								#print('tmp_words: ',tmp_words,tmp_words in self.model2)
								if(tmp_words in self.model2): # 判断它们是不是再状态转移表里
									tuple_word[0] = tuple_word_tmp;
									#print(tmp_words,tmp_words in self.model2)
									
									#print(float(self.model2[tmp_words]))
									#print(float(self.model1[tmp_words[-2]]))
									tuple_word[1] = 1.0
									tuple_word[1] = tuple_word[1] * float(self.model2[tmp_words]) / float(self.model1[tmp_words[-2]])
									# 核心！在当前概率上乘转移概率，公式化简后为第n-1和n个字出现的次数除以第n-1个字出现的次数
									#print(self.model2[tmp_words],self.model1[tmp_words[-2]])
									#print(tuple_word[1])
								else:
									tuple_word[1] = 0.0
									#print("zero")False
									continue
									
								if(tuple_word[1] >= pow(yuzhi, i)):
									# 大于阈值之后保留，否则丢弃
									#print(tuple_word)
									list_words_2.append(tuple_word)	
								
						else:		
							tmp_words = tuple_word[0][-2:] # 取出用于计算的最后两个字
							#print('tmp_words: ',tmp_words,tmp_words in self.model2)
							if(tmp_words in self.model2): # 判断它们是不是再状态转移表里
								#print(tmp_words,tmp_words in self.model2)
								tuple_word[1] = tuple_word[1] * float(self.model2[tmp_words]) / float(self.model1[tmp_words[-2]])
								# 核心！在当前概率上乘转移概率，公式化简后为第n-1和n个字出现的次数除以第n-1个字出现的次数
								#print(self.model2[tmp_words],self.model1[tmp_words[-2]])
							else:
								tuple_word[1] = 0.0
								continue
								
							#print('tw2: ',tuple_word)
							#print(tuple_word[1] >= pow(yuzhi, i))
							if(tuple_word[1] >= pow(yuzhi, i)):
								# 大于阈值之后保留，否则丢弃
								#print(tuple_word)
								list_words_2.append(tuple_word)
						
				list_words = list_words_2
				#print(list_words,'\n')
		#print(list_words)
		for i in range(0, len(list_words)):
			for j in range(i + 1, len(list_words)):
				if(list_words[i][1] < list_words[j][1]):
					tmp = list_words[i]
					list_words[i] = list_words[j]
					list_words[j] = tmp
		
		return list_words
		pass
		
	def GetSymbolDict(self, dictfilename):
		'''
		读取拼音汉字的字典文件
		返回读取后的字典
		'''
		txt_obj = open(dictfilename, 'r', encoding='UTF-8') # 打开文件并读入
		txt_text = txt_obj.read()
		txt_obj.close()
		txt_lines = txt_text.split('\n') # 文本分割
		
		dic_symbol = {} # 初始化符号字典
		for i in txt_lines:
			list_symbol=[] # 初始化符号列表
			if(i!=''):
				txt_l=i.split('\t')
				pinyin = txt_l[0]
				for word in txt_l[1]:
					list_symbol.append(word)
			dic_symbol[pinyin] = list_symbol
		
		return dic_symbol
		
	def GetLanguageModel(self, modelLanFilename):
		'''
		读取语言模型的文件
		返回读取后的模型
		'''
		txt_obj = open(modelLanFilename, 'r', encoding='UTF-8') # 打开文件并读入
		txt_text = txt_obj.read()
		txt_obj.close()
		txt_lines = txt_text.split('\n') # 文本分割
		
		dic_model = {} # 初始化符号字典
		for i in txt_lines:
			if(i!=''):
				txt_l=i.split('\t')
				if(len(txt_l) == 1):
					continue
				#print(txt_l)
				dic_model[txt_l[0]] = txt_l[1]
				
		return dic_model
	
	def GetPinyin(self, filename):
		file_obj = open(filename,'r',encoding='UTF-8')
		txt_all = file_obj.read()
		file_obj.close()
	
		txt_lines = txt_all.split('\n')
		dic={}
	
		for line in txt_lines:
			if(line == ''):
				continue
			pinyin_split = line.split('\t')
			
			list_pinyin=pinyin_split[0]
			
			if(list_pinyin not in dic and int(pinyin_split[1]) > 1):
				dic[list_pinyin] = pinyin_split[1]
		return dic


if(__name__=='__main__'):
	
	ml = ModelLanguage('model_language')
	ml.LoadModel()
	
	#str_pinyin = ['zhe4','zhen1','shi4','ji2', 'hao3','de5']
	#str_pinyin = ['jin1', 'tian1', 'shi4', 'xing1', 'qi1', 'san1']
	#str_pinyin = ['ni3', 'hao3','a1']
	#str_pinyin = ['wo3','dui4','shi4','mei2','cuo4','ni3','hao3']
	#str_pinyin = ['wo3','dui4','shi4','tian1','mei2','na5','li3','hai4']
	#str_pinyin = ['ba3','zhe4','xie1','zuo4','wan2','wo3','jiu4','qu4','shui4','jiao4']
	#str_pinyin = ['wo3','qu4','a4','mei2','shi4','er2','la1']
	#str_pinyin = ['wo3', 'men5', 'qun2', 'li3', 'xiong1', 'di4', 'jian4', 'mei4', 'dou1', 'zai4', 'shuo1']
	#str_pinyin = ['su1', 'an1', 'ni3', 'sui4', 'li4', 'yun4', 'sui2', 'cong2', 'jiao4', 'ming2', 'tao2', 'qi3', 'yu2', 'peng2', 'ya4', 'yang4', 'chao1', 'dao3', 'jiang1', 'li3', 'yuan2', 'kang1', 'zhua1', 'zou3']
	#str_pinyin = ['da4', 'jia1', 'hao3']
	str_pinyin = ['kao3', 'yan2', 'yan1', 'yu3', 'ci2', 'hui4']
	#r = ml.decode(str_pinyin)
	r=ml.SpeechToText(str_pinyin)
	print('语音转文字结果：\n',r)

