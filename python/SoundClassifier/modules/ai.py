import numpy as np
from PIL import Image
from modules import globals

# Keras
import keras
from keras import backend as K
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing import image
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Input, Dropout
from keras.layers.convolutional import Conv1D, Conv2D, MaxPooling2D

# Classifier settings
#====================================================#
NUM_CLASSES     = 2
LEARNING_RATE   = 0.0001
EPOCHS          = 10
BATCH_SIZE      = 8 # or 16
DENSE_UNITS     = 128
TRAINING_DATA   = [] # XS Example array to be trained
TRAINING_LABELS = [] # YS Label array
RESULT          = None

def addExample(example, label):
    # add examples to training dataset
    encoded_y = keras.utils.np_utils.to_categorical(label,num_classes=NUM_CLASSES) # make one-hot
    TRAINING_LABELS.append(encoded_y)
    TRAINING_DATA.append(example)
    globals.examples = len(TRAINING_DATA) # store amount of examples for client
    print('add example for label %d'%label)

def prepare_data(spectogram):
    spectogram_array_extended = np.expand_dims(spectogram, axis=0)
    return spectogram_array_extended

def create_model():
    model = Sequential()
    model.add(Conv2D(32, kernel_size = (3,3), input_shape = (1, 32, 32), data_format='channels_first'))
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
    return model
