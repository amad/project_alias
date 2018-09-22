import numpy as np
from modules import globals
import pyaudio
import time

# Audio settings
#====================================================#
CHUNK               = 1024
FORMAT              = pyaudio.paInt16
CHANNELS            = 1
RATE                = 44100
RECORD_SECONDS      = 2
FRAMES_RANGE        = 25 # the same as Y-axe values for convinience
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
    if(current_sec - prev_sec < 1.2):
        globals.SILENCE = True
    else:
        globals.SILENCE = False

pre_emphasis = 0.97
NFFT = 512
nfilt = FRAMES_RANGE

def create_mfcc(data):
    #frames = np.append(data[0],data[1:]-0.97 * data[:-1])
    frames = data*np.hamming(len(data))
    mag_frames = np.absolute(np.fft.rfft(frames, NFFT))  # Magnitude of the FFT
    pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))  # Power Spectrum
    low_freq_mel = 0
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

def make_spectrogram():
    global RUNNING_SPECTOGRAM
    new_array = (create_mfcc(FRAME));
    RUNNING_SPECTOGRAM = np.vstack([new_array,RUNNING_SPECTOGRAM]) #Stack the new sound chunk infront in the specrtogram array.
    if(len(RUNNING_SPECTOGRAM) > FRAMES_RANGE): #see if array is full
        RUNNING_SPECTOGRAM = np.delete(RUNNING_SPECTOGRAM,len(RUNNING_SPECTOGRAM)-1,axis = 0) #remove the oldes chunk
        globals.SPECTOGRAM_FULL = True
    #print RUNNING_SPECTOGRAM.shape

def get_spectrogram():
    global RUNNING_SPECTOGRAM
    return RUNNING_SPECTOGRAM
