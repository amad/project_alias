# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import time
from threading import Thread

# Import modules
from modules import globals
from modules import connection
from modules import sound
from modules import ai

TRAIN   = False
PREDICT = False

# TO DO
#====================================================#
# - Make spectrogram have fine adjustment (tore)
#       - fixed range fro voice freq
# - Use globals.py for all global variables (bjørn)
# - Test on rpi3 and others (bjørn + tore)
# - Make a silence detection that -> do nut run librosa or keras while true - (tore) *****DONE*****
# - Make code lighter for low cpu/memory boards (bjørn + tore)
#       - test minimal audio preprocessing
#       - test minimal keras settings
#       -
# - create play audio module (voices and noise) - (bjørn)

# Functions
#====================================================#
@connection.socketio.on('msgEvent', namespace='/socket')
def test_message(message):
    msg = message['data']
    global TRAIN
    global PREDICT

    # make sure the spectogram is full before resiving commands
    if (sound.SPECTOGRAM_FULL):

        if('class0' in msg):
            example = ai.prepare_data(sound.get_spectrogram())
            ai.addExample(example,0)

        if('class1' in msg and globals.micOn):
            example = ai.prepare_data(sound.get_spectrogram())
            ai.addExample(example,1)

        if('train' in msg):
            PREDICT = False
            TRAIN = True

# Main thread
def main_thread():
    global TRAIN
    global PREDICT
    global RESULT

    # setup keras model
    model = ai.create_model()
    model.compile(optimizer= 'adam',loss= 'binary_crossentropy',metrics = ['accuracy'])
    model.summary()

    while stream.is_active():

        time.sleep(0.03)
        print globals.micOn
        if(globals.micOn): #when TRUE DO THE MAGIC 
          sound.make_spectrogram();
        else:
          globals.result = 0

        # print('------------------------------------')
        if TRAIN and sound.SPECTOGRAM_FULL:
          #pause sound while traning
          print('start training')
          model.fit(np.array(ai.TRAINING_DATA),
                    np.array(ai.TRAINING_LABELS),
                    epochs=ai.EPOCHS,
                    batch_size=ai.BATCH_SIZE)
          TRAIN = False
          PREDICT = True

        elif PREDICT and sound.SPECTOGRAM_FULL and globals.micOn:
          sample = ai.prepare_data(sound.get_spectrogram())
          sample_extended = np.expand_dims(sample, axis=0).astype('float32')
          prediction = model.predict(sample_extended)
          globals.result = np.argmax(prediction)

print "================================================================="

globals.initialize()
# Start audio stream
stream = sound.pyaudio.PyAudio().open(format=sound.FORMAT,
                 channels=sound.CHANNELS,
                 rate=sound.RATE,
                 output=False,
                 input=True,
                 stream_callback=sound.audio_callback)

stream.start_stream() # start stream

print "================================================================="

# Setup and start main thread
thread = Thread(target=main_thread)
thread.daemon = True
thread.start()

# Start socket io
if __name__ == '__main__':
    connection.socketio.run(connection.app, host=connection.HOST, port=connection.PORT, debug=False, log_output=False)

stream.close()
sound.pyaudio.terminate()
