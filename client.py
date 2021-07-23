import socket
from socket import AF_INET, SOCK_DGRAM
import pause, datetime as dt
from utilities import *
import numpy as np
import pickle
import time

# #1 Coloquei tudo para o tensorflow.keras
# #2 np_utils está desatualizado para tensorflow >2, é apenas keras.utils

#### TESTANDO O ENVIO E RECEBINDO DE IMAGES ###

##########################
# CONFIGURATION
##########################

# Defining the hyparams
opt = SGD(lr=0.01, momentum=0.9)
targ_shape = (16, 16, 3)
targ_size = targ_shape[:-1]
dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
model_name = 'cnn_%s_SGD.h5'%(targ_shape[0])
sample_size = 1012

buffer_size = 1024
encoding = 'utf-8'
# SENSOR PERIOD IN SEC
period = 2

# FOG ADDRESS

#fog_name = '34.123.200.72' # IP Externo da Cloud
fog_name = "192.168.0.104" # IP local
#PORT = 3389 # Porta que a GC libera
PORT = 10001  # porta local


fog_address = (fog_name, PORT)
# SENSOR ADDRESS
#sensor_name = "0.0.0.0"

#----------------------------------------------------------


class Message:
    def __init__(self, id, time, img, img_name, result):
        self.sensor_id = id
        self.time = time
        self.img = img
        self.img_name = img_name
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
time.sleep(5)
start = time.monotonic()
#while True:

try:
    now_plus_period = current_time + datetime.timedelta(seconds=period)
    pause.until(now_plus_period)
    current_time = datetime.datetime.now()
    print('\n\n CurrentTime %s' % datetime.datetime.now(), file=sys.stderr)

    # Loading the test image from the test images directory
    img_name =  test_fnames[np.random.randint(0, len(test_fnames))] # randomly chooses a image 
    print(f"Sending the {img_name}")
    img = load_img(train_dir + '/' + img_name, target_size=targ_size) # Loads it

    # Transforming into a array
    imgarray = img_to_array(img)
    print(f"Original shape: {imgarray.shape}")
    
    #imgarray = imgarray.reshape((1,) + imgarray.shape) # DL Models  [Alterando a dimensão, agora é um vetor unidimensional]
    imgarray = imgarray.reshape(1, -1) # ML Models
    imgarray = imgarray / 255


    # Showing the image
    #plt.imshow(img)
    #plt.show()
    print(f"Sent shape: {imgarray.shape}\n")

    # Create a class called Message that will hold different files and informations about the image
    # Such as: The array itself, the name of the image and the time which the images is being sent.
    msg = Message(1, time.time(), imgarray, img_name, -1)

    #msg2 = Message(1, time.time(), img_name, -1)
    data = pickle.dumps(msg)

    #data2 = pickle.dumps(msg2)

    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Connecting to the server {fog_address}...")
    sock2.connect(fog_address)
    print("Connected!!\n")

    print("Sending the message...")
    sock2.sendall(data)
    print(f"Message sent!\n ...")
    print("Connection Closed.")

    #print(sock2.recv(buffer_size).decode(encoding)) 

    sock2.close()
except Exception:
    pass
end = time.monotonic()
tempo = dt.timedelta(seconds= end-start)
#if tempo.seconds >=300:
   # break
