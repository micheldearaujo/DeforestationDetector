"""
Random Forest Classifier to classify Amazon dataset

Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""
from utilities import *

sizes = [8, 16, 32, 64, 128]
estimators=[200, 300, 400]
for estimator in estimators:
    for size in sizes:

        # Defining the hyparams
        targ_shape = (size,size)
        dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
        estimators = estimator


        # Loading the dataset
        Xtr, Xval, ytr, yval = load_dataset_ML(dataset_name,targ_shape)


        # Creating and fitting the model
        rfc = RandomForestClassifier(n_estimators=estimators, verbose=1, oob_score=True)

        start_time = time.monotonic()
        rfc.fit(Xtr, ytr)
        end_time = time.monotonic()

        # Validating
        prev_val = 1 #evaluation(rfc, Xval, yval)
        score_val = 1 #rfc.score(rfc, Xval, yval)


        print('Tempo do treinamento: ')
        print('\n')
        print(timedelta(seconds=end_time - start_time))
        print('Amazon Dataset: ', targ_shape)
        print('F1_score_validation: ', prev_val)
        print('Score_validation: ', score_val)


        # Saving the model
        filename = 'rfc_%s_%s_.sav'%(targ_shape[0],estimators)
        joblib.dump(rfc, base_dir+'/'+filename)
        tempo = timedelta(seconds=end_time - start_time)

        # Printing the results
        file=open(base_dir+'/'+'rfc_training_.txt','a')
        file.write('Image Size: %s_%s\n'%(targ_shape[0],estimators))
        file.write('Training time: %s\n'%tempo)
        file.write('F1_Score_Validation: %s\n'%prev_val)
        file.write('Score_Validation: %s\n'%score_val)
        file.write('----------------------------------------------------\n')
        file.close()
