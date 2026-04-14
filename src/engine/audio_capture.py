import soundcard as sc
import numpy as np

def get_system_audio_stream(samplerate=16000, channels=1):
    speaker = sc.default_speaker()
    mic = sc.get_microphone(speaker.id, include_loopback=True)
    return mic.recorder(samplerate=samplerate, channels=channels, blocksize=4096)

def capture_chunk(recorder, duration=3, samplerate=16000):
    numframes = samplerate * duration
    data = recorder.record(numframes=numframes)
    
    if data.ndim > 1:
        data = np.mean(data, axis=1)
    
    return data.astype(np.float32)