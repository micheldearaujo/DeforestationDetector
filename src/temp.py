from utilities import *


targ_shape = (128, 128, 3)
dataset_name = 'amazon_data_%s.npz'%(targ_shape[0])
opt = SGD(lr=0.01, momentum=0.9)

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
    modelo.compile(optimizer=opt, loss='binary_crossentropy', metrics=[fbeta])
    return modelo

modelo = define_model()
model_name = 'cnn_%s_SGD.h5' % (targ_shape[0])
modelo.load_weights(base_dir+'/'+model_name)

modelo.save(base_dir+'/' + 'cnn_%s_SGD_new.h5')