import os, glob
#import pandas as pd
#inspect_dir = 'face_input'
#inspect_range = (0,17)
#valid_frame_path = 'valid_frame.txt'
#AfewMissed_frame_path = 'AfewMissd_frame.txt'
#segment_num_list = pd.read_csv('segment_num_list.csv')

dir_path = './marged_output_video/'
if not os.path.isdir(dir_path):
    os.mkdir(dir_path)

wav_dir = './predict_testdata_exp2/'
video_dir = './video_data/'
print('1,wav files directory : %s'%wav_dir)
print('2,video files directory : %s'%video_dir)
for video_file_path in glob.glob(video_dir+'*.mp4'):
    print(video_file_path)
    segment_idx = video_file_path.rsplit('/',1)[1].replace('.mp4','').replace('fps25_','')
    # 動画に対応する音声があるかチェック
    list=glob.glob(wav_dir + segment_idx + '_' + '*.wav')
    print('length :'+str(len(list)))
    print(list)
    if len(list) == 0:
        continue
    # 動画に対応する音声がテストデータにある場合
    for wav_file_path in glob.glob(wav_dir + segment_idx+ '_' + '*.wav'):
        command = ''
        video_pair_idx = wav_file_path.rsplit('/',1)[1].replace('.wav','')
        output_path = dir_path + 'MargedVideo_' +video_pair_idx + '.mp4' 
        #command += 'ffmpeg -i %s -i %s -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 %s;' %(video_file_path, wav_file_path, output_path)
        command = 'ffmpeg -i %s -i %s -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 %s;' %(video_file_path, wav_file_path, output_path)
        os.system(command)
#print(command)
#os.system(command)
