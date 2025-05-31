'''
import sounddevice as sd
import numpy as np
import time
import scipy.io.wavfile as wav
import os

class AudioRecorder:
    def __init__(self, queue, save_dir, silence_threshold=0.01, silence_duration=1.0, min_speech_duration=0.5):
        self.fs = 16000  # 取樣率
        self.buffer = []
        self.queue = queue
        self.save_dir = save_dir
        self.recording = False
        self.silence_threshold = silence_threshold  # 音量閾值（RMS）
        self.silence_duration = silence_duration  # 靜音持續時間（秒）
        self.min_speech_duration = min_speech_duration  # 最小語音片段長度（秒）
        self.silence_start = None
        self.speech_start = None

        # 確保保存目錄存在
        os.makedirs(save_dir, exist_ok=True)

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"錄音錯誤: {status}")
            return

        # 計算音量（使用 RMS）
        volume = np.sqrt(np.mean(indata ** 2))
        now = time.time()

        if volume > self.silence_threshold:
            # 檢測到語音
            if self.speech_start is None:
                self.speech_start = now  # 記錄語音開始時間
            self.buffer.append(indata.copy())
            self.silence_start = None
        elif self.buffer:
            # 檢測到靜音且緩衝區有數據
            if self.silence_start is None:
                self.silence_start = now
            elif now - self.silence_start > self.silence_duration:
                # 靜音持續時間超過閾值，檢查語音長度是否足夠
                speech_duration = (now - self.speech_start) if self.speech_start else 0
                if speech_duration >= self.min_speech_duration:
                    self.save_buffer()
                else:
                    print(f"語音片段過短 ({speech_duration:.2f}秒)，忽略")
                    self.buffer = []
                    self.speech_start = None
                    self.silence_start = None

    def save_buffer(self):
        if not self.buffer:
            return

        try:
            audio_data = np.concatenate(self.buffer)
            audio_data = (audio_data * 32767).astype(np.int16)  # 轉換為 16 位整數
            filename = os.path.join(self.save_dir, f"speech_{int(time.time())}.wav")
            wav.write(filename, self.fs, audio_data)
            self.queue.put(filename)
            print(f"已保存音檔: {filename}")
        except Exception as e:
            print(f"保存音檔失敗: {e}")
        finally:
            self.buffer = []
            self.speech_start = None
            self.silence_start = None

    def start(self):
        self.recording = True
        try:
            with sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.fs):
                print("🎙 開始錄音，按 Ctrl+C 結束")
                while self.recording:
                    time.sleep(0.01)  # 降低 CPU 使用率
        except KeyboardInterrupt:
            print("錄音停止")
            self.stop()
        except Exception as e:
            print(f"錄音發生錯誤: {e}")
            self.stop()

    def stop(self):
        self.recording = False
        # 保存緩衝區中剩餘的語音數據
        if self.buffer and (time.time() - (self.speech_start or 0)) >= self.min_speech_duration:
            self.save_buffer()
        print("錄音已結束")

'''
import sounddevice as sd
import numpy as np
import time
import scipy.io.wavfile as wav
import os

class AudioRecorder:
    def __init__(self, queue, save_dir, silence_threshold=0.0005, silence_duration=0.5, min_speech_duration=0.5):
        self.fs = 16000
        self.buffer = []
        self.queue = queue
        self.save_dir = save_dir
        self.recording = False
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.min_speech_duration = min_speech_duration
        self.silence_start = None
        self.speech_start = None
        os.makedirs(save_dir, exist_ok=True)

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            #print(f"錄音錯誤: {status}")
            return

        volume = np.sqrt(np.mean(indata ** 2))
        now = time.time()
        #print(f"音量: {volume:.4f}")  # 調試用，觀察音量值

        if volume > self.silence_threshold:
            if self.speech_start is None:
                self.speech_start = now
            self.buffer.append(indata.copy())
            self.silence_start = None
        elif self.buffer:
            if self.silence_start is None:
                self.silence_start = now
            elif now - self.silence_start > self.silence_duration:
                speech_duration = (now - self.speech_start) if self.speech_start else 0
                if speech_duration >= self.min_speech_duration:
                    self.save_buffer()
                else:
                    print(f"語音片段過短 ({speech_duration:.2f}秒)，忽略")
                self.buffer = []
                self.speech_start = None
                self.silence_start = None

    def save_buffer(self):
        if not self.buffer:
            return

        try:
            audio_data = np.concatenate(self.buffer)
            duration = len(audio_data) / self.fs
            if duration < self.min_speech_duration:
                #print(f"片段過短 ({duration:.2f}秒)，忽略")
                return
            if np.max(np.abs(audio_data)) > 1.0:
                audio_data = audio_data / np.max(np.abs(audio_data))  # 歸一化
            audio_data = (audio_data * 32767).astype(np.int16)
            filename = os.path.join(self.save_dir, f"speech_{int(time.time())}.wav")
            wav.write(filename, self.fs, audio_data)
            self.queue.put(filename)
            #print(f"已保存音檔: {filename}, 時長: {duration:.2f}秒")
        except Exception as e:
            print(f"保存音檔失敗: {e}")
        finally:
            self.buffer = []
            self.speech_start = None
            self.silence_start = None

    def start(self):
        self.recording = True
        try:
            with sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.fs):
                print("🎙 開始錄音，按 Ctrl+C 結束")
                while self.recording:
                    time.sleep(0.01)
        except KeyboardInterrupt:
            print("錄音停止")
            self.stop()
        except Exception as e:
            print(f"錄音發生錯誤: {e}")
            self.stop()

    def stop(self):
        self.recording = False
        if self.buffer and (time.time() - (self.speech_start or 0)) >= self.min_speech_duration:
            self.save_buffer()
        print("錄音已結束")

# 使用範例
if __name__ == "__main__":
    from queue import Queue
    queue = Queue()
    recorder = AudioRecorder(queue, "recordings")
    recorder.start()