"""
K-Nearest Neighbors to classify Amazon dataset
Evaluating the model
Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""
from utilities import *

# -----------------------------------------------

# Definindo os parametros
# targ_shape = (16, 16,3)
# targ_size = targ_shape[:-1]
# dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])


# -------------------------------------------------

# Load the file with the images names and labels
mapping_csv = pd.read_csv(base_dir + '/' + 'train_classes.csv')

# ------------------------------------------------------------

# Loading the image-label dictionary
mapping = create_file_mapping(mapping_csv)

# Loading the label-number dictionary
labels_map, inv_labels_map = create_tag_map(mapping_csv)

# Creating a list with all possible labels
all_labels = []
for i in range(len(inv_labels_map)):
    all_labels.append(inv_labels_map[i])


# Classifying all the images in the test set
start_time=time.monotonic()
def evaluate_model(dataset_name):
    TP, FP, TN, FN = 0, 0, 0, 0
    for image_no in range(len(Xte), 2*len(Xte)):
        print('progresso: %s de %s'%(image_no,2*len(Xte)))
        # Carregando a imagem de test
        img_name = 'train_%s.jpg'%image_no
        #print(img_name)
        img = load_img(train_dir+'/'+img_name, target_size=targ_size)
        imgarray = img_to_array(img)
        imgarray = imgarray.reshape(1,-1) # Alterando a dimensão, agora é um vetor unidimensional
        imgarray = imgarray/255

        # Predicting the new image
        predicted_labels = knn.predict(imgarray)
        #print(predicted_labels)

        # Let`s get the image True Labels:
        true_labels = mapping['train_%s'%image_no]

        # Criando uma lista ordenada com as classes verdadeiras e todas as outras classes
        true_labels_list = [0 for i in range(len(all_labels))]
        for label_ in true_labels:
            index_ = all_labels.index(label_)
            true_labels_list[index_] = 1

        # Criando um dataframe para organizar todas as informações da classificacao da imagem
        knn_df = pd.DataFrame(all_labels, columns=['Labels'])
        knn_df['True_labels'] = pd.Series(true_labels_list)
        knn_df['Predicted_labels'] = pd.Series(predicted_labels[0])
        #print(rfc_df)

        # Calculando os TP, FP, TN, FN
        TP += len(knn_df[(knn_df['True_labels'] == 1) & (knn_df['Predicted_labels'] == 1)])
        FP += len(knn_df[(knn_df['True_labels'] == 0) & (knn_df['Predicted_labels'] == 1)])
        TN += len(knn_df[(knn_df['True_labels'] == 0) & (knn_df['Predicted_labels'] == 0)])
        FN += len(knn_df[(knn_df['True_labels'] == 1) & (knn_df['Predicted_labels'] == 0)])

    # definindo e calculando as métricas:
    # print('Avg True Positives: ', TP)
    # print('Avg False Positives: ', FP)
    # print('Avg True Negatives: ', TN)
    # print('Avg False Negatives: ', FN)

    # Calculating the metrics
    # Precision
    precision = round(TP / (TP + FP), 3)

    # Recall (Sensibility ou True Positive Rate)
    recall = round(TP / (TP + FN), 3)

    # Accuracy (Percentage of Trues)
    acc = round((TP+TN)/(TP + FP + TN + FN), 3)

    # F1 Score (Weighted average betewwn precision and recall)
    f1_score = round(2 * (precision * recall) / (precision + recall), 3)



    #----------------------------------------------------
    end_time=time.monotonic()
    tempo = timedelta(seconds=end_time - start_time)
    print('Tempo de Evaluation:')
    print(tempo)

    file=open(base_dir+'/'+'knn_scores.txt','a')
    file.write('Image Size: %s\n'%targ_shape[0])
    file.write('Evaluation time: %s\n'%tempo)
    file.write('Avg Precision: %s\n'%precision)
    file.write('Avg Recall: %s\n'%recall)
    file.write('Avg Accuracy: %s\n'%acc)
    file.write('Avg F1_Score: %s\n'%f1_score)
    file.write('----------------------------------------------------\n')
    file.close()


for k in [12,24,48,96]:
    targ_shape = (k, k, 3)
    targ_size=targ_shape[:-1]
    print('Modelo: %s'%targ_shape[0])
    # Loading the testset
    dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
    Xte, yte = load_testset_ML(dataset_name)
    knn = joblib.load(base_dir+'/'+'knn_%s.sav'%targ_shape[0])
    evaluate_model(dataset_name)