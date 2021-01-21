import sys
sys.path.append ('./model/model')
sys.path.append ('./model/utils')
from keras.models import load_model
#from option import ModelMGPU
import os
import scipy.io.wavfile as wavfile
import numpy as np
import utils
import tensorflow as tf



#parameters
people = 2
num_gpu=1

#path
model_path = './saved_AV_models/AVmodel-1p-001-0.29544.h5'
#model_path = './saved_AV_models/AVmodel-1p-003-0.25622.h5'
result_path = './predict_testdata/'
os.makedirs(result_path,exist_ok=True)

database = './data/AV_model_database/mix/'
face_emb_path = '/home/kody.uchiyama/speech_separation-master/data/video/face1022_emb/'

print('Initialing Parameters......')

#loading data
print('Loading data ......')
test_file = []
with open('./data/AV_log/AVdataset_test.txt','r') as f:
    test_file = f.readlines()


def get_data_name(line,people=people,database=database,face_emb_path=face_emb_path):
    parts = line.split() # get each name of file for one testset
    # mix_17-145_00091.npy crm_17-145_00091_17-145.npy 17-145_face_emb.npy
    mix_str = parts[0]
    name_list = mix_str.replace('.npy','')
    name_list = name_list.replace('mix_','')
    names = name_list.split('_')
    single_idxs = [] # 17-145, 00091
    for i in range(2):
        single_idxs.append(names[i])
    file_path1 = database + mix_str
    file_path2 = face_emb_path + parts[2]
    mix = np.load(file_path1)
    face_emb = np.load(file_path2)
    #face_emb_ex = np.zeros((1,75,1,1792,1))
    #face_emb_ex[1,:,:,:,1] = face_emb
    #for i in range(1):
    #    face_emb_ex[1,:,:,:,i] = face_emb

    return mix,single_idxs,face_emb

#result predict
av_model = load_model(model_path,custom_objects={'tf':tf})
if num_gpu>1:
    parallel = ModelMGPU(av_model,num_gpu)
    for line in test_file:
        mix,single_idxs,face_emb = get_data_name(line,people,database,face_emb)
        mix_ex = np.expand_dims(mix,axis=0)
        cRMs = parallel.predict([mix_ex,face_emb])
        cRMs = cRMs[0]
        prefix =''
        for idx in single_idxs:
            prefix +=idx+'-'
        for i in range(len(cRMs)):
            cRM =cRMs[:,:,:,i]
            assert cRM.shape ==(298,257,2)
            F = utils.fast_icRM(mix,cRM)
            T = utils.fase_istft(F,power=False)
            filename = result_path+str(single_idxs[i])+'.wav'
            wavfile.write(filename,16000,T)

count = 0
if num_gpu<=1:
    for line in test_file:
        mix,single_idxs,face_emb = get_data_name(line,people,database,face_emb_path)
        # print(mix.shape) # (298, 257, 2)
        # print(face_emb.shape) # (75, 1, 1792)
        mix_ex = np.expand_dims(mix,axis=0)
        face_emb_ex = np.expand_dims(face_emb,axis=0)
        face_emb_ex = np.expand_dims(face_emb_ex,axis=4)
        # print(mix_ex.shape) #(1, 298, 257, 2)
        # print(face_emb_ex.shape) #(1, 75, 1, 1792, 1)
        cRMs = av_model.predict([mix_ex,face_emb_ex])
        #print(cRMs.shape) # (1, 298, 257, 2, 1)
        cRMs = cRMs[0]
        prefix =''
        for idx in single_idxs:
            prefix +=idx+'_'
        cRM =cRMs[:,:,:,0]
        assert cRM.shape ==(298,257,2)
        # mixスペクトログラムにcRMマスクをかける
        F = utils.fast_icRM(mix,cRM)
        T = utils.fast_istft(F,power=False)
        filename = result_path+prefix+str(single_idxs[0])+'.wav'
        wavfile.write(filename,16000,T)

        count = count + 1
        if count%500 == 0:
            print(count)
