"""
K-Nearest Neighbors to classify Amazon dataset

Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""
from utilities import *

sizes = [64]
for size in sizes:

    # Definind the hyperams
    targ_shape = (size, size)
    dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])


    # Loading the dataset
    Xtr, Xval, ytr, yval = load_dataset_ML(dataset_name, targ_shape)

    # error_rate = []
    # Escolhendo o melhor k
    # for i in range(1, 41):
    #     print('loop %s' % i)
    #     knn = KNeighborsClassifier(n_neighbors=i)
    #     knn.fit(Xtr, ytr)
    #     pred_i = knn.predict(Xval)
    #     error_rate.append(np.mean(pred_i != yval))
    # plt.figure(figsize=(10, 6))
    # plt.plot(range(1, 41), error_rate, color='blue', linestyle='dashed', marker='o',
    #          markerfacecolor='red', markersize=10)
    # plt.title('Error Rate vs. K Value')
    # plt.xlabel('K')
    # plt.ylabel('Error Rate')
    # plt.show()

    # Creating the model
    knn = KNeighborsClassifier(n_neighbors=19)

    start_time = time.monotonic()
    knn.fit(Xtr, ytr)
    end_time = time.monotonic()

    # Making predictions and validation
    # Validation set
    #prev_val = evaluation(knn,Xval, yval)
    #score_val = knn.score(knn,Xval, yval)

    # # Test set
    # prev_te = evaluation(Xte, yte)
    # score_te = knn.score(Xte, yte)

    # Saving the model
    filename = 'knn_%s_.sav'%targ_shape[0]
    joblib.dump(knn, base_dir+'/'+filename)

    tempo = timedelta(seconds=end_time - start_time)

    # Printing the results
    print('Amazon Dataset: ', targ_shape)
    #print('F1_score_validation: ', prev_val)
    #print('F1_score_test: ', prev_te)
    #print('Score_validation: ', score_val)
    #print('Score_test: ', score_te)
    print('Tempo do treinamento: ')
    print('\n')
    print(tempo)