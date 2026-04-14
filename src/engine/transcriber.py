from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator

class TranscriberEngine:
    def __init__(self):
        self.model = WhisperModel("tiny", device="cpu", compute_type="int8")



    def transcribe(self, audio_data):
        segments, _ = self.model.transcribe(
            audio_data,
            beam_size=5,
            task="transcribe"
        )
        return "".join(segment.text for segment in segments)
        
class TranslatorEngine:

    def __init__(self):
        self.translator = GoogleTranslator(source="auto", target="es")

    def translate(self, text):
        return self.translator.translate(text)