import socket
import time
import datetime as dt
from utilities import *
import pickle
import csv
import argparse
import multiprocessing


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
estimators = 100

encoding = 'utf-8'
buffer_size = 1024
freq = 10 # Frequency of reading
period_interval = 60 # seconds of processing
threshold = 0.3

# SENSOR ADDRESS
#sensor1_name = "127.0.0.1"

# FOG ADDRESS
#fog_ip = "10.128.0.2"
fog_ip = "127.0.0.1"
PORT = 10001



##########################

def criarCSV(name):
    
    f = open(name, 'w')

    try:

        writer = csv.writer(f)

        writer.writerow(('imageCounter', 'currentTime', 'meanNetworkDelay',
                         'meanResponseTime', 'classificationTime'))

    finally:
        f.close()

# -----------------------------------------------------------------------

class Message:
    def __init__(self, id, time, img, img_name,result):
        self.sensor_id = id
        self.time = time
        self.img = img
        self.img_name = img_name
        self.result = result



parser = argparse.ArgumentParser(description = 'Entradas')

parser.add_argument('--dispositivo', action = 'store', dest = 'd',
                           required = True, help = 'Cloud, Edge or Server.')
parser.add_argument('--workload', action = 'store', dest = 'w', required = True,
                           help = '0.1, 0.5 or 1.0')

arguments = parser.parse_args()

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

fog_address = (fog_ip, PORT)

print('Starting Cloud UP on %s Port %s' % fog_address, file=sys.stderr)
sock2.bind(fog_address)
sock2.listen(10001)



# ---------------------------- Model Related --------------------------
# Load the file with the images names and labels
mapping_csv = pd.read_csv(base_dir + '/train_classes.csv')
modelo = load_model(base_dir+'/'+model_name, compile=False) # CNN Model
modelo.compile(optimizer=opt, loss='binary_crossentropy', metrics=[fbeta]) # CNN Model
#modelo = joblib.load(base_dir+'/'+'knn_%s_.sav'%targ_shape[0]) # KNN modelo
#modelo = joblib.load(base_dir+'/'+'rfc_%s_%s_.sav'%(targ_shape[0],estimators)) # RFC Model

# Loading the image-label dictionary
mapping = create_file_mapping(mapping_csv)

# Loading the label-number dictionary
labels_map, inv_labels_map = create_tag_map(mapping_csv)


# Creating a list with all possible labels
classes = []
for i in range(len(inv_labels_map)):
    classes.append(inv_labels_map[i])
    

    
# -----------------------------------------------------------



name = "performance" + arguments.d + "_" + arguments.w + ".csv"
criarCSV(name)  # Chama a função para criar a csv

#time.sleep(1)
processos = []

# I will define for how long the algorithm will run
# Now I start counting how many time has passed
start = time.monotonic()
#while True:



def process_image(image, image_name):
    img = image
    imagefile = image_name

    # Predicting the label
    print(f"Predicting the labels of image:\n{image_name}\n")
    prediction = modelo.predict(img)


    #  ------ Testing the prediction

    # Defining a list with the particular image true labels
    true_classes = mapping[imagefile.split('.')[0]]

    # Defining a ordered list with the true labels and all other possible labels
    true_classes_list =[0 for i in range(len(classes))]
    for class_ in true_classes:
        index_ = classes.index(class_)
        true_classes_list[index_] = 1

    # Creating a dataframe to organize the data from the image classification
    df_labels = pd.DataFrame(classes, columns=['Labels'])
    df_labels['True_labels'] = pd.Series(true_classes_list)
    df_labels['Predicted_proba'] = pd.Series(prediction[0])

    # Defining as 1 the classes whose probability is bigger than the threshold
    def enconder(probabilidade):
        if probabilidade > threshold:
            return 1
        else:
            return 0

    print("The predictions results are: \n")
    df_labels['Predicted_labels'] = df_labels['Predicted_proba'].apply(enconder)
    print(df_labels)
    print('\n')

    TP = len(df_labels[(df_labels['True_labels'] == 1) & (df_labels['Predicted_labels'] == 1)])
    FP = len(df_labels[(df_labels['True_labels'] == 0) & (df_labels['Predicted_labels'] == 1)])
    TN = len(df_labels[(df_labels['True_labels'] == 0) & (df_labels['Predicted_labels'] == 0)])
    FN = len(df_labels[(df_labels['True_labels'] == 1) & (df_labels['Predicted_labels'] == 0)])
    print('True Positives: ', TP)
    print('False Positives: ', FP)
    print('True Negatives: ', TN)
    print('False Negatives: ', FN)
    print('\n')

    # Defining and calculating the metrics
    try:
        # Precision
        precision = round(TP / (TP + FP), 3)
        print('Avg Precision: ', precision)

        # Recall (Sensibility or True Positive Rate)
        recall = round(TP / (TP + FN), 3)
        print('Avg Recal: ', recall)

        # F1 Score (Weighted mean between precision e recall)
        f1_score = round(2 * (precision * recall) / (precision + recall), 3)

        # Overall Accuracy (Percent of right classifications of the total classifications)
        acc = round((TP+TN)/(TP + FP + TN + FN), 3)

        print('Accuracy: ', acc)
        print('F1_Score:', f1_score)
        print('\n')
        print('The predicted labels to this image are: ')
        print(df_labels[df_labels['Predicted_labels']==1]['Labels'])
        print('\n')
        
    except ZeroDivisionError as e:
        print(e)





def receive_image():
    mean_delay = 0.0
    counter = 0
    mean_delay2 = 0.0
    
    while True:

        end = time.monotonic()
        tempo = dt.timedelta(seconds = end-start)
        print(f"Se passaram {round(tempo.seconds/60, 2)} minutos.")
        if (tempo.seconds > period_interval):
            break

        try:
            f = open(name, 'a')
            writer = csv.writer(f)

            print('\n\n\nWaiting for client Connection...\n', file=sys.stderr)

            # This first loop ensures that if, for some reason, the connection breaks in the middle of the transference
            # It will try again until the transference is completed
            while True:
                try:

                    connection, client_address = sock2.accept()
                    print('Client Connected! ', file=sys.stderr)
                    print('Received MSG From Client %s\n' % client_address[0], file=sys.stderr)

                    # This second loops collects the incoming message. Since the image is too heavy
                    # It is broke down into pieces and received partially.
                    # When the message is null the loop is broken and them
                    # The pickle gather the pieces into a one.
                    # A list to gather all the pieces of the message
                    data = []
                    pieces = 1
                    while True:
                        packet = connection.recv(buffer_size)
                        if not packet: break
                        data.append(packet)
                        pieces += 1

                    print("The message was fully received!")
                    print(f"The message was broken into {pieces} pieces.")
                    print(f"{'-'*15}// end of message //{'-'*15}\n ... \n")

                    #connection.send(f"{fog_address} received your image!".encode(encoding))

                    # Now that the image is fully received, it is necessary to load it
                    msg = pickle.loads(b"".join(data))
                    break

                except Exception:
                    pass

            # Getting the transmission time
            # msg.time is the time which the message was sent from the client
            # now is the time that the image was fully received at the server.
            # So, delay2 is the difference between sending the image and receiving it.
            now = time.time()
            delay2 = time.time() - msg.time
            mean_delay2 = mean_delay2 + delay2
            connection.close()


            # Processing the image
            print(f"{'-'*15}// Processing Image //{'-'*15}\n", file=sys.stderr)
            print(f"Received a Array of shape {msg.img.shape}.\n")

            # Sending image to the processing
            process_image(msg.img, msg.img_name)

            # Chamando a função que executa o modelo
            """processo = multiprocessing.Process(target=run_model, args=[msg.img])
            processos.append(processo)
            processo.start() """
            

            # Displaying the image
            #img = array_to_img(img_array)
            #plt.imshow(img)
            #plt.show()
            # --------------------------------------------------------------------------------------

            # Now lets count the time after the image was processed
            # delay is the time since the image was sent from the client to when it finished being processed
            # And we setup a counter to count how many images were processed
            delay = time.time() - msg.time
            mean_delay = mean_delay + delay
            counter = counter + 1


            #data = pickle.dumps(msg)
            # ---------------------------------------------------------------------------------------
            print(f"{'-'*15}// Image processed //{'-'*15}\n", file=sys.stderr)
            currentDT = datetime.datetime.now()
            print('Current Time: %s' % str(currentDT))
            print('Mean response time: %f - MSG Counter: %f' % (mean_delay / counter, counter))
            print('Mean network delay: %f \n' % (mean_delay2 / counter))

            writer.writerow((counter, str(currentDT), mean_delay2 / counter, mean_delay / counter, delay))

        finally:
            f.close()

"""         end = time.monotonic()
        tempo = dt.timedelta(seconds = end-start)
        print(f"Se passaram {round(tempo.seconds/60, 2)} minutos.")


        if (tempo.seconds > period_interval):
            break """
    
#for processo in processos:
 #   processo.join()


# Starting the script
receive_image()