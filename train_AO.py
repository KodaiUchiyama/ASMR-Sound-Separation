import sys

sys.path.append('./model/AO_model/')
import AO_model as AO
from option import ModelMGPU, latest_file
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, Callback
from keras.models import Model, load_model
from data_load import AOGenerator
from keras.callbacks import TensorBoard, CSVLogger
from keras import optimizers
import os
from loss import audio_discriminate_loss2 as audio_loss
import tensorflow as tf
import matplotlib.pyplot as plt
# Resume Model
resume_state = False

# Parameters
people_num = 1
epochs = 100
initial_epoch = 0
batch_size = 4
gamma_loss = 0.1
beta_loss = gamma_loss * 2

# Accelerate Training Process
workers = 8
MultiProcess = True
NUM_GPU = 1 

# PATH
model_path = './saved_AO_models'  # model path
database_path = 'data/'

# create folder to save models
folder = os.path.exists(model_path)
if not folder:
    os.makedirs(model_path)
    print('create folder to save models')
filepath = model_path + "/AOmodel-" + str(people_num) + "p-{epoch:03d}-{val_loss:.5f}.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
csv_logger = CSVLogger('training.log',separator=',',append=False)

# automatically change lr
def scheduler(epoch):
    ini_lr = 0.0001
    lr = ini_lr
    if epoch >= 5:
        lr = ini_lr / 5
    if epoch >= 10:
        lr = ini_lr / 10
    return lr


rlr = LearningRateScheduler(scheduler, verbose=1)
# format: mix.npy food_single.npy 
trainfile = []
valfile = []
'''
with open((database_path + 'AV_log/' + 'AVdataset_train_small.txt'), 'r') as t:
    trainfile = t.readlines()
with open((database_path + 'AV_log/' + 'AVdataset_val_small.txt'), 'r') as v:
    valfile = v.readlines()
'''
with open((database_path + 'AV_log/' + 'AVdataset_train.txt'), 'r') as t:
    trainfile = t.readlines()
with open((database_path + 'AV_log/' + 'AVdataset_val.txt'), 'r') as v:
    valfile = v.readlines()
# the training steps
if resume_state:
    latest_file = latest_file(model_path + '/')
    AV_model = load_model(latest_file, custom_objects={"tf": tf})
    info = latest_file.strip().split('-')
    initial_epoch = int(info[-2])
else:
    AO_model = AO.AO_model(people_num)

train_generator = AOGenerator(trainfile, database_path=database_path, batch_size=batch_size, shuffle=True)
val_generator = AOGenerator(valfile, database_path=database_path, batch_size=batch_size, shuffle=True)

if NUM_GPU > 1:
    parallel_model = ModelMGPU(AV_model, NUM_GPU)
    adam = optimizers.Adam()
    loss = audio_loss(gamma=gamma_loss, beta=beta_loss, people_num=people_num)
    parallel_model.compile(loss=loss, optimizer=adam)
    print(AV_model.summary())
    history=parallel_model.fit_generator(generator=train_generator,
                                 validation_data=val_generator,
                                 epochs=epochs,
                                 workers=workers,
                                 use_multiprocessing=MultiProcess,
                                 callbacks=[TensorBoard(log_dir='./log_AV'), checkpoint, rlr],
                                 initial_epoch=initial_epoch
                                 )
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss plt.plot(history.history['loss']) plt.plot(history.history['val_loss']) plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
if NUM_GPU <= 1:
    adam = optimizers.Adam()
    #loss = audio_loss(gamma=gamma_loss, beta=beta_loss, people_num=people_num)
    loss = 'mean_squared_error'
    AO_model.compile(optimizer=adam, loss=loss)
    print(AO_model.summary())
    history=AO_model.fit_generator(generator=train_generator,
                           validation_data=val_generator,
                           epochs=epochs,
                           workers=workers,
                           use_multiprocessing=MultiProcess,
                           callbacks=[TensorBoard(log_dir='./log_AV'), checkpoint, rlr, csv_logger],
                           initial_epoch=initial_epoch
                           )
    '''
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss plt.plot(history.history['loss']) plt.plot(history.history['val_loss']) plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    '''
