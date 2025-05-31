import pyaudio
import numpy as np
from faster_whisper import WhisperModel
from RealtimeSTT import AudioToTextRecorder

# 初始化语音识别引擎
model = WhisperModel(
    "small",
    device="cuda",
    compute_type="int8_float32"  # 或 "float32"
)
# 实时录音配置
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 480  # 30ms chunks

class RealTimeSTT:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.buffer = np.array([], dtype=np.int16)
        
    def start(self):
        def callback(in_data, frame_count, time_info, status):
            audio_chunk = np.frombuffer(in_data, dtype=np.int16)
            self.buffer = np.append(self.buffer, audio_chunk)
            
            # 每0.5秒处理一次
            if len(self.buffer) >= RATE * 0.5:
                self.process_buffer()
                
            return (None, pyaudio.paContinue)
        
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=callback
        )
        
    def process_buffer(self):
        segments, _ = model.transcribe(
            self.buffer.astype(np.float32) / 32768.0,
            language="zh",
            vad_filter=True
        )
        
        for segment in segments:
            print(f"实时转录: {segment.text}")
            
        self.buffer = np.array([], dtype=np.int16)

if __name__ == "__main__":
    stt = RealTimeSTT()
    stt.start()
    print("start")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        stt.stream.stop_stream()
        stt.stream.close()
        stt.audio.terminate()
