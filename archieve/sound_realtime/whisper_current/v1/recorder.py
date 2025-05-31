import sounddevice as sd
import numpy as np
import time
import scipy.io.wavfile as wav
import os

class AudioRecorder:
    def __init__(self, queue, save_dir, silence_threshold=500, silence_duration=1.0):
        self.fs = 16000
        self.buffer = []
        self.queue = queue
        self.save_dir = save_dir
        self.recording = True
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.silence_start = None

    def audio_callback(self, indata, frames, time_info, status):
        volume = np.linalg.norm(indata) * 1000
        now = time.time()
        if volume > self.silence_threshold:
            self.buffer.append(indata.copy())
            self.silence_start = None
        elif self.buffer:
            if self.silence_start is None:
                self.silence_start = now
            elif now - self.silence_start > self.silence_duration:
                self.save_buffer()

    def save_buffer(self):
        audio_data = np.concatenate(self.buffer)
        audio_data = (audio_data * 32767).astype(np.int16)  # 修正：轉換成 int16
        filename = os.path.join(self.save_dir, f"{int(time.time())}.wav")
        wav.write(filename, self.fs, audio_data)
        self.queue.put(filename)
        self.buffer = []
        self.silence_start = None


    def start(self):
        with sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.fs):
            print("🎙 開始錄音，按 Ctrl+C 結束")
            while self.recording:
                time.sleep(0.1)

    def stop(self):
        self.recording = False
