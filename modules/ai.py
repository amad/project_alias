import numpy as np
from modules import globals

# Keras
import keras
from keras import backend as K
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Input, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D

# Classifier settings
#====================================================#
NUM_CLASSES     = 2
LEARNING_RATE   = 0.0001
EPOCHS          = 10
BATCH_SIZE      = 8
DENSE_UNITS     = 128
TRAINING_DATA   = [] # XS Example array to be trained
TRAINING_LABELS = [] # YS Label array
RESULT          = None

model = Sequential()

def addExample(sample, label):
    # add examples to training dataset
    sample = np.expand_dims(sample, axis=0)
    print sample.shape
    encoded_y = keras.utils.np_utils.to_categorical(label,num_classes=NUM_CLASSES) # make one-hot
    TRAINING_LABELS.append(encoded_y)
    TRAINING_DATA.append(sample)
    print('add example for label %d'%label)

def prepare_data(spectogram):
    spectogram_array_extended = np.expand_dims(spectogram, axis=0)
    return spectogram_array_extended

def create_model():
    global model
    model.add(Conv2D(32, kernel_size = (3,3), input_shape = (1, 25, 25), data_format='channels_first'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Conv2D(filters = 16, kernel_size = (3,3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Conv2D(filters = 32, kernel_size = (3,3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(rate = 0.2))
    model.add(Flatten())
    model.add(Dense(units = DENSE_UNITS, activation = 'relu'))
    model.add(Dropout(rate = 0.5))
    model.add(Dense(units = NUM_CLASSES, activation = 'softmax'))
    model.compile(optimizer= 'adam',loss= 'binary_crossentropy',metrics = ['accuracy'])

def train_model():
    global model
    model.fit(np.array(TRAINING_DATA),
        np.array(TRAINING_LABELS),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE)
    #model.save('alias.h5')

def predict(sample):
    global model
    sample = np.expand_dims(sample, axis=0)
    sample_extended = np.expand_dims(sample, axis=0)
    prediction = model.predict(sample_extended)
    return np.argmax(prediction)

def save_model():
    global model
    model.save('alias.h5')

def load_model():
    return load_model('alias.h5')
