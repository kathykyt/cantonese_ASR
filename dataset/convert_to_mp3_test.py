import os
import wave
import numpy as np
import matplotlib.pyplot as plt  
import math
import time

from pydub import AudioSegment
from pathlib import Path



dataPath = "zh-HK/clips/"
sourcePath = "cv-corpus-6.1-2020-12-11/"

def mp3ToWav(filename):
    
  my_file = Path(sourcePath + filename)
  if my_file.is_file():
    # file exists
    
    #get the filename without ext.
    tmpName = filename.split('.');
    #print(tmpName)
    SaveFilename = tmpName[0];
    SaveFilename = SaveFilename + ".wav";
   
    #check if the wav file already exists
    # if not convert it.
    my_file_wav = Path(SaveFilename)
    if my_file_wav.is_file():
      
      return SaveFilename;
    else:  
      filename2 = sourcePath + filename;
      sound = AudioSegment.from_mp3(filename2)
      #sound = am.from_file(filepath, format='wav', frame_rate=22050)
      sound = sound.set_frame_rate(16000)
      sound.export(SaveFilename, format="wav")
      return SaveFilename
    
  else:
    print("mp3 file not exists, please check filepath \n");
    print(filename);
    return None;
  
   




with open("zh-HK/test.wav.txt") as file_in:
    lines = []
    for line in file_in:
        lines.append(line)
        
table_list = [];
for j in range(len(lines)):
   tmptuple = lines[j].split()
   table_list.append(tmptuple[1])


file_name_list = table_list

#print(file_name_list)

for j in range(len(file_name_list)):
   filename = file_name_list[j];
   print(filename + "\n");
   mp3ToWav(filename);
   
   
print("===convertion completed ==");


   




