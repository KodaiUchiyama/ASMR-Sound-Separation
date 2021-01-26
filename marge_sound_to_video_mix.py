# 作成した分離済み音声付き動画のリストから，対応する合成音の付き動画を作成する

import os, glob

dir_path = './marged_output_video_mix/'
if not os.path.isdir(dir_path):
    os.mkdir(dir_path)

wav_dir = './data/AV_model_database/mix_wav/'
video_dir = './marged_output_video/'
print('1,wav files directory : %s'%wav_dir)
print('2,video files directory : %s'%video_dir)
for video_file_path in glob.glob(video_dir+'*.mp4'): #MargedVideo_25-108_00028_25-108.mp4
    segment_idx = video_file_path.rsplit('/',1)[1].replace('.mp4','').replace('MargedVideo_','').rsplit('_',1)[0]
    # 動画に対応する音声があるかチェック
    list=glob.glob(wav_dir +'mix_'+ segment_idx + '.wav') #/mix_wav/mix_0-105_00055.wav
    print('length :'+str(len(list)))
    print(list)
    if len(list) == 0:
        print('対応する合成音なし')
        continue
    # 動画に対応する音声がテストデータにある場合
    command = ''
    wav_file_path = wav_dir +'mix_'+ segment_idx + '.wav'
    output_path = dir_path + 'MargedVideo_' +segment_idx + '.mp4' 
    #command += 'ffmpeg -i %s -i %s -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 %s;' %(video_file_path, wav_file_path, output_path)
    command = 'ffmpeg -i %s -i %s -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 %s;' %(video_file_path, wav_file_path, output_path)
    os.system(command)
#print(command)
#os.system(command)
