
import pycantonese as pc

dataPath = "zh-HK/clips/"

with open("../dataset/cv-corpus-6.1-2020-12-11/zh-HK/other.tsv") as file_in:
    lines = []
    for line in file_in:
        lines.append(line)
        

#print(lines)

table_list = [];
for j in range(len(lines)):
  table_list.append(lines[j].split());

clip_name_list = table_list

#print(clip_name_list)

formated_list = [];

#print(clip_name_list[0]);

for i in range(len(clip_name_list)):

    tmptmplist = [];
    #print(clip_name_list[i]);
    tmp_list = clip_name_list[i][1].split(".");
    tmptmplist.append(tmp_list[0]);
    tmptmplist.append(clip_name_list[i][1]);
    tmptmplist.append(clip_name_list[i][2]);
    tmpStr = clip_name_list[i][2];
    outStr = "";
    for jj in range(len(tmpStr)):
       cchar = tmpStr[jj];
       #print(cchar)
       result = pc.characters_to_jyutping(cchar);
       #print(result[0][1])
       #print(type(result[0][1]))
       if ( type(result[0][1]) != type(None) ):
          outStr = outStr + result[0][1] + " ";
          
    #print(outStr);
    tmptmplist.append(outStr);

    formated_list.append(tmptmplist);
    

#print(formated_list);

waveList = "";
syllableList = "";
AllDataList = "";

for i in range(len(formated_list)):
  syllableList = syllableList + formated_list[i][0] + " " + formated_list[i][3] + "\n";
  filePath = dataPath + formated_list[i][1]
  waveList = waveList + formated_list[i][0] + " " + filePath + "\n";
  AllDataList = AllDataList + formated_list[i][1] + " " + formated_list[i][2] + " " + formated_list[i][3] + "\n"
  
#print(syllableList);
#print(waveList);
#print(AllDataList);

text_file = open("test.wav.txt", "w")
n = text_file.write(waveList)
text_file.close()

text_file = open("test.syllable.txt", "w")
n = text_file.write(syllableList)
text_file.close()

#text_file = open("all.txt", "w")
#n = text_file.write(AllDataList)
#text_file.close()



