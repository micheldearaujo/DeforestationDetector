"""
Convolutional Neural Network to classify Amazon dataset
Predicting new images

Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""

# Importing the library
from utilities import *

# Definind the hyparams
opt = SGD(lr=0.01, momentum=0.9)
targ_shape = (8, 8, 3)
targ_size = targ_shape[:-1]
dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
model_name = 'cnn_%s_SGD.h5'%(targ_shape[0])
sample_size = 2048  #len(test_fnames)*0.5

# Load the file with the images names and labels
mapping_csv = pd.read_csv(base_dir + '/train_classes.csv')

# Defining as 1 the labels with probability > threshold
def enconder(probabilidade):
    if probabilidade>threshold:
        return 1
    else:
        return 0



# Loading the image-label dictionary
mapping = create_file_mapping(mapping_csv)

# Loading the label-number dictionary
labels_map, inv_labels_map = create_tag_map(mapping_csv)



# Creating a list with all possible labels
classes = []
for i in range(len(inv_labels_map)):
    classes.append(inv_labels_map[i])

# Defning the tresholds
threshold = 0.3

# Initializing the automatic prediction at 1000  images in the
# Test directory

def run():
    
    # Loading the compiling the previously trained model
    modelo = load_model(base_dir+'/'+model_name, compile=False)
    modelo.compile(optimizer=opt, loss='binary_crossentropy', metrics=[fbeta])

    # Loading the testset
    Xte, yte = load_testset_DL(dataset_name)

    classifying_times = []
    initial_time = time.monotonic()
    for k in range(sample_size):
        imagefile = test_fnames[np.random.randint(0, len(test_fnames))]

        # Loading the test image
        img_name = imagefile
        print(img_name)
        img = load_img(test_dir+'/'+img_name, target_size=targ_size)
        imgarray = img_to_array(img)
        imgarray = imgarray.reshape((1,)+imgarray.shape) # Alterando a dimensão, agora é um vetor unidimensional
        imgarray = imgarray/255

        # Classifying the new image
        start_time = time.monotonic()
        prediction = modelo.predict(imgarray)
        end_time = time.monotonic()
        tempo = timedelta(seconds=end_time - start_time)

        # Creating a ordered list with the images true labels and the other labels
        true_classes = mapping[imagefile.split('.')[0]]

        # Creating a ordered list with the images true labels and the other labels
        true_classes_list = [0 for i in range(len(classes))]
        for class_ in true_classes:
            index_ = classes.index(class_)
            true_classes_list[index_] = 1

        # Creating a dataframe to organize all the info
        df_labels = pd.DataFrame(classes, columns=['Labels'])
        df_labels['True_labels'] = pd.Series(true_classes_list)
        df_labels['Predicted_proba'] = pd.Series(prediction[0])
        df_labels['Predicted_labels'] = df_labels['Predicted_proba'].apply(enconder)
        print(df_labels)

        TP = len(df_labels[(df_labels['True_labels'] == 1) & (df_labels['Predicted_labels'] == 1)])
        FP = len(df_labels[(df_labels['True_labels'] == 0) & (df_labels['Predicted_labels'] == 1)])
        TN = len(df_labels[(df_labels['True_labels'] == 0) & (df_labels['Predicted_labels'] == 0)])
        FN = len(df_labels[(df_labels['True_labels'] == 1) & (df_labels['Predicted_labels'] == 0)])
        print('True Positives: ',TP)
        print('False Positives: ',FP)
        print('True Negatives: ',TN)
        print('False Negatives: ',FN)


        # ==========  Calculating the metrics =========
        try:
            # Precision
            precision = round(TP / (TP + FP), 3)
            print('Avg Precision: ', precision)

            # Recall (Sensibility ou True Positive Rate)
            recall = round(TP / (TP + FN), 3)
            print('Avg Recal: ', recall)

            # F1 Score (Weighted average beteewn precision and recall)
            f1_score = round(2 * (precision * recall) / (precision + recall), 3)

            # Accuracy (Percentage of Trues)
            acc = round((TP+TN)/(TP + FP + TN + FN), 3)
        except:
            pass

        # print('Avg Accuracy: ', acc)
        # print('Avg F1_Score:', f1_score)
        # print('\n')
        # print('As classes previstas da imagem são: ')
        print(df_labels[df_labels['Predicted_labels']==1]['Labels'])
        print('\n')
        # Terminando a contagem do tempo
        print('Classification Time: ')
        print(tempo)
        classifying_times.append(tempo)

    
    final_time = time.monotonic()
    processing_time = timedelta(seconds=final_time - initial_time)
    
    file=open(base_dir+'/'+'cnn_classificationtime.txt','a')
    file.write('Image Size: %s\n'%(targ_shape[0]))
    file.write('Average Single prediction time: %s\n'%np.mean(classifying_times))
    try:
        file.write('Standard deviation Single prediction time: %s\n'%np.std(classifying_times))
    except:
        pass
    file.write('samples: %s\n'%len(classifying_times))
    file.write('Total processing time: %s\n'%processing_time)
    file.write('----------------------------------------------------\n')
    file.close()
    
    

shapes = [8, 16, 32, 64, 128]
for shape in shapes:
    
    opt = SGD(lr=0.01, momentum=0.9)
    targ_shape = (shape, shape, 3)
    targ_size = targ_shape[:-1]
    dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
    model_name = 'cnn_%s_SGD.h5'%(targ_shape[0])
    sample_size = 2024  #len(test_fnames)*0.5
    
    run()
    sleep(120)
    
