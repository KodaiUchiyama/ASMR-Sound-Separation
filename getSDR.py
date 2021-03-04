import numpy as np
import os, glob
from scipy.spatial.distance import euclidean
#from fastdtw import fastdtw
from matplotlib import pyplot as plt
#import librosa
#import librosa.display # この行が必要
#順序つき辞書
from collections import OrderedDict
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from scipy.io import wavfile
from pesq import pesq
import mir_eval

truesound_file = "/home/kody.uchiyama/speech_separation-master/data/audio/norm_audio_train/"
# trim_audio_train0-50.wav 
predicted_file = './predict_testdata_exp1/' 
#predicted_file = './predict_testdata_AO/' 
# 1-111_00091_1-111.wav
pesq_list = []

#result_file = 'result_score_mse.txt'
count = 0
##予測された音声とテスト音声を一つずつ取得
for predicted_path in glob.glob(predicted_file+"*.wav"):
    #predicted側index抽出
    predicted_id = predicted_path.rsplit('_',1)[1].replace('.wav','') #1-16
    
    #正解音声を取得 16kHz
    rate, ref = wavfile.read(truesound_file + "trim_audio_train" + predicted_id + ".wav")
    #予測した音声を取得 16kHz
    rate, deg = wavfile.read(predicted_path)
    #print(rate)
    #print(ref.shape)
    #print(deg.shape)
    #output_metrics = pesq(rate, ref, deg, 'wb')
    output_metrics = mir_eval.separation.bss_eval_sources(ref, deg)
    # (sdr, sir, sar, perm)  
    # PESQ計算
    #print("Separation Metrics:"+ predicted_id+": "+ str(output_metrics))
    #print(output_metrics[0][0]) #SDR
    pesq_list.append(output_metrics[0][0])
    count = count + 1 
    if count%500 == 0:
        print(count)
print("List length:"+str(len(pesq_list)))
pesq_list = np.array(pesq_list)
#print(pesq_list)
print("Average of SDR:"+str(np.mean(pesq_list)))
