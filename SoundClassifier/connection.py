# Socket I/O
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
from threading import Thread

# Socket I/O
#====================================================#
PORT            = 5000
HOST            = '0.0.0.0'
app             = Flask(__name__)
app.debug       = False
socketio        = SocketIO(app, async_mode='threading')
socket_thread   = None

# this thread is running in the background sending data to the client when connected
def response_thread():
     print 'In background_stuff'
     while True:
         socketio.sleep(0.1)
         global spectogram
         print spectogram
        # socketio.emit('response', {'data': result}, namespace='/socket')

@app.route('/')
def index():
    print('Someone Connected!')
    global socket_thread
    if socket_thread is None:
        socket_thread = Thread(target=response_thread)
        socket_thread.start()
    return render_template('index.html')
