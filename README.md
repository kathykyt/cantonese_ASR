# cantonese_ASR

This project is a modified version of ASR for Chinese, https://github.com/CynthiaSuwi/ASR-for-Chinese-Pipeline, however, that project is mainly for madarin, in this project, we try to use this pipeline and choose the dataset to be from mozilla's common voice Hong Kong cantonese dataset (https://commonvoice.mozilla.org/en/datasets , zh-HK_100h_2020-12-11), and based on the corpus information from pycantonese (https://pycantonese.org/searches.html). The training is based on cantonese corpus and dataset. 


Please follow the following to setup and try your training or test
===================================================================
1. Setup:

   System: Ubuntu 20.04

   python3.6: install python3.6 by typing "sudo apt-get install python3.6" 
   
2. clone the source code by "git clone https://github.com/kathykyt/cantonese_ASR.git"

3. Create a virtual python environment: "cd catonese_ASR" , run "virtualenv -p /usr/bin/python3.6 venv"

4. setup python virtual environment: "source venvbin/activate" 

6. Install required packages: "pip install -r requirements.txt" 

5. Visit https://commonvoice.mozilla.org/en/datasets and select the download the cantonese dataset file, zh-HK_100h_2020-12-11 to download, the file is zh-HK.tar.gz. copy it under the directory, cantonest_ASR/dataset/
by "cp zh-HK.tar.gz {your top diretory}/cantonest_ASR/dataset/ "

6. extract the file by "tar xvf zh-HK.tar.gz"

7. Prepare the wave file for training and testing. Since the commonvoice data is mp3, we have to convert them to .wav files. To convert it, under cantonest_ASR/dataset/ run "./convert_to_mp3.py ", after that run "./convert_to_mp3_test.py". 

8. 
