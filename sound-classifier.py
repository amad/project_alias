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

# TO DO
#====================================================#
# - Test on rpi3 and others (bjørn + tore)
# - See what can make the code lighter
# - create play audio module (voices and noise) - (bjørn)
# - make logic so when predict changes it waits 2 secounds before predict again

# Functions
#====================================================#
@connection.socketio.on('msgEvent', namespace='/socket')
def test_message(message):
    msg = message['data']
    global TRAIN
    global PREDICT

    # make sure the spectogram is full before resiving commands
    if (globals.SPECTOGRAM_FULL):
        PREDICT = False
        if('class0' in msg):
            example = sound.get_spectrogram()
            ai.addExample(example,0)
            globals.BG_EXAMPLES += 1
            LED.listen()
        elif('class1' in msg and globals.SILENCE):
            example = sound.get_spectrogram()
            ai.addExample(example,1)
            globals.TR_EXAMPLES += 1
            LED.listen()
        elif('train' in msg):
            PREDICT = False
            TRAIN = True

# Main thread
def main_thread():
    global TRAIN
    global PREDICT
    global RESULT

    # setup keras model
    ai.create_model()

    #noise = sound.audioPlayer("data/noise.wav");
    #wakeup = sound.audioPlayer("data/noise.wav");

    trigger = False
    trigger_timer = False
    prev_timer = 0;
    interval = 1;


    while stream.is_active():
        time.sleep(0.02)
        LED.off()
        current_sec = time.time() % 60

        if(globals.SILENCE): # when TRUE do the magic!
            sound.make_spectrogram();
        else:
            globals.RESULT = 0

        if TRAIN and globals.SPECTOGRAM_FULL:
            ai.train_model()
            TRAIN = False
            PREDICT = True

        elif PREDICT and globals.SPECTOGRAM_FULL and globals.SILENCE:
            sample = sound.get_spectrogram()
            globals.RESULT = ai.predict(sample)

            if(globals.RESULT == 0 and trigger == False):
                trigger = True
            elif(globals.RESULT == 1 and trigger == True):
                print("stop noise")
                print("play wakeword")
                LED.on()
                prev_timer = current_sec
                trigger_timer = True
                trigger = False

        if(trigger_timer):
            if(current_sec - prev_timer < 3):
                PREDICT = False
            else:
                print("stop wakeword")
                print("srart noise")
                LED.off()
                trigger_timer = False
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
