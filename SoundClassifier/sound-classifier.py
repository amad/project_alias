import numpy as np
import time
import json
from threading import Thread

# Import modules
import sound
import ai
import connection

TRAIN_CLASS_0 = False
TRAIN_CLASS_1 = False
# Functions
#====================================================#
@connection.socketio.on('msgEvent', namespace='/socket')
def test_message(message):
    msg = message['data']
    global train
    global predict
    global TRAIN_CLASS_0
    global TRAIN_CLASS_1

    # make sure the spectogram is full before resiving commands
    if len(sound.FRAMES) >= sound.FRAMES_RANGE:

        if('class0' in msg):
            #ai.addExample(ai.prepare_frame(sound.create_spectogram()), 0)
            if TRAIN_CLASS_0:
                connection.emit('response', {'data': 'Example added to 0'})
            TRAIN_CLASS_0 = not TRAIN_CLASS_0

        if('class1' in msg):
            #ai.addExample(ai.prepare_frame(sound.create_spectogram()), 1)
            if TRAIN_CLASS_1:
                connection.emit('response', {'data': 'Example added to 1'})
            TRAIN_CLASS_1 = not TRAIN_CLASS_1

        if('train' in msg):
            predict = False
            train = True
            print('start training')
    else:
        connection.emit('response', {'data': 'Setting up'})

# Main thread
def main_thread():

    while stream.is_active():
        connection.socketio.sleep(1)
        global predict
        global result
        global train

        spectogram = sound.create_spectogram() #numpy.ndarray
        spectogram_to_list = spectogram.tolist()
        data_to_server = json.dumps({"data": spectogram_to_list})
        print spectogram_to_list
        #json.dump(b, codecs.open(json_file, 'w', encoding="utf-8"), sort_Keys=True, ident=4)
        print("NET LINE __________________________________________")
        #print spectogram
        #LIST_STR = ''.join(str(e) for e in spectogram)
        #print len(LIST_STR)
        connection.socketio.emit('response', {'data': data_to_server}, namespace='/socket')
        
        if TRAIN_CLASS_0:
            print("train on class 0")

        if TRAIN_CLASS_1:
            print("train on class 1")

    '''
    # Create a keras model
   
    model.compile(optimizer= 'adam',
                  loss= 'sparse_categorical_crossentropy',
                  metrics = ['accuracy'])

    # Main Loop 
    while stream.is_active():
        global predict
        global result
        global train

        print "hello"
        spectogram = sound.create_spectogram()
        

        if train is True:
            model.fit(np.array(ai.TRAINING_DATA),
                      np.array(ai.TRAINING_LABELS),
                      epochs=ai.EPOCHS,
                      batch_size=ai.BATCH_SIZE)
            train = False
            predict = True

        if predict is True:
            processed_image = ai.prepare_frame(spectogram)
            prediction = model.predict(processed_image)
            result = np.argmax(prediction)
            print(result)
    '''
#====================================================#

# Start audio stream
stream = sound.pa.open(format=sound.FORMAT,
                 channels=sound.CHANNELS,
                 rate=sound.RATE,
                 output=False,
                 input=True,
                 stream_callback=sound.audio_callback)
stream.start_stream() # start stream
print "hello stream is started"

# Setup and start main thread
thread = Thread(target=main_thread)
thread.daemon = True
thread.start()

# Start socket io
if __name__ == '__main__':
    connection.socketio.run(connection.app, host=connection.HOST, port=connection.PORT, debug=False)

stream.close()
pa.terminate()
