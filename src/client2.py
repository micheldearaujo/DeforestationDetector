import socket
from socket import AF_INET, SOCK_DGRAM
import pause, datetime as dt
from utilities import *
import numpy as np
import pickle
import time
import csv

#### TESTANDO O ENVIO E RECEBINDO DE IMAGES ###

##########################
# CONFIGURATION
##########################

# Defining the hyparams
opt = SGD(lr=0.01, momentum=0.9)
targ_shape = (32, 32, 3)
targ_size = targ_shape[:-1]
dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
model_name = 'cnn_%s_SGD.h5'%(targ_shape[0])
sample_size = 1012

encoding = 'utf-8'
buffer_size = 1024
freq = 60           # Frequency of reading
period_interval = 1800    # seconds of processing

# Messenger frequency
period = 1.0

# FOG ADDRESS

fog_name = '34.125.201.89'  # IP Externo da Cloud
#fog_name = "127.0.0.1"     # IP local
PORT = 3389                 # Porta que a GC libera
#PORT = 10001               # porta local


fog_address = (fog_name, PORT)
# SENSOR ADDRESS
#sensor_name = "0.0.0.0"

#----------------------------------------------------------

class Message:
    def __init__(self, id, time, img, img_name, period, period_interval, c_time, targ_shape, result):
        """
        Send the image, the image name, the period, the period_interval and the image size
        """
        self.sensor_id = id
        self.time = time
        self.img = img
        self.img_name = img_name
        self.period = period
        self.period_interval = period_interval
        self.c_time = c_time
        self.targ_shape = targ_shape
        self.result = result



def load_image(c_time, period):

    # Loading the test image from the test images directory
    img_name =  test_fnames[np.random.randint(0, len(test_fnames))] # randomly chooses a image 
    print(f"Sending the {img_name}")
    img = load_img(train_dir + '/' + img_name, target_size=targ_size) # Loads it

    # Transforming into a array
    imgarray = img_to_array(img)
    print(f"Original shape: {imgarray.shape}")
    
    imgarray = imgarray.reshape((1,) + imgarray.shape) # DL Models  [Alterando a dimensão, agora é um vetor unidimensional]
    #imgarray = imgarray.reshape(1, -1) # ML Models
    imgarray = imgarray / 255


    # Showing the image
    #plt.imshow(img)
    #plt.show()
    print(f"Sent shape: {imgarray.shape}\n")

    # Create a class called Message that will hold and send different files and informations about the image
    # Such as: The array itself, the name of the image and the time which the images is being sent,
    # the period (frequency), and total period_interval and the image size.
    msg = Message(1, time.time(), imgarray, img_name, period, period_interval, c_time, targ_shape[0], -1)
    
    return msg


def send_image(period):

    qtdeImages = 0
    mean_delay = 0.0
    counter = 0
    current_time = datetime.datetime.now()

    # counting the passed processing time
    end = time.monotonic()
    tempo = dt.timedelta(seconds= end-start)
    print(f"Se passaram {round(tempo.seconds/60, 2)} minutos.\nWorkload = {period}")

    # Send images until period_interval
    
    while (tempo.seconds <= period_interval):
        print(tempo.seconds, "--------", period_interval)
        try:

            now_plus_period = current_time + datetime.timedelta(seconds=period)
            pause.until(now_plus_period)
            current_time = datetime.datetime.now()
            print('\n\n CurrentTime %s' % datetime.datetime.now(), file=sys.stderr)

            msg = load_image(tempo.seconds, period)

            data = pickle.dumps(msg)

            #data2 = pickle.dumps(msg2)

            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            print(f"Connecting to the server {fog_address}...")
            sock2.connect(fog_address)
            print("Connected!!\n")

            # Sending the data
            print("Sending the message...")
            sock2.sendall(data)
            print(f"Message sent!\n ...")
            qtdeImages += 1
            # Closing connection
            sock2.close()
            print("Connection Closed.\n")
            print('-'*30)

            #feedback = sock2.recv(buffer_size).decode(encoding)
            #print(feedback)


            # Waiting to send another one
            time.sleep(period)

            end = time.monotonic()
            tempo = dt.timedelta(seconds= end-start)
            print(f"Se passaram {round(tempo.seconds/60, 2)} minutos.\nWorkload = {period}")

        except Exception:
            pass



    # Finished processing
    with open("./Throughput.txt", "a") as file:
        file.write("-------------------------\n")
        file.write(f"Tamanho da imagem: {targ_size[0]}, workload: {period}\n")
        file.write(f"qtde Real de Mensagens enviadas: {qtdeImages}\n")
        file.write(f"qtde Teórica de Mensagens enviadas: {period_interval/period}\n")
    

    with open("Throughput.csv", "a") as f:
        print("escrevendo aquivo")
        writer = csv.writer(f)
        writer.writerow((
            "CNN", "Cloud", targ_size[0], period, period_interval/period, qtdeImages
        ))

    print("#############################")
    print("Finished Round")
    print("Resting for 60 seconds to the next round...")



""" with open("Throughput.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow((
        "Algorithm", "Pltaform", "Size", "Workload", "qtdeTeorica", "qtdeEnviada"
    )) """




#while True:

#for workload in [1.0, 0.75, 0.5, 0.25, 0.1]:
    # Start counting the processing time
workload = 0.01
start = time.monotonic()

send_image(workload)
time.sleep(60)
