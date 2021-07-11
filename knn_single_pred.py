"""
K-Nearest Neighbors to classify Amazon dataset
Make single predictions
Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""
from utilities import *


# Defining the hyperams
targ_shape = (8, 8, 3)
targ_size = targ_shape[:-1]
dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
sample_size = 404  #len(test_fnames)*0.1

# Load the file with the images names and labels
mapping_csv = pd.read_csv(base_dir + '/' + 'train_classes.csv')

# Loading the compiling the previously trained model
knn = joblib.load(base_dir+'/'+'knn_%s.sav'%targ_shape[0])

# Loading the testset
#Xte, yte = load_testset_ML(dataset_name)

# Loading the image-label dictionary
mapping = create_file_mapping(mapping_csv)

# Loading the label-number dictionary
labels_map, inv_labels_map = create_tag_map(mapping_csv)

# Test the algorithm in 404 randomly sampled images from the test directory
# To get the average classifying time
classifying_times = []
for k in range(sample_size):
    imagefile = test_fnames[np.random.randint(0, len(test_fnames))]
    img_name = imagefile
    print(img_name)
    img = load_img(train_dir+'/'+img_name, target_size=targ_size)
    imgarray = img_to_array(img)
    imgarray = imgarray.reshape(1,-1) # Alterando a dimensão, agora é um vetor unidimensional
    imgarray = imgarray/255

    # Avaliando o modelo
    #score = rfc.score(Xte, yte)
    #print('Amazon Dataset: ', targ_shape)
    #print('Score_test: ', score)

    # Predicting the label
    start_time=time.monotonic()
    predicted_labels = knn.predict(imgarray)
    end_time=time.monotonic()
    tempo = timedelta(seconds=end_time - start_time)
    print(predicted_labels)

    # Creating a list with images true labels
    true_labels = mapping[imagefile.split('.')[0]]

    # Creating a list with all possible labels
    all_labels = []
    for i in range(len(inv_labels_map)):
        all_labels.append(inv_labels_map[i])

    # Creating a ordered list with the images true labels and the other labels
    true_labels_list =[0 for i in range(len(all_labels))]
    for class_ in true_labels:
        index_ = all_labels.index(class_)
        true_labels_list[index_] = 1

    # Creating a dataframe to organize all the info
    knn_df = pd.DataFrame(all_labels, columns=['Labels'])
    knn_df['True_labels'] = pd.Series(true_labels_list)
    knn_df['Predicted_labels'] = pd.Series(predicted_labels[0])
    print(knn_df)
    print('The predicted labels are: ')
    print(knn_df[knn_df['Predicted_labels']==1]['Labels'])
    print('\n')
    print('Classification Time:')
    print(tempo)
    classifying_times.append(tempo)

file=open(base_dir+'/'+'knn_classificationtime.txt','a')
file.write('Image Size: %s\n'%targ_shape[0])
file.write('Average Single prediction time: %s\n'%np.mean(classifying_times))
#file.write('Standard deviation Single prediction time: %s\n'%np.std(classifying_times))
file.write('----------------------------------------------------\n')
file.close()