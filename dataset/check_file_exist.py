import pycantonese as pc
from pathlib import Path

dataPath = "zh-HK/clips/"

with open("zh-HK/dev.wav.txt") as file_in:
    lines = []
    for line in file_in:
        lines.append(line)
        
#print(lines)        
count = 0;        
for   i in range(len( lines )):
   tmp = lines[i];
   tmp2 = tmp.split(' ');
   tmp3 = tmp2[1].split('\n');
   filename = tmp3[0]
   #print(filename)
   #get the filename without ext.
   tmpName = filename.split('.');
   #print(tmpName)
   SaveFilename = tmpName[0];
   SaveFilename = SaveFilename + ".wav";
   my_file = Path(SaveFilename)
   if my_file.is_file():
     count = count + 1;
   else:
     print("found no file " + SaveFilename );
     
     
