import threading
import queue
import time
import os
import keyboard  # New dependency for key detection
from transcriber import WhisperTranscriber
from recorder import AudioRecorder

AUDIO_DIR = "recordings"
os.makedirs(AUDIO_DIR, exist_ok=True)

role1="應徵者"
role2="面試官"



def worker(audio_queue):
    transcriber = WhisperTranscriber()
    while True:
        item = audio_queue.get()
        if item is None:
            break
        audio_path, source = item
        print(f"🔍 認識中 ({source}): {audio_path}")
        for text, start, end in transcriber.transcribe(audio_path):
            print(f"[{source} {start:.2f}s - {end:.2f}s] {text}")
        os.remove(audio_path)

if __name__ == "__main__":
    # Define device IDs for the two microphones (replace with actual device IDs)
    mic1_device_id = 4  #role1  4: b2   6:b1  
    mic2_device_id = 6  #role2  Example device ID for second microphone

    # Create a single queue for both microphones
    audio_queue = queue.Queue()

    # Create a shared flag for manual save trigger
    manual_save_event = threading.Event()

    # Initialize two recorders with different device IDs and source labels
    recorder1 = AudioRecorder(audio_queue, AUDIO_DIR, device_id=mic1_device_id, source_label=role1, manual_save_event=manual_save_event)
    recorder2 = AudioRecorder(audio_queue, AUDIO_DIR, device_id=mic2_device_id, source_label=role2, manual_save_event=manual_save_event)

    # Start a single transcriber thread
    transcriber_thread = threading.Thread(target=worker, args=(audio_queue,))
    transcriber_thread.start()

    try:
        # Start both recorders in separate threads
        recorder_thread1 = threading.Thread(target=recorder1.start)
        recorder_thread2 = threading.Thread(target=recorder2.start)

        recorder_thread1.start()
        recorder_thread2.start()

        # Listen for spacebar press to trigger manual save
        print("按空白鍵立即保存並轉錄當前語音片段")
        while recorder_thread1.is_alive() or recorder_thread2.is_alive():
            if keyboard.is_pressed("space"):
                print("🚀 空白鍵觸發：立即保存語音片段")
                manual_save_event.set()  # Signal recorders to save buffer
                time.sleep(0.5)  # Debounce to prevent multiple triggers
                manual_save_event.clear()  # Reset the event
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("⛔ 停止錄音")
        recorder1.stop()
        recorder2.stop()
        audio_queue.put(None)
        transcriber_thread.join()