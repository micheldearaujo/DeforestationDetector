"""
Convolutional Neural Network to classify Amazon dataset

Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""

# Importing the library
from utilities import *

# Definind the hyparams
targ_shape = (128, 128, 3)
dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
opt = SGD(lr=0.01, momentum=0.9)

# Creating the CNN model, using VGG Blocks
# Three blocks of two 3x3 convolutions and a 2x2 MaxPooling2D
def define_model(in_shape=targ_shape, out_shape=17):
    modelo = Sequential()
    modelo.add(Conv2D(int(targ_shape[0]/4), (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=targ_shape))
    modelo.add(Conv2D(int(targ_shape[0]/4), (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
    modelo.add(MaxPooling2D((2, 2)))
    modelo.add(Conv2D(int(targ_shape[0]/2), (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
    modelo.add(Conv2D(int(targ_shape[0]/2), (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
    modelo.add(MaxPooling2D((2, 2)))
    modelo.add(Conv2D(targ_shape[0], (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
    modelo.add(Conv2D(targ_shape[0], (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
    modelo.add(MaxPooling2D((2, 2)))
    modelo.add(Flatten())
    modelo.add(Dense(targ_shape[0], activation='relu', kernel_initializer='he_uniform'))
    modelo.add(Dense(out_shape, activation='sigmoid'))
    # Compilando
    # Carregando os weights em caso de interrupção anterior:
    modelo.compile(optimizer=opt, loss='binary_crossentropy', metrics=[fbeta])
    return modelo

# Plotting the training results
def resumo(modelohis):
    # Plotando o loss
    plt.subplot(211)
    plt.title('Cross Entropy Loss')
    plt.plot(modelohis.history['loss'], color='blue', label='Training Loss')
    plt.plot(modelohis.history['val_loss'], color='orange', label='Validation Loss')
    plt.legend()
    # Plotting accuracy
    plt.subplot(212)
    plt.title('Fbeta Score')
    plt.plot(modelohis.history['fbeta'], color='blue', label='Training Fbeta')
    plt.plot(modelohis.history['val_fbeta'], color='orange', label='Validation Fbeta')
    plt.legend()
    # saving the plot
    filename = sys.argv[0].split('/')[-1]
    plt.tight_layout()
    plt.savefig(base_dir+'/'+filename + '_plot_%s_SGD.png'%(targ_shape[0]))
    plt.close()

# Executing the model
def run():
    # Load
    Xtr, Xval, ytr, yval = load_dataset_DL(dataset_name)
    # Creating the data augmentation
    train_datagen = ImageDataGenerator(rescale=1.0/255.0,
                                       horizontal_flip=True,
                                       vertical_flip=True,
                                       rotation_range=90)

    # The test images are only reescaled

    val_datagen = ImageDataGenerator(rescale=1.0/255.0)

    # Applying the iterators
    # Here is created the arrays who will feed the model
    # The Xtr and Xte arrays will become the iterators
    # train_it and val_it are the new Xtr and Xte
    train_it = train_datagen.flow(Xtr, ytr, batch_size=targ_shape[0])
    val_it = val_datagen.flow(Xval, yval, batch_size=targ_shape[0])
    #test_it = test_datagen.flow(Xte, yte, batch_size=targ_shape[0])

    # Building the model
    model = define_model()
    model_name = 'cnn_%s_SGD.h5' % (targ_shape[0])
    checkpoint = ModelCheckpoint(base_dir+'/'+model_name, monitor='loss', save_best_only=True,
                                 mode='min', save_freq=1, save_weights_only=True)
    early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=25)


    # Fitting
    start_time = time.monotonic()
    modelfit = model.fit(train_it,
                                     steps_per_epoch=len(train_it),
                                     validation_data=val_it,
                                     validation_steps=len(val_it),
                                     epochs=200,
                                     verbose=1,
                           callbacks=[early_stop,checkpoint])
    # Avaliando o modelo
    loss, fbeta = model.evaluate(val_it,
                                            steps=len(val_it),
                                            verbose=1)
    end_time = time.monotonic()
    tempo = timedelta(seconds=end_time - start_time)

    print('> loss=%.3f, fbeta=%.3f'%(loss, fbeta))

    # Saving the model
    model_name = 'cnn_%s_SGD_ts.h5'%(targ_shape[0])
    # Salvando o modelo para futuras previsoes
    model.save(base_dir+'/'+model_name)
    # Plotando as curvas de aprendizado
    resumo(modelfit)


    file = open(base_dir + '/' + 'cnn_training.txt', 'a')
    file.write('Image Size: %s\n' % targ_shape[0])
    file.write('Training time: %s\n' % tempo)
    file.write('Loss: %s\n' % loss)
    file.write('Fbeta_score: %s\n' % fbeta)
    file.write('----------------------------------------------------\n')
    file.close()
    print('Tempo do treinamento: ')
    print(tempo)

    return loss, fbeta



# Running everyting
loss, fbeta = run()


