import os
import time
import queue
import threading
import wave
import numpy as np
import pyaudio
from vosk import Model, KaldiRecognizer

# 載入 Vosk 模型（自動指定）
MODEL_PATH = "C:/Users/Key20/Desktop/vosk-model-small-cn-0.22"
model = Model(MODEL_PATH)

# 音訊參數
RATE = 16000
CHANNELS = 1
CHUNK = 1024
SILENCE_THRESHOLD = 300  # 音量小於此視為靜音
MAX_SILENCE_CHUNKS = 10  # 停頓多少個 chunk 算作一句話結束

# 佇列：儲存音訊片段
audio_queue = queue.Queue()

# Recorder 執行緒（Producer）
def audio_producer():
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     frames_per_buffer=CHUNK)
    print("🎤 錄音開始，請說話...")

    frames = []
    silence_count = 0
    voice_frame_count = 0
    start_time = time.time()

    while True:
        data = stream.read(CHUNK)
        audio = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio).mean()

        frames.append(data)

        if volume < SILENCE_THRESHOLD:
            silence_count += 1
        else:
            silence_count = 0
            voice_frame_count += 1

        if silence_count > MAX_SILENCE_CHUNKS:
            if voice_frame_count > 3:  # 有實際講話才送出
                timestamp = time.strftime("%H:%M:%S", time.localtime(start_time))
                audio_queue.put((b''.join(frames), timestamp))
                print(f"\n⏱ 段落偵測（有講話） ➜ {timestamp}")
            #else:
                #print(f"\n💤 段落為靜音，略過")

            # 重置
            frames = []
            start_time = time.time()
            silence_count = 0
            voice_frame_count = 0

# Consumer 處理語音（可開多執行緒）
def audio_consumer(worker_id):
    while True:
        audio_data, timestamp = audio_queue.get()
        recognizer = KaldiRecognizer(model, RATE)
        recognizer.AcceptWaveform(audio_data)
        result = recognizer.Result()
        import json
        text = json.loads(result).get("text", "")
        if text.strip():
            print(f"\n🧠 [{timestamp}] Worker-{worker_id} 辨識結果：\n{text}\n")
        else:
            print(f"\n❓ [{timestamp}] Worker-{worker_id} 無法辨識內容。")

# 啟動系統
if __name__ == "__main__":
    # 啟動錄音執行緒
    threading.Thread(target=audio_producer, daemon=True).start()

    # 啟動多個語音辨識 Worker 執行緒
    for i in range(2):  # 可以依硬體能力調整 worker 數量
        threading.Thread(target=audio_consumer, args=(i+1,), daemon=True).start()

    while True:
        time.sleep(1)
