# Socket I/O
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
from threading import Thread

import numpy as np
import json
from modules import globals
from modules import sound
import logging
import matplotlib.pyplot as plt

# Socket I/O
#====================================================#
PORT            = 5000
HOST            = '0.0.0.0'
app             = Flask(__name__)
app.debug       = False
socketio        = SocketIO(app, async_mode='threading', logger=False, engineio_logger=False)
socket_thread   = None
log             = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# this thread is running in the background sending data to the client when connected
def response_thread():
     while True:
         if sound.SPECTOGRAM_FULL:
             socketio.sleep(0.03) #speed of data transmit
             spec_as_list = sound.get_spectrogram().tolist() # convert from numpy to regular list
             spec_to_server = json.dumps(spec_as_list, indent=4) # convert list to json format
             socketio.emit('response', {'spectogram': spec_to_server, 'result': globals.result, 'examples': globals.examples}, namespace='/socket')

@app.route('/')
def index():
    print('Someone Connected!')
    global socket_thread
    if socket_thread is None:
        socket_thread = Thread(target=response_thread)
        socket_thread.start()
    return render_template('index.html')