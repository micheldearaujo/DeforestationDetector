"""
Random Forest Classifier to classify Amazon dataset
Evaluating the model

Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""
from utilities import *

# -----------------------------------------------

# Defining the hyparams
targ_shape = (128,128,3)
targ_size = targ_shape[:-1]
dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
estimators=500

# -------------------------------------------------
# Load the file with the images names and labels
mapping_csv = pd.read_csv(base_dir + '/' + 'train_classes.csv')


# ------------------------------------------------------------
# Calling the dictionary function
mapping = create_file_mapping(mapping_csv)

# Loading the label-number dictionary
labels_map, inv_labels_map = create_tag_map(mapping_csv)

# Creating a list with all possible labels
all_labels = []
for i in range(len(inv_labels_map)):
    all_labels.append(inv_labels_map[i])

# Loading the compiling the previously trained model
rfc = joblib.load(base_dir+'/'+'rfc_%s_%s.sav'%(targ_shape[0],estimators))

# Loading the testset
Xte, yte = load_testset_ML(dataset_name)

# Classifying all the images in the test set
TP, FP, TN, FN = 0, 0, 0, 0
start_time=time.monotonic()
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
    predicted_labels = rfc.predict(imgarray)
    #print(predicted_labels)

    # Creating a list with images true labels
    true_labels = mapping['train_%s'%image_no]

    # Creating a ordered list with the images true labels and the other labels
    true_labels_list = [0 for i in range(len(all_labels))]
    for label_ in true_labels:
        index_ = all_labels.index(label_)
        true_labels_list[index_] = 1

    # Creating a dataframe with all scores
    rfc_df = pd.DataFrame(all_labels, columns=['Labels'])
    rfc_df['True_labels'] = pd.Series(true_labels_list)
    rfc_df['Predicted_labels'] = pd.Series(predicted_labels[0])
    #print(rfc_df)

    # Calculating the TP, FP, TN, FN
    TP += len(rfc_df[(rfc_df['True_labels'] == 1) & (rfc_df['Predicted_labels'] == 1)])
    FP += len(rfc_df[(rfc_df['True_labels'] == 0) & (rfc_df['Predicted_labels'] == 1)])
    TN += len(rfc_df[(rfc_df['True_labels'] == 0) & (rfc_df['Predicted_labels'] == 0)])
    FN += len(rfc_df[(rfc_df['True_labels'] == 1) & (rfc_df['Predicted_labels'] == 0)])

end_time=time.monotonic()
tempo = timedelta(seconds=end_time - start_time)

# Calculating the metrics
# Precision
precision = round(TP / (TP + FP), 3)

# Recall (Sensibility ou True Positive Rate)
recall = round(TP / (TP + FN), 3)

# Accuracy (Percentage of Trues)
acc = round((TP + TN) / (TP + FP + TN + FN), 3)

# F1 Score (Weighted average betewwn precision and recall)
f1_score = round(2 * (precision * recall) / (precision + recall), 3)



#----------------------------------------------------

print('Evaluation Time')
print(tempo)

file=open(base_dir+'/'+'rfc_scores.txt','a')
file.write('Image Size: %s_%s\n'%(targ_shape[0],estimators))
file.write('Evaluation time: %s\n'%tempo)
file.write('Avg Precision: %s\n'%precision)
file.write('Avg Recall: %s\n'%recall)
file.write('Avg Accuracy: %s\n'%acc)
file.write('Avg F1_Score: %s\n'%f1_score)
file.write('----------------------------------------------------\n')
file.close()
