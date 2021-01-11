with open('./AV_model_database/dataset_train.txt', 'r') as tr:
    lines = tr.readlines()
    for line in lines:
        info = line.strip().split(' ') #mix_13-148_00124.npy crm_13-148_00124_13-148.npy
        num1 = info[0].strip().rsplit('_',1)[0] #mix_13-148 
        num2 = num1.replace('mix_','')
        new_line = line.strip() + ' ' + num2 + '_face_emb.npy' + '\n'
        #print(new_line)
        with open('AVdataset_train.txt', 'a') as f:
            f.write(new_line)

with open('./AV_model_database/dataset_val.txt', 'r') as tr:
    lines = tr.readlines()
    for line in lines:
        info = line.strip().split(' ') #mix_13-148_00124.npy crm_13-148_00124_13-148.npy
        num1 = info[0].strip().rsplit('_',1)[0] #mix_13-148 
        num2 = num1.replace('mix_','')
        new_line = line.strip() + ' ' + num2 + '_face_emb.npy' + '\n'
        #print(new_line)
        with open('AVdataset_val.txt', 'a') as f:
            f.write(new_line)

with open('./AV_model_database/dataset_test.txt', 'r') as tr:
    lines = tr.readlines()
    for line in lines:
        info = line.strip().split(' ') #mix_13-148_00124.npy crm_13-148_00124_13-148.npy
        num1 = info[0].strip().rsplit('_',1)[0] #mix_13-148 
        num2 = num1.replace('mix_','')
        new_line = line.strip() + ' ' + num2 + '_face_emb.npy' + '\n'
        #print(new_line)
        with open('AVdataset_test.txt', 'a') as f:
            f.write(new_line)

