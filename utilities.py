"""
Models Utilities

Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""

import numpy as np
import sys, os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.image import imread
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras import backend
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img, load_img
import time
import datetime
from datetime import timedelta
import joblib
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

# Definindo o caminho dos diretorios
#base_dir = '/media/michel/DADOS/data/amazonia/kaggle' # Ubuntu
base_dir = 'D:/data/amazonia/kaggle'
train_dir = os.path.join(base_dir, 'train-jpg')
test_dir = os.path.join(base_dir, 'test-jpg')
train_fnames = os.listdir(train_dir)
test_fnames = os.listdir(test_dir)


# Loading the dataset for the ML algorithms
def load_dataset_ML(dataset_name, targ_shape):
    data = np.load(base_dir+'/'+dataset_name)
    X, y = data['arr_0'], data['arr_1']
    print('Dimensões: ')
    print('X: ',X.shape, '\n y: ', y.shape)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=1)
    Xtr = Xtr.reshape(Xtr.shape[0], targ_shape[0] * targ_shape[0] * 3)  ## Vamos concatenar os dados das 3 dimensoes em apenas 1 dimensão
    Xte = Xte.reshape(Xte.shape[0], targ_shape[0] * targ_shape[0] * 3)
    #Xtr = Xtr.reshape(-1,1)
    #Xte = Xte.reshape(-1,1)
    # Dividindo o set test em dois, para temos validation+test
    Xval = Xte[:4048, :]
    yval = yte[:4048]
    Xte = Xte[4048:, :]
    yte = yte[4048:]
    # Normalizando os dados entre 0 e 1
    scaler = MinMaxScaler()
    Xtr = scaler.fit_transform(Xtr)
    Xval = scaler.fit_transform(Xval)
    Xte = scaler.fit_transform(Xte)
    return Xtr, Xval, ytr, yval

# Loading the dataset for the DL algorithms
def load_dataset_DL(dataset_name):
    # Carregando
    data = np.load(base_dir + '/'+ dataset_name)
    X, y = data['arr_0'], data['arr_1']
    # Separando os sets de training e testing
    Xtr, Xval, ytr, yval = train_test_split(X, y, test_size=0.2, random_state=1)
    Xval, yval = Xval[:4048,:], yval[:4048]
    print('As dimensões dos vetores são: \n')
    print('Xtr: ', Xtr.shape)
    print('\n')
    print('ytr: ', ytr.shape)
    print('\n')
    print('Xval: ', Xval.shape)
    print('\n')
    print('yval: ', yval.shape)
    print('\n')
    return Xtr, Xval, ytr, yval

def load_testset_DL(dataset_name):
    # Carregando
    data = np.load(base_dir + '/'+ dataset_name)
    X, y = data['arr_0'], data['arr_1']
    # Criando o testset, lembrando que os primeiros 4048 são de validação, já utilizados em cima
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=1)
    Xte, yte = Xte[4048:,:], yte[4048:]
    print('As dimensões dos vetores são: \n')
    print('Xte shape: ', Xte.shape)
    print('\n')
    print('yte shape: ', yte.shape)
    print('\n')
    return Xte, yte

def load_testset_ML(dataset_name, targ_shape):
    # Carregando
    data = np.load(base_dir + '/'+ dataset_name)
    X, y = data['arr_0'], data['arr_1']
    # Criando o testset, lembrando que os primeiros 4048 são de validação, já utilizados em cima
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=1)
    Xtr = Xtr.reshape(Xtr.shape[0], targ_shape[0] * targ_shape[0] * 3)  ## Vamos concatenar os dados das 3 dimensoes em apenas 1 dimensão
    Xte = Xte.reshape(Xte.shape[0], targ_shape[0] * targ_shape[0] * 3)
    Xte, yte = Xte[4048:,:], yte[4048:]
    print('As dimensões dos vetores são: \n')
    print('Xte shape: ', Xte.shape)
    print('\n')
    print('yte shape: ', yte.shape)
    print('\n')
    return Xte, yte


# Creating a function to calcutate the fbeta score
def fbeta(y_true, y_pred, beta=2):
    # Clipando a previsao
    y_pred = backend.clip(y_pred, 0, 1)
    tp = backend.sum(backend.round(backend.clip(y_true*y_pred, 0, 1)), axis=1)
    fp = backend.sum(backend.round(backend.clip(y_pred-y_true, 0, 1)), axis=1)
    fn = backend.sum(backend.round(backend.clip(y_true-y_pred, 0, 1)), axis=1)
    # Calculando a precisao
    p = tp/(tp+fp+backend.epsilon())
    # Calculando o Recall
    r = tp/(tp+fn+backend.epsilon())
    # calculando o fbeta, tirado a média para cada classe
    bb = beta**2
    fbeta_score = backend.mean((1+bb)*(p*r)/(bb*p+r+backend.epsilon()))
    return fbeta_score

def evaluation(model, x, true):
    ypred = model.predict(x)
    return f1_score(true, ypred, average='samples')

# Creating a dictionary connecting a numeric value to each label
def create_tag_map(mapping_csv):
    labels = set()
    for i in range(len(mapping_csv)):
        tags = mapping_csv['tags'][i].split(' ')
        labels.update(tags)

    labels = list(labels)
    labels.sort()
    labels_map = {labels[k]: k for k in range(len(labels))}
    inv_labels_map = {k: labels[k] for k in range(len(labels))}
    return labels_map, inv_labels_map

# Creating a dictionary with all images and their labels
def create_file_mapping(mapping_csv):
    mapping=dict() # Criamos um dicionário vazio
    for j in range(len(mapping_csv)):
        """ percorremos o dataframe inteiro, pegando cada nome da imagem
        e sua respectiva tag, então separamos a tag por espaço
        e dizemos que o nome da tag é igual a sua tag, isso cria o dicionário!
        Agora temos multilabels para cada imagem.
        """
        name, tags = mapping_csv['image_name'][j], mapping_csv['tags'][j]
        mapping[name] = tags.split(' ')
    return mapping

