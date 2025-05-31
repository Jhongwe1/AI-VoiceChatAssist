import threading
import queue
import time
import os
from transcriber import WhisperTranscriber
from recorder import AudioRecorder

AUDIO_DIR = "recordings"
os.makedirs(AUDIO_DIR, exist_ok=True)

def worker(audio_queue):
    transcriber = WhisperTranscriber()
    while True:
        audio_path = audio_queue.get()
        if audio_path is None:
            break
        print(f"🔍 認識中: {audio_path}")
        for text, start, end in transcriber.transcribe(audio_path):
            print(f"[{start:.2f}s - {end:.2f}s] {text}")
        os.remove(audio_path)

if __name__ == "__main__":
    audio_queue = queue.Queue()
    recorder = AudioRecorder(audio_queue, AUDIO_DIR)
    transcriber_thread = threading.Thread(target=worker, args=(audio_queue,))
    transcriber_thread.start()

    try:
        recorder.start()
    except KeyboardInterrupt:
        print("⛔ 停止錄音")
        recorder.stop()
        audio_queue.put(None)
        transcriber_thread.join()
