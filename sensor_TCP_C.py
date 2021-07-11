import socket
from socket import AF_INET, SOCK_DGRAM
import pause, datetime as dt
from utilities import *
import numpy as np
import pickle
import time

# #1 Coloquei tudo para o tensorflow.keras
# #2 np_utils está desatualizado para tensorflow >2, é apenas keras.utils

##########################
# CONFIGURATION
##########################

# Defining the hyparams
opt = SGD(lr=0.01, momentum=0.9)
targ_shape = (64, 64, 3)
targ_size = targ_shape[:-1]
dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
model_name = 'cnn_%s_SGD.h5'%(targ_shape[0])
sample_size = 1012

# SENSOR PERIOD IN SEC
period = 0.01

# FOG ADDRESS

#fog_name = '34.123.200.72' # IP Externo da Cloud
fog_name = "192.168.0.105" # IP local
#PORT = 3389 # Porta que a GC libera
PORT = 10001  # porta local


fog_address = (fog_name, PORT)
# SENSOR ADDRESS
#sensor_name = "0.0.0.0"

########################

#Carregamento da massa de dados
#X_teste e y_teste representam os dígitos de cada registro de X_treinamento e y_treinamento.

# (X_treinamento, y_treinamento), (X_teste, y_teste) = mnist.load_data()
# X_treinamento = X_treinamento.reshape((len(X_treinamento), np.prod(X_treinamento.shape[1:])))
#
# X_teste = X_teste.reshape((len(X_teste), np.prod(X_teste.shape[1:])))
# X_treinamento = X_treinamento.astype('float32')
# X_teste = X_teste.astype('float32')
# X_treinamento /= 255
# X_teste /= 255
# y_treinamento = to_categorical(y_treinamento, 10)
# y_teste = to_categorical(y_teste, 10)


class Message:
    def __init__(self, id, time, img, result):
        self.sensor_id = id
        self.time = time
        self.img = img
        self.result = result



'''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sensor_address = (sensor_name, 10000)
sock.bind(sensor_address)
sock.listen(5)

'''
#port = 5000

mean_delay = 0.0

counter = 0

current_time = datetime.datetime.now()
time.sleep(120)
start = time.monotonic()
while True:

    try:
        now_plus_period = current_time + datetime.timedelta(seconds=period)
        pause.until(now_plus_period)
        current_time = datetime.datetime.now()
        print('\n\n %s sending msg' % datetime.datetime.now(), file=sys.stderr)

        # Loading the test image from the test images directory
        #--------- CNN -----------
        img_name = test_fnames[np.random.randint(0, len(test_fnames))]
        print(img_name)
        img = load_img(train_dir + '/' + img_name, target_size=targ_size)
        imgarray = img_to_array(img)
        #imgarray = imgarray.reshape((1,) + imgarray.shape) # DL Models  [Alterando a dimensão, agora é um vetor unidimensional]
        imgarray = imgarray.reshape(1, -1) # ML Models
        imgarray = imgarray / 255



        #img = np.expand_dims(img, axis = 0) # nao precisa para o cnn
        msg = Message(1, time.time(), imgarray, -1)
        #msg2 = Message(1, time.time(), img_name, -1)
        data = pickle.dumps(msg)
        #data2 = pickle.dumps(msg2)

        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect(fog_address)
        sock2.sendall(data)
        #sock2.sendall(data2)
        sock2.close()
    except Exception:
        pass
    end = time.monotonic()
    tempo = dt.timedelta(seconds= end-start)
    if tempo.seconds >=2220:
        break
