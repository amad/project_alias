# coding=utf-8
import numpy as np
import time
from threading import Thread

# Import modules
from modules import globals
from modules import connection
from modules import sound
from modules import ai
from modules import led

TRAIN   = False
PREDICT = False

LED = led.Pixels()
LED.off()

#Initialize the sound objects 
#noise = sound.audioPlayer("data/noise.wav",True,"noise")
#wakeup = sound.audioPlayer("data/ok_google.wav",False,"wakeup")


# TO DO
#====================================================#
# - create play audio module (voices and noise) - (bjørn)
# - Send single frame auido data to client, to make a beautiful vizz 
# - Create and save a big dataset for background sounds.
# - Load in the dataset in beinning of sketch (when above is done)

# Functions
#====================================================#
@connection.socketio.on('msgEvent', namespace='/socket')
def test_message(message):
    msg = message['data']
    global TRAIN
    global PREDICT
        
    PREDICT = False
    #noise.stop()
    #wakeup.stop()
    if('class0' in msg and globals.EXAMPLE_READY):
        example = sound.get_spectrogram()
        ai.addExample(example,0)
        globals.BG_EXAMPLES += 1
        LED.listen()
    elif('class1' in msg and globals.EXAMPLE_READY and not globals.UPDATE_BG_DATA):
        example = sound.get_spectrogram()
        ai.addExample(example,1)
        globals.TR_EXAMPLES += 1
        LED.listen()
    elif('train' in msg):
        PREDICT = False
        TRAIN = True
    elif('reset' in msg):
        print("reset model")
        ai.reset_model()
        globals.TR_EXAMPLES = 0
        PREDICT = True


# Main thread
def main_thread():
    global TRAIN
    global PREDICT
    global RESULT

    # setup keras model
    PREDICT = ai.create_model()
    print(PREDICT)

    # Start the sound threads
    #noise.start()
    #wakeup.start()

    triggered = False
    prev_timer = 0;
    interval = 3;

    # Program loop 
    while stream.is_active():
        time.sleep(0.03)
        LED.off()
        current_sec = time.time()

        # If the mic is triggered an spectogram is not done, make a row more. 
        if(globals.MIC_TRIGGER and not globals.SPECTOGRAM_FULL):    
            sound.make_spectrogram();
        else:
             globals.RESULT = 0 # if silence just return 0 

        # If the train button is hit, and there are more than 2 example go train
        if TRAIN:
            ai.labels_to_model = np.array(ai.TRAINING_LABELS)
            ai.data_to_model = np.array(ai.TRAINING_DATA)
            print(ai.labels_to_model.shape)
            print(ai.data_to_model.shape)
            ai.train_model()
            TRAIN = False
            PREDICT = True

        # If train is done, and a new finished frame is ready, go predict it. 
        elif PREDICT and globals.EXAMPLE_READY:
            sample = sound.get_spectrogram()
            globals.RESULT = ai.predict(sample).item()

            if globals.RESULT  == 1:
                #noise.stop()
                #wakeup.play()
                LED.on()
                print("stop noise")
                print("play wake word")
                triggered = True
                PREDICT = False
                prev_timer = current_sec

        else:
            globals.RESULT = 0


        if current_sec - prev_timer > interval:
            if triggered:
                #noise.play()
                print("start noise")
                LED.off()
                triggered = False;
                PREDICT = True

# Setup
#====================================================#

globals.initialize()
stream = sound.initialize()
stream.start_stream() # start stream

# Setup and start main thread
thread = Thread(target=main_thread)
thread.daemon = True
thread.start()

print('')
print("============================================")
print("SERVER RUNNING ON: http://" + str(connection.HOST) + ":" + str(connection.PORT))
print("============================================")
print('')

# Start socket io
if __name__ == '__main__':
    connection.socketio.run(connection.app, host=connection.HOST, port=connection.PORT, debug=False, log_output=False)

LED.off()
stream.close()
sound.pyaudio.terminate()
