import numpy as np
from modules import globals

# Audio
import os
import pyaudio
import wave
import time
import threading

# Audio settings
#====================================================#
CHUNK               = 1024
FORMAT              = pyaudio.paInt16
CHANNELS            = 1
RATE                = 16000
SPECTOGRAM_LEN      = 33
FRAMES_RANGE        = 20 # the same as Y-axe values for convinience
RUNNING_SPECTOGRAM  = np.empty([1,FRAMES_RANGE], dtype=np.int16) # array to store thespectogram
FINISHED_SPECTOGRAM = np.empty([1,FRAMES_RANGE], dtype=np.int16) # array to store thespectogram
FRAME               = np.empty([CHUNK], dtype=np.int16) # frames to fill up spectogram

def initialize():
    return pyaudio.PyAudio().open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     output=False,
                     input=True,
                     stream_callback=audio_callback)

# Callback on mic input
def audio_callback(in_data, frame_count, time_info, flag):
    global FRAME
    audio_data = np.fromstring(in_data, dtype=np.int16)
    mic_thresh(audio_data)
    FRAME = audio_data #store the new chunk in global array.
    return None, pyaudio.paContinue


# Make threshold for microphone
prev_sec = 0
def mic_thresh(volume):
    global prev_sec
    current_sec = time.time()
    if(np.max(volume) > 5500):
        globals.MIC_TRIGGER = True
        prev_sec  = current_sec


# Callback on mic input
pre_emphasis = 0.97
NFFT = 512
nfilt = FRAMES_RANGE

def create_mfcc(data):
    frames = np.append(data[0],data[1:] - pre_emphasis * data[:-1])
    frames = frames*np.hamming(len(data))
    mag_frames = np.absolute(np.fft.rfft(frames, NFFT))  # Magnitude of the FFT
    pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))  # Power Spectrum
    low_freq_mel = 100
    high_freq_mel = (8000 * np.log10(1 + (RATE / 2) / 700))  # Convert Hz to Mel
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
    hz_points = (700 * (10**(mel_points / 8000) - 1))  # Convert Mel to Hz
    bin = np.floor((NFFT + 1) * hz_points / RATE)

    fbank = np.zeros((nfilt, int(np.floor(NFFT / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])   # left
        f_m = int(bin[m])             # center
        f_m_plus = int(bin[m + 1])    # right

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = np.dot(pow_frames, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = 20 * np.log10(filter_banks)  # dB
    filter_banks -= (np.mean(filter_banks, axis=0) + 1e-8)
    return filter_banks


# Update spectogram and toogle when ready 
def make_spectrogram():
    global RUNNING_SPECTOGRAM
    global FINISHED_SPECTOGRAM
    new_array = (create_mfcc(FRAME));
    RUNNING_SPECTOGRAM = np.vstack([new_array,RUNNING_SPECTOGRAM]) #Stack the new sound chunk infront in the specrtogram array.
    if(len(RUNNING_SPECTOGRAM) > SPECTOGRAM_LEN): #see if array is full
        FINISHED_SPECTOGRAM = RUNNING_SPECTOGRAM
        RUNNING_SPECTOGRAM= np.empty([1,FRAMES_RANGE], dtype=np.int16)  #remove the oldes chunk
        globals.SPECTOGRAM_FULL = True 
        globals.EXAMPLE_READY = True  
        globals.MIC_TRIGGER = False         

# Updates and returns the finished spectogram
def get_spectrogram():
    global FINISHED_SPECTOGRAM
    globals.EXAMPLE_READY = False
    return FINISHED_SPECTOGRAM

# Update and returns the live stream 
def get_spectrogram_spec():
    global RUNNING_SPECTOGRAM
    globals.SPECTOGRAM_FULL = False
    return RUNNING_SPECTOGRAM





# Audio player class
#====================================================#

class audioPlayer(threading.Thread) :
    CHUNK = 1024

    def __init__(self,filepath,loop,name) :
        super(audioPlayer, self).__init__()
        self.filepath = os.path.abspath(filepath)
        self.loop = loop
        self.name = name
        self.canPlay = loop
    
    def run(self):

        # Open Wave File and start play!
        print("try to play" + self.filepath)
        wf = wave.open(self.filepath, 'rb')
        player = pyaudio.PyAudio()
        # Open Output Stream (basen on PyAudio tutorial)
        stream = player.open(format = player.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True)

        while True:
            def play_stream():
                data = wf.readframes(self.CHUNK)
                while len(data) > 0 and self.canPlay:
                    stream.write(data)
                    data = wf.readframes(self.CHUNK)
                    if len(data) <= 0:
                        print("done")
                        wf.rewind()
                        if self.loop:
                            play_stream()

            play_stream()

        stream.close()
        player.terminate()

    def play(self):
        print("play " + self.name)
        self.canPlay = True

    def stop(self):
        print("stop " + self.name)
        self.canPlay = False


