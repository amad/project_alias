def initialize():
    global RESULT, BG_EXAMPLES, TR_EXAMPLES, TRAIN, PREDICT, SILENCE, SPECTOGRAM_FULL, SPECTOGRAM_FULL_FFT

    TRAIN       = False
    PREDICT     = False
    RESULT      = 3
    BG_EXAMPLES = 0
    TR_EXAMPLES = 0
    SILENCE		= False
    SPECTOGRAM_FULL = False
    SPECTOGRAM_FULL_FFT = False