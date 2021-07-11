import socket
from utilities import *
import pickle
import csv
import argparse

##########################
# CONFIGURATION
##########################

# Defining the hyparams
opt = SGD(lr=0.01, momentum=0.9)
targ_shape = (8, 8, 3)
targ_size = targ_shape[:-1]
dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
model_name = 'cnn_%s_SGD.h5'%(targ_shape[0])
sample_size = 4048
estimators = 100

# SENSOR ADDRESS
#sensor1_name = "127.0.0.1"

# FOG ADDRESS
#fog_name = "10.128.0.2"
fog_name = "192.168.0.104" # IP do meu note


##########################

def criarCSV(name):
    
    f = open(name, 'w')

    try:

        writer = csv.writer(f)

        writer.writerow(('imageCounter', 'currentTime', 'meanNetworkDelay',
                         'meanResponseTime'))

    finally:
        f.close()

# -----------------------------------------------------------------------

class Message:
    def __init__(self, id, time, img, result):
        self.sensor_id = id
        self.time = time
        self.img = img
        self.result = result


#sensor1_address = (sensor1_name, 10000)

parser = argparse.ArgumentParser(description = 'Entradas')

parser.add_argument('--dispositivo', action = 'store', dest = 'd',
                           required = True, help = 'Cloud, Edge or Server.')
parser.add_argument('--workload', action = 'store', dest = 'w', required = True,
                           help = '0.1, 0.5 or 1.0')

arguments = parser.parse_args()

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

fog_address = (fog_name, 5050)

print('Starting Cloud UP on %s Port %s' % fog_address, file=sys.stderr)
sock2.bind(fog_address)
sock2.listen(5)

#model = pickle.load(open('model.pkl', 'rb'))

# ---------------------------- Model Related --------------------------
# Load the file with the images names and labels
mapping_csv = pd.read_csv(base_dir + '/train_classes.csv')
modelo = load_model(base_dir+'/'+model_name, compile=False) # CNN Model
modelo.compile(optimizer=opt, loss='binary_crossentropy', metrics=[fbeta]) # CNN Model
#modelo = joblib.load(base_dir+'/'+'knn_%s.sav'%targ_shape[0]) # KNN modelo
#modelo = joblib.load(base_dir+'/'+'rfc_%s_%s.sav'%(targ_shape[0],estimators)) # RFC Model

# Loading the image-label dictionary
mapping = create_file_mapping(mapping_csv)

# Loading the label-number dictionary
labels_map, inv_labels_map = create_tag_map(mapping_csv)

# Loading the testset
#Xte, yte = load_testset_DL(dataset_name)

# Creating a list with all possible labels
classes = []
for i in range(len(inv_labels_map)):
    classes.append(inv_labels_map[i])
# -----------------------------------------------------------



mean_delay = 0.0
counter = 0
mean_delay2 = 0.0

# current_time = datetime.datetime.now()
name = "performance" + arguments.d + "_" + arguments.w + ".csv"
criarCSV(name)  # Chama a função para criar a csv


#criarCSV()  # Chama a função para criar a csv

while True:

    f = open(name, 'a')

    try:
        writer = csv.writer(f)

        print('\n\n\nWaiting for client Connection', file=sys.stderr)

        while True:
            try:

                connection, client_address = sock2.accept()
                data = []
                while True:
                    packet = connection.recv(1001)
                    if not packet: break
                    data.append(packet)
                msg = pickle.loads(b"".join(data))
                break
            except Exception:
                pass

        delay2 = time.time() - msg.time
        mean_delay2 = mean_delay2 + delay2
        print('Client Connected! ', file=sys.stderr)
        print('Received MSG From Client %s' % client_address[0], file=sys.stderr)
        print('Processing Image', file=sys.stderr)
        connection.close()

        # Processing the image
        prediction = modelo.predict(msg.img)

        # # Creating a ordered list with the images true labels and the other labels
        # true_classes = mapping[img_name.split('.')[0]]
        #
        # # Creating a ordered list with the images true labels and the other labels
        # true_classes_list = [0 for i in range(len(classes))]
        # for class_ in true_classes:
        #     index_ = classes.index(class_)
        #     true_classes_list[index_] = 1
        #
        # # Creating a dataframe to organize all the info
        # df_labels = pd.DataFrame(classes, columns=['Labels'])
        # df_labels['True_labels'] = pd.Series(true_classes_list)
        # df_labels['Predicted_proba'] = pd.Series(prediction[0])
        # df_labels['Predicted_labels'] = df_labels['Predicted_proba'].apply(enconder)
        # print(df_labels)
        #
        # TP = len(df_labels[(df_labels['True_labels'] == 1) & (df_labels['Predicted_labels'] == 1)])
        # FP = len(df_labels[(df_labels['True_labels'] == 0) & (df_labels['Predicted_labels'] == 1)])
        # TN = len(df_labels[(df_labels['True_labels'] == 0) & (df_labels['Predicted_labels'] == 0)])
        # FN = len(df_labels[(df_labels['True_labels'] == 1) & (df_labels['Predicted_labels'] == 0)])
        # print('True Positives: ', TP)
        # print('False Positives: ', FP)
        # print('True Negatives: ', TN)
        # print('False Negatives: ', FN)
        #
        # # ==========  Calculating the metrics =========
        # try:
        #     # Precision
        #     precision = round(TP / (TP + FP), 3)
        #     print('Avg Precision: ', precision)
        #
        #     # Recall (Sensibility ou True Positive Rate)
        #     recall = round(TP / (TP + FN), 3)
        #     print('Avg Recal: ', recall)
        #
        #     # F1 Score (Weighted average between precision and recall)
        #     f1_score = round(2 * (precision * recall) / (precision + recall), 3)
        #
        #     # Accuracy (Percentage of Trues)
        #     acc = round((TP + TN) / (TP + FP + TN + FN), 3)
        # except:
        #     pass
        #
        # print('Avg Accuracy: ', acc)
        # # # print('Avg F1_Score:', f1_score)
        # print('\n')
        # print('As classes previstas da imagem são: ')
        # print(df_labels[df_labels['Predicted_labels'] == 1]['Labels'])
        # # print('\n')

        delay = time.time() - msg.time
        mean_delay = mean_delay + delay
        counter = counter + 1
        data = pickle.dumps(msg)

        print('Image processed', file=sys.stderr)
        currentDT = datetime.datetime.now()
        print('Current Time: %s' % str(currentDT))
        print('Mean response time: %f - MSG Counter: %f' % (mean_delay / counter, counter))
        print('Mean network delay: %f \n' % (mean_delay2 / counter))

        writer.writerow((counter, str(currentDT), mean_delay2 / counter, mean_delay / counter))

    finally:
        f.close()
