import whisper
import pyaudio

# 載入模型（選擇 base 或 small 以平衡速度與精度）
model = whisper.load_model("base")

# 即時音訊流處理
audio_stream = pyaudio.PyAudio().open(
    format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024
)

while True:
    audio_chunk = audio_stream.read(1024)
    result = model.transcribe(audio_chunk, language="zh")
    print(result["text"])
