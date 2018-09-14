import numpy as np
# Audio
import pyaudio
import matplotlib.pyplot as plt
import librosa
import librosa.display
import wave

# Audio settings
#====================================================#
CHUNK           = 1024
FORMAT          = pyaudio.paInt16 #paFloat32
CHANNELS        = 1
RATE            = 44100
WAVE_FILENAME   = 'file.wav'
RECORD_SECONDS  = 2
#FRAMES_RANGE   = int(RATE / xCHUNK * RECORD_SECONDS)
FRAMES_RANGE    = 100
FRAMES          = [] # frames to fill up spectogram
pa              = pyaudio.PyAudio()
TEST_DATA       = 0


def audio_callback(in_data, frame_count, time_info, flag):
    TEST_DATA = np.fromstring(in_data, dtype=np.int16)
    #triggers when resiving an audio chunk
    FRAMES.append(in_data)
    if len(FRAMES) > FRAMES_RANGE:
        del FRAMES[0] # delete oldest frame
    return None, pyaudio.paContinue


def create_spectogram():
    # creates a temp wav file and joins frames into a spectogram
    waveFile = wave.open(WAVE_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(pa.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(FRAMES))
    waveFile.close()

    print WAVE_FILENAME
    # load wav file into librosa
    y, sr = librosa.load(WAVE_FILENAME)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=25)
    log_S = librosa.amplitude_to_db(S, ref=np.max)
    return log_S