import numpy as np
from modules import globals

# Audio
import os
import pyaudio
import librosa
import wave
import time
import threading

# Audio settings
#====================================================#
CHUNK               = 1024
FORMAT              = pyaudio.paInt16
CHANNELS            = 1
RATE                = 44100
RECORD_SECONDS      = 2
FRAMES_RANGE        = 32 # the same as Y-axe values for convinience
RUNNING_SPECTOGRAM  = np.empty([1,FRAMES_RANGE], dtype=np.int16) # array to store thespectogram
FRAME               = np.empty([CHUNK], dtype=np.int16) # frames to fill up spectogram

def initialize():
    return pyaudio.PyAudio().open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     output=False,
                     input=True,
                     stream_callback=audio_callback)

def audio_callback(in_data, frame_count, time_info, flag):
    global FRAME
    audio_data = np.fromstring(in_data, dtype=np.int16)
    mic_thresh(audio_data)
    FRAME = audio_data #store the new chunk in global array.
    return None, pyaudio.paContinue

prev_sec = 0
def mic_thresh(volume):
    # Make threshold for microphone
    global prev_sec
    current_sec = time.time() % 60
    if(np.max(volume) > 1000):
        prev_sec  = current_sec
    if(current_sec - prev_sec  < 1.5):
        globals.SILENCE = True
    else:
        globals.SILENCE = False

def process_sound():
    # creates a temp wav file with a single frame
    waveFile = wave.open('data/temp.wav', 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(pyaudio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(FRAME)
    waveFile.close()

    # load wav file into librosa
    y, sr = librosa.load('data/temp.wav')
    S = librosa.feature.melspectrogram(y, sr=sr, power=2, fmax=8000, n_mels=FRAMES_RANGE)
    NEW_CHUNK = librosa.power_to_db(S, ref=np.max) #Store procced sound chunk
    return NEW_CHUNK

def get_spectrogram():
    global RUNNING_SPECTOGRAM
    return RUNNING_SPECTOGRAM

def make_spectrogram():
    global RUNNING_SPECTOGRAM
    y_chunk_shaped = np.reshape(process_sound(),(1, FRAMES_RANGE)) #Reshape array structore to fit the final spectogram array
    RUNNING_SPECTOGRAM = np.vstack([y_chunk_shaped,RUNNING_SPECTOGRAM]) #Stack the new sound chunk infront in the specrtogram array.
    if(len(RUNNING_SPECTOGRAM) > FRAMES_RANGE): #see if array is full
        RUNNING_SPECTOGRAM = np.delete(RUNNING_SPECTOGRAM,len(RUNNING_SPECTOGRAM)-1,axis = 0) #remove the oldes chunk
        globals.SPECTOGRAM_FULL = True

# Audio player
#====================================================#

class audioPlayer(threading.Thread) :
  CHUNK = 1024

  def __init__(self,filepath,loop=True) :
    super(audioPlayer, self).__init__()
    self.filepath = os.path.abspath(filepath)
    self.loop = loop

  def run(self):
    # Open Wave File and start play!
    wf = wave.open(self.filepath, 'rb')
    player = pyaudio.PyAudio()

    # Open Output Stream (basen on PyAudio tutorial)
    stream = player.open(format = player.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True)

    # PLAYBACK LOOP
    data = wf.readframes(self.CHUNK)
    while self.loop :
      stream.write(data)
      data = wf.readframes(self.CHUNK)
      if data == '' : # If file is over then rewind.
        wf.rewind()
        data = wf.readframes(self.CHUNK)

    stream.close()
    player.terminate()

  def play(self) :
    self.start()

  def stop(self) :
    self.loop = False
