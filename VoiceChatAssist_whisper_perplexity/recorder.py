import sounddevice as sd
import numpy as np
import time
import scipy.io.wavfile as wav
import os

class AudioRecorder:
    def __init__(self, queue, save_dir, device_id=None, source_label="default", silence_threshold=0.0005, silence_duration=0.3, min_speech_duration=0.5, manual_save_event=None):
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
        self.device_id = device_id
        self.source_label = source_label
        self.manual_save_event = manual_save_event
        os.makedirs(save_dir, exist_ok=True)
        self.max_speech_duration = 15.0  # Maximum speech duration before forcing transcription

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
            if self.speech_start:  # Ensure speech_start is set before checking
                speech_duration = now - self.speech_start
                if speech_duration >= self.max_speech_duration:
                    print(f"語音片段超過 {self.max_speech_duration} 秒 ({self.source_label})，強制保存")
                    self.save_buffer()

        elif self.buffer:
            if self.silence_start is None:
                self.silence_start = now
            elif now - self.silence_start > self.silence_duration:
                speech_duration = (now - self.speech_start) if self.speech_start else 0
                if speech_duration >= self.min_speech_duration:
                    #print(f"檢測到停頓 ({self.source_label})，保存語音片段")
                    self.save_buffer()
                else:
                    #print(f"語音片段過短 ({self.source_label}, {speech_duration:.2f}秒)，忽略")
                    self.buffer = []
                    self.speech_start = None
                    self.silence_start = None

        # Check for manual save trigger
        if self.manual_save_event and self.manual_save_event.is_set() and self.buffer:
            speech_duration = (now - self.speech_start) if self.speech_start else 0
            if speech_duration >= self.min_speech_duration:
                #print(f"手動保存觸發 ({self.source_label})")
                self.save_buffer()
            #else:
                #print(f"手動保存忽略：語音片段過短 ({self.source_label}, {speech_duration:.2f}秒)")
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
                #print(f"保存忽略：語音片段過短 ({self.source_label}, {duration:.2f}秒)")
                return
            if np.max(np.abs(audio_data)) > 1.0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            audio_data = (audio_data * 32767).astype(np.int16)
            timestamp = int(time.time() * 1000)
            filename = os.path.join(self.save_dir, f"speech_{timestamp}_{self.source_label}.wav")
            wav.write(filename, self.fs, audio_data)
            self.queue.put((filename, self.source_label))
            #print(f"音檔已保存 ({self.source_label}): {filename}")
        except Exception as e:
            print(f"保存音檔失敗 ({self.source_label}): {e}")
        finally:
            self.buffer = []
            self.speech_start = None
            self.silence_start = None

    def start(self):
        self.recording = True
        try:
            with sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.fs, device=self.device_id):
                print(f"🎙 開始錄音 ({self.source_label})，按 Ctrl+C 結束或空白鍵手動保存")
                while self.recording:
                    time.sleep(0.01)
        except KeyboardInterrupt:
            print(f"錄音停止 ({self.source_label})")
            self.stop()
        except Exception as e:
            print(f"錄音發生錯誤 ({self.source_label}): {e}")
            self.stop()

    def stop(self):
        self.recording = False
        if self.buffer and (time.time() - (self.speech_start or 0)) >= self.min_speech_duration:
            self.save_buffer()
        print(f"錄音已結束 ({self.source_label})")