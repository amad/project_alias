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
import atexit

LED = led.Pixels()
LED.off()

#Initialize the sound objects
noise = sound.audioPlayer("data/noise.wav",-1,"noise",True)
wakeup = sound.audioPlayer("data/ok_google.wav",0,"wakeup", False)

# TO DO
#====================================================#
# - Send single frame auido data to client, to make a beautiful vizz
# - Create and save a big dataset for background sounds.

# Functions
#====================================================#
@connection.socketio.on('msgEvent', namespace='/socket')
def test_message(message):
    msg = message['data']
    globals.PREDICT = False

    #Add example to class 0 - Silence / background noise
    if('class0' in msg and globals.EXAMPLE_READY):
        example = sound.get_spectrogram()
        ai.addExample(example,0)
        globals.BG_EXAMPLES += 1
        LED.listen()
        connection.send_response()

    #Add example to class 1 - WakeWord
    elif('class1' in msg and globals.EXAMPLE_READY and not globals.UPDATE_BG_DATA):
        example = sound.get_spectrogram()
        ai.addExample(example,1)
        globals.TR_EXAMPLES += 1
        LED.listen()
        connection.send_response()

    #Receive train command
    elif('train' in msg):
        globals.PREDICT = False
        globals.TRAIN = True
        connection.send_response()  

    #Receive reset command
    elif('reset' in msg):
        globals.RESET = True;   
        connection.send_response()  
        ai.reset_model()
        globals.RESET = False; 
        globals.TR_EXAMPLES = 0
        globals.PREDICT = True
        connection.send_response()

    #Receive is Button is pressed or released
    if('btn_release' in msg):
        globals.BUTTON_PRESSED = False
    else:
        globals.BUTTON_PRESSED = True


# Main thread
def main_thread():
    # setup keras model
    globals.PREDICT = ai.create_model()
    connection.send_response()
    triggered = False
    prev_timer = 0;
    interval = 5;
    noise.play()


    # Program loop
    while stream.is_active():
        time.sleep(0.066)
        LED.off()
        current_sec = time.time()

        # If the mic is triggered an spectogram is not done, make a row more.
        if(globals.MIC_TRIGGER and not globals.EXAMPLE_READY):
            sound.make_spectrogram()
        else:
             globals.RESULT = 0 # if silence just return 0

        #Toggle to ensure that Example state is reset in sync with button commands
        if not globals.BUTTON_PRESSED:
            globals.EXAMPLE_READY = False;
            globals.PREDICT = True


        # If the train button is hit, and there are more than 2 example go train
        if globals.TRAIN:
            ai.labels_to_model = np.array(ai.TRAINING_LABELS)
            ai.data_to_model = np.array(ai.TRAINING_DATA)
            print(ai.labels_to_model.shape)
            print(ai.data_to_model.shape)
            ai.train_model()
            globals.TRAIN = False
            globals.PREDICT = True
            connection.send_response()  

        # If train is done, and a new finished frame is ready, go predict it.
        elif globals.PREDICT and globals.EXAMPLE_READY:
            sample = sound.get_spectrogram()
            globals.RESULT = ai.predict(sample).item()

            if globals.RESULT  == 1:
                noise.stop()
                wakeup.play()
                LED.on()
                triggered = True
                globals.PREDICT = False
                prev_timer = current_sec

        else:
            globals.RESULT = 0


        if current_sec - prev_timer > interval:
            if triggered:
                noise.play()
                print("start noise")
                LED.off()
                triggered = False;
                globals.PREDICT = True

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


def exit_handler():
    #noise.close()
    LED.off()
    stream.close()
    sound.pyaudio.terminate()
atexit.register(exit_handler)
