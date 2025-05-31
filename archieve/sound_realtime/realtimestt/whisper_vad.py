import webrtcvad
import pyaudio
import whisper

vad = webrtcvad.Vad(2)  # 靈敏度2
model = whisper.load_model("base")

# 持續錄音，偵測語音段落
def record_and_transcribe():
    while True:
        audio_chunk = record_until_silence(vad)
        if audio_chunk:
            result = model.transcribe(audio_chunk, language='zh')
            print("辨識結果:", result['text'])

record_until_silence() #需自行實作，偵測語音結束自動分段
