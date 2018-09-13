import numpy as np
from PIL import Image
# Keras
import keras
from keras import backend as K
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.metrics import sparse_categorical_crossentropy
from keras.preprocessing import image
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Input

# Classifier settings
#====================================================#
NUM_CLASSES     = 2
LEARNING_RATE   = 0.0001
EPOCHS          = 10
BATCH_SIZE      = 16
DENSE_UNITS     = 100
TRAINING_DATA   = [] # XS Example array to be trained
TRAINING_LABELS = [] # YS Label array
predict         = False
train           = False
result          = None

def prepare_frame(spectogram):
    # convert array to image and ready for keras
    img = Image.fromarray(spectogram, 'RGB')
    img = img.resize((125,125))
    img_array = np.array(img)
    img_array_extended = np.expand_dims(img_array, axis=0).astype('float32')
    return img_array_extended

def addExample(example, label):
    # add examples to training dataset
    encoded_y = keras.utils.np_utils.to_categorical(label,num_classes=NUM_CLASSES) # make one-hot
    TRAINING_LABELS.append(encoded_y[0])
    TRAINING_DATA.append(example[0])
    print('add example for label %d'%label)

def createModel():
    # create a keras classifier
    model = Sequential()
    model.add(Flatten(return_sequences=True, input_shape = (125, 125, 3))) # should be (7,7,256)
    model.add(Dense(units = DENSE_UNITS, activation = 'relu', use_bias = True))
    model.add(Dense(units = NUM_CLASSES, activation = 'softmax', use_bias = False)) # NUMBER OF CLASSES
    return model