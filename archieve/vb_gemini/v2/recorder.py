import sounddevice as sd
import numpy as np
import time
import scipy.io.wavfile as wav
import os
import keyboard

class AudioRecorder:
    def __init__(self, queue, save_dir, device_id=None, source_label="default", silence_threshold=0.0005, silence_duration=0.3, min_speech_duration=0.5):
        self.fs = 16000
        self.queue = queue
        self.save_dir = save_dir
        self.recording = False
        self.buffer = []
        self.device_id = device_id
        self.source_label = source_label
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.min_speech_duration = min_speech_duration
        self.silence_start = None
        self.speech_start = None
        os.makedirs(save_dir, exist_ok=True)
        self.max_speech_duration = 120  # Maximum speech duration before forcing save

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"錄音錯誤 ({self.source_label}): {status}")
            return

        volume = np.sqrt(np.mean(indata ** 2))
        now = time.time()

        if volume > self.silence_threshold:
            if self.speech_start is None:
                self.speech_start = now
            self.buffer.append(indata.copy())
            self.silence_start = None

            # Check if speech duration exceeds max_speech_duration
            if self.speech_start:
                speech_duration = now - self.speech_start
                if speech_duration >= self.max_speech_duration:
                    print(f"語音片段超過 {self.max_speech_duration} 秒 ({self.source_label})，強制保存")
                    self.save_buffer()



    def save_buffer(self):
        if not self.buffer:
            print(f"無錄音數據 ({self.source_label})")
            return

        try:
            audio_data = np.concatenate(self.buffer)
            duration = len(audio_data) / self.fs
            if duration < self.min_speech_duration:
                print(f"保存忽略：語音片段過短 ({self.source_label}, {duration:.2f}秒)")
                return
            if np.max(np.abs(audio_data)) > 1.0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            audio_data = (audio_data * 32767).astype(np.int16)
            timestamp = int(time.time() * 1000)
            filename = os.path.join(self.save_dir, f"speech_{timestamp}_{self.source_label}.wav")
            wav.write(filename, self.fs, audio_data)
            self.queue.put((filename, self.source_label))
            print(f"音檔已保存 ({self.source_label}): {filename}")
        except Exception as e:
            print(f"保存音檔失敗 ({self.source_label}): {e}")
        finally:
            self.buffer = []
            self.speech_start = None
            self.silence_start = None

    def start(self):
        self.recording = True
        is_recording = False
        last_key_press = 0
        debounce_time = 0.3  # Debounce time in seconds
        print(f"🎙 準備錄音 ({self.source_label})，按 's' 鍵切換錄音開/關")
        while self.recording:
            if keyboard.is_pressed('s') and (time.time() - last_key_press) > debounce_time:
                last_key_press = time.time()
                is_recording = not is_recording  # Toggle recording state
                if is_recording:
                    print(f"開始錄音 ({self.source_label})")
                    self.buffer = []
                    self.speech_start = None
                    self.silence_start = None
                    try:
                        with sd.InputStream(
                            callback=self.audio_callback,
                            channels=1,
                            samplerate=self.fs,
                            device=self.device_id
                        ):
                            while is_recording and self.recording:
                                time.sleep(0.01)
                                if keyboard.is_pressed('s') and (time.time() - last_key_press) > debounce_time:
                                    last_key_press = time.time()
                                    is_recording = False
                    except Exception as e:
                        print(f"錄音發生錯誤 ({self.source_label}): {e}")
                    print(f"停止錄音 ({self.source_label})，檢查語音片段")
                    # Save only if valid speech was detected
                    if self.buffer and self.speech_start:
                        speech_duration = (time.time() - self.speech_start) if self.speech_start else 0
                        if speech_duration >= self.min_speech_duration:
                            self.save_buffer()
                        else:
                            print(f"語音片段過短 ({self.source_label}, {speech_duration:.2f}秒)，忽略")
                            self.buffer = []
                            self.speech_start = None
                            self.silence_start = None
                    else:
                        print(f"無有效語音數據 ({self.source_label})")
                else:
                    print(f"錄音已暫停 ({self.source_label})，按 's' 鍵繼續")
            time.sleep(0.01)

    def stop(self):
        self.recording = False
        if self.buffer and self.speech_start:
            speech_duration = time.time() - self.speech_start
            if speech_duration >= self.min_speech_duration:
                self.save_buffer()
            else:
                print(f"最終語音片段過短 ({self.source_label}, {speech_duration:.2f}秒)，忽略")
        print(f"錄音已結束 ({self.source_label})")