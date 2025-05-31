import os
import queue
import threading
import sounddevice as sd
import vosk
import json
import argparse

# ----------------------
# 參數設定
# ----------------------

class SpeechRecognizer:
    def __init__(self, model_path: str, lang='zh-cn', samplerate=16000, blocksize=8000):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型不存在：{model_path}")
        self.q = queue.Queue()
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, samplerate)
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.running = True

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"[⚠️ 錄音狀態] {status}", flush=True)
        self.q.put(bytes(indata))

    def _recognize_loop(self):
        while self.running:
            data = self.q.get()
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "")
                if text.strip():
                    print(f"✅ 辨識：{text}", flush=True)
            else:
                partial = json.loads(self.recognizer.PartialResult())
                partial_text = partial.get("partial", "")
                if partial_text.strip():
                    print(f"⏳ 片段：{partial_text}", end='\r', flush=True)

    def start(self):
        print("🎤 語音轉文字啟動中...（Ctrl+C 可結束）")
        threading.Thread(target=self._recognize_loop, daemon=True).start()
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=self.blocksize,
                               dtype='int16', channels=1, callback=self._audio_callback):
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                print("\n🛑 結束語音辨識")
                self.running = False

# ----------------------
# 主程式
# ----------------------

if __name__ == '__main__':
    # 直接指定模型資料夾
    MODEL_PATH = r"C:\Users\Key20\Desktop\vosk-model-small-cn-0.22"

    # 檢查模型是否存在
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"❌ 模型不存在：{MODEL_PATH}\n請先下載並放置於指定位置。")

    # 建立辨識器實例，啟動語音辨識
    recognizer = SpeechRecognizer(model_path=MODEL_PATH)
    recognizer.start()
