import threading
import numpy as np
from engine.audio_capture import get_system_audio_stream, capture_chunk
from engine.audio_queue import enqueue_audio, dequeue_audio, enqueue_text, dequeue_text
from engine.transcriber import TranslatorEngine
from engine.transcriber import TranscriberEngine
from ui_overlay import TranslationOverlay
stop_event = threading.Event()

def capture_loop(mic):
   
    while not stop_event.is_set():
        chunk = capture_chunk(mic) 
        if chunk is None:
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

def translate_loop(translator, overlay):
    buffer = ""
    while not stop_event.is_set():
        text = dequeue_text(timeout=0.3)
        
        if text is None:
            
            if buffer.strip():
                result = translator.translate(buffer.strip())
                if result.strip():
                    overlay.update_text(result)
                buffer = ""
            continue
        
        buffer += " " + text  
        
       
        if any(buffer.rstrip().endswith(p) for p in [".", "?", "!", "..."]):
            result = translator.translate(buffer.strip())
            if result.strip():
                overlay.update_text(result)
            buffer = ""
def main():
    overlay = TranslationOverlay()
    transcriber = TranscriberEngine()
    translator = TranslatorEngine()

    with get_system_audio_stream() as mic:
        threads = [
            threading.Thread(target=capture_loop,   args=(mic,),                   daemon=True),
            threading.Thread(target=whisper_loop,   args=(transcriber,),            daemon=True),
            threading.Thread(target=translate_loop, args=(translator, overlay),     daemon=True), 
        ]
        for t in threads:
            t.start()

        overlay.run()
        stop_event.set() 


if __name__ == "__main__":
    main()