import queue

AUDIO_QUEUE = queue.Queue(maxsize=5)
TEXT_QUEUE = queue.Queue(maxsize=10)

def enqueue_audio(chunk):
    try:
        AUDIO_QUEUE.put_nowait(chunk)
    except queue.Full:
        AUDIO_QUEUE.get_nowait()
        AUDIO_QUEUE.put_nowait(chunk)

def dequeue_audio(timeout=1):
    try:
        return AUDIO_QUEUE.get(timeout=timeout)
    except queue.Empty:
        return None

def enqueue_text(text):
    TEXT_QUEUE.put_nowait(text)

def dequeue_text(timeout=1):
    try:
        return TEXT_QUEUE.get(timeout=timeout)
    except queue.Empty:
        return None