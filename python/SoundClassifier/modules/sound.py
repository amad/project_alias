import numpy as np
from modules import globals

# Audio
import pyaudio
import matplotlib.pyplot as plt
import librosa
import librosa.display
import wave
import time


# Audio settings
#====================================================#
CHUNK               = 1024
FORMAT              = pyaudio.paInt16 #paFloat32
CHANNELS            = 1
RATE                = 44100
WAVE_FILENAME       = 'temp.wav'
RECORD_SECONDS      = 2
#FRAMES_RANGE   = int(RATE / xCHUNK * RECORD_SECONDS)
FRAMES_RANGE        = 32 # the same as Y-axe values for convinience
SPECTOGRAM_FULL     = False
RUNNING_SPECTOGRAM  = np.empty([1,FRAMES_RANGE], dtype=np.int16) # array to store thespectogram
FRAME               = np.empty([CHUNK], dtype=np.int16) # frames to fill up spectogram
PREVIOUS_SEC        = 0

def audio_callback(in_data, frame_count, time_info, flag):
    global FRAME
    audio_data = np.fromstring(in_data, dtype=np.int16)
    mic_thresh(audio_data)
    FRAME = audio_data #store the new chunk in global array.
    return None, pyaudio.paContinue

def mic_thresh(volume):
    # Make threshold for microphone
    global PREVIOUS_SEC 
    current_sec = time.time() % 60
    if(np.max(volume) > 2000):
        PREVIOUS_SEC  = current_sec
    if(current_sec - PREVIOUS_SEC  < 0.7):
        globals.micOn = True;
    else:
        globals.micOn = False

def process_sound(): 
    # creates a temp wav file with a single frame
    waveFile = wave.open(WAVE_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(pyaudio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(FRAME)
    waveFile.close()

    # load wav file into librosa
    y, sr = librosa.load(WAVE_FILENAME)
    S = librosa.feature.melspectrogram(y, sr=sr, power=2, fmax=8000, n_mels=FRAMES_RANGE)
    NEW_CHUNK = librosa.power_to_db(S, ref=np.max) #Store procced sound chunk
    return NEW_CHUNK

def get_spectrogram():
    global RUNNING_SPECTOGRAM
    return RUNNING_SPECTOGRAM

def make_spectrogram():
    global RUNNING_SPECTOGRAM
    global SPECTOGRAM_FULL

    y_chunk_shaped = np.reshape(process_sound(),(1, FRAMES_RANGE)) #Reshape array structore to fit the final spectogram array
    RUNNING_SPECTOGRAM = np.vstack([y_chunk_shaped,RUNNING_SPECTOGRAM]) #Stack the new sound chunk infront in the specrtogram array.
    if(len(RUNNING_SPECTOGRAM) > FRAMES_RANGE): #see if array is full
        RUNNING_SPECTOGRAM = np.delete(RUNNING_SPECTOGRAM,len(RUNNING_SPECTOGRAM)-1,axis = 0) #remove the oldes chunk
        SPECTOGRAM_FULL = True
    return RUNNING_SPECTOGRAM
