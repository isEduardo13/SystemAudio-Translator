import threading
import numpy as np
from engine.audio_capture import get_system_audio_stream, capture_chunk
from engine.audio_queue import enqueue_audio, dequeue_audio, enqueue_text, dequeue_text
from engine.transcriber import TranslatorEngine
from engine.transcriber import TranscriberEngine
stop_event = threading.Event()

def capture_loop(mic):
    while not stop_event.is_set():
        chunk = capture_chunk(mic, duration=4)
        if np.abs(chunk).mean() < 0.001:
            continue
        enqueue_audio(chunk)

def process_loop(engine):   
    while not stop_event.is_set():
        chunk = dequeue_audio(timeout=1)  
        if chunk is None:
            continue
        result = engine.translate_audio(chunk)
        if result.strip():
            print(f"Translate: {result}")
def whisper_loop(transcriber):

    while not stop_event.is_set():
        chunk = dequeue_audio(timeout=1)
        if chunk is None:
            continue
        text = transcriber.transcribe(chunk)
        if text.strip():
            enqueue_text(text)

def translate_loop(translator):
  
    while not stop_event.is_set():
        text = dequeue_text(timeout=1)
        if text is None:
            continue
        result = translator.translate(text)
        if result.strip():
            print(f"Translate: {result}")
def main():
    print("beginning...")
    transcriber = TranscriberEngine()
    translator = TranslatorEngine()

    with get_system_audio_stream() as mic:
        print("Listening... (Ctrl+C para salir)")

        threads = [
            threading.Thread(target=capture_loop,   args=(mic,),        daemon=True),
            threading.Thread(target=whisper_loop,   args=(transcriber,), daemon=True),
            threading.Thread(target=translate_loop, args=(translator,),  daemon=True),
        ]

        for t in threads:
            t.start()

        try:
            while True:
                stop_event.wait(timeout=0.5)
        except KeyboardInterrupt:
            print("\n Stopping...")
            stop_event.set()

        for t in threads:
            t.join(timeout=3)
        print("Finished.")

if __name__ == "__main__":
    main()