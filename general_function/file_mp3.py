# -*- coding: utf-8 -*-

import os
import wave
import numpy as np
import matplotlib.pyplot as plt  
import math
import time

from pydub import AudioSegment
from pathlib import Path


def mp3ToWav(filename):
    
  #my_file = Path(filename)
  #check if the .wav file already there first.
  tmpName = filename.split('.');
  SaveFilename = tmpName[0];
  SaveFilename = SaveFilename + ".wav";
  my_file = Path(SaveFilename)
  
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
      sound = AudioSegment.from_mp3(filename)
      #sound = am.from_file(filepath, format='wav', frame_rate=22050)
      sound = sound.set_frame_rate(16000)
      sound.export(SaveFilename, format="wav")
      return SaveFilename
    
  else:
    print("mp3 file not exists, please check filepath \n");
    print(filename);
    return None;
  
   

