"""
Random Forest Classifier to classify Amazon dataset
Making single predictions

Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""
from utilities import *

# Defining the hyparams
targ_shape = (64, 64, 3)
targ_size = targ_shape[:-1]
dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
estimators = 500
sample_size = 404 #len(test_fnames)*0.1


# Load the file with the images names and labels
mapping_csv = pd.read_csv(base_dir + '/' + 'train_classes.csv')


# Loading the compiling the previously trained model
rfc = joblib.load(base_dir+'/'+'rfc_%s_%s.sav'%(targ_shape[0],estimators))

# Carregando o testset inteiro
#Xte, yte = load_testset(dataset_name)

# Loading the image-label dictionary
labels_map, inv_labels_map = create_tag_map(mapping_csv)

# Test the algorithm in 404 randomly sampled images from the test directory
# To get the average classifying time
classifying_times = []
for k in range(sample_size):
    imagefile = test_fnames[np.random.randint(0, len(test_fnames))]

    # Loading the test image
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

    # Classifying the new image
    start_time = time.monotonic()
    predicted_labels = rfc.predict(imgarray)
    end_time=time.monotonic()
    print(predicted_labels)

    # Creating a list with images true labels
    mapping = create_file_mapping(mapping_csv)
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


    # Creating a dataframe with all scores
    rfc_df = pd.DataFrame(all_labels, columns=['Labels'])
    rfc_df['True_labels'] = pd.Series(true_labels_list)
    rfc_df['Predicted_labels'] = pd.Series(predicted_labels[0])
    print(rfc_df)


    print('The predicted_labels are: ')
    print(rfc_df[rfc_df['Predicted_labels']==1]['Labels'])
    print('\n')


    tempo = timedelta(seconds=end_time - start_time)
    print('Tempo de Classificação:')
    print(tempo)
    classifying_times.append(tempo)

# Printing the results
file=open(base_dir+'/'+'rfc_classificationtime.txt','a')
file.write('Image Size: %s_%s\n'%(targ_shape[0],estimators))
file.write('Average Single prediction time: %s\n'%np.mean(classifying_times))
#file.write('Standard deviation Single prediction time: %s\n'%np.std(classifying_times))
file.write('----------------------------------------------------\n')
file.close()