import soundcard as sc
import numpy as np

SAMPLERATE = 16000
FRAME_DURATION = 0.03        # Analyze in 50-millisecond frames
FRAME_SIZE = int(SAMPLERATE * FRAME_DURATION)  # 800 samples por frame

SILENCE_THRESHOLD = 0.04    # RMS min of 0.01 for silence
SILENCE_FRAMES = 14           # Consecutive silent frames to be cut (~400ms)
MAX_DURATION = 5          # Max of 7 seconds per chunk to avoid huge buffers
MIN_DURATION = 0.3         # Min of 0.5 seconds to avoid too short chunks


def get_system_audio_stream(samplerate=SAMPLERATE, channels=1):
    speaker = sc.default_speaker()
    mic = sc.get_microphone(speaker.id, include_loopback=True)
    return mic.recorder(samplerate=samplerate, channels=channels, blocksize=FRAME_SIZE)


def is_silent(frame: np.ndarray, threshold=SILENCE_THRESHOLD) -> bool:

    rms = np.sqrt(np.mean(frame ** 2))
    return rms < threshold


def capture_chunk(recorder) -> np.ndarray | None:
    frames = []
    silent_count = 0
    total_frames = 0
    max_frames = int(MAX_DURATION * SAMPLERATE)
    min_frames = int(MIN_DURATION * SAMPLERATE)
    speaking = False

    while True:
        frame = recorder.record(numframes=FRAME_SIZE)

      
        if frame.ndim > 1:
            frame = np.mean(frame, axis=1)
        frame = frame.astype(np.float32)

        silence = is_silent(frame)

        if not speaking:
            if not silence:
                
                speaking = True
                frames.append(frame)
                total_frames += len(frame)
        else:
            frames.append(frame)
            total_frames += len(frame)

            if silence:
                silent_count += 1
            else:
                silent_count = 0  

        
            if total_frames >= min_frames and silent_count >= SILENCE_FRAMES:
                break

            
            if total_frames >= max_frames:
                break

    if not frames:
        return None

    return np.concatenate(frames)