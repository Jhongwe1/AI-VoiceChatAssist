from faster_whisper import WhisperModel

class WhisperTranscriber:
    def __init__(self, model_size="small"):
        self.model = WhisperModel(model_size, device="cuda", compute_type="int8")

    def transcribe(self, file_path):
        segments, _ = self.model.transcribe(file_path, language="zh")
        for seg in segments:
            yield seg.text, seg.start, seg.end
