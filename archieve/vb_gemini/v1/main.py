import threading
import queue
import time
import os
import keyboard
from recorder import AudioRecorder
from google import genai

# Gemini API settings
client = genai.Client(api_key="AIzaSyBNcdvICYUvxcbkiNeVJOyfyldKvc2lEQU")
MODEL = "gemini-2.0-flash"

AUDIO_DIR = "recordings"
os.makedirs(AUDIO_DIR, exist_ok=True)

role1 = "應徵者"
role2 = "面試官"

# Conversation container for Gemini responses
conversation_container = []

def process_audio_with_gemini(audio_queue):
    while True:
        item = audio_queue.get()
        if item is None:
            break
        audio_path, source = item
        try:
            # Upload audio file to Gemini API
            myfile = client.files.upload(file=audio_path)
            # Generate content with Chinese response instruction
            response = client.models.generate_content(
                model=MODEL,
                contents=["用中文回復對話 並多講一些其他相關內容", myfile]
            )
            formatted_text = f"{source}說完話的生成回復 {response.text}"
            print(formatted_text)
            #print(response.text)
            conversation_container.append(formatted_text)
        except Exception as e:
            print(f"處理音檔失敗 ({source}): {e}")
        finally:
            # Remove the audio file after processing
            try:
                os.remove(audio_path)
            except Exception as e:
                print(f"刪除音檔失敗 ({audio_path}): {e}")

if __name__ == "__main__":
    # Define device IDs for the two microphones
    mic1_device_id = 4  # 應徵者
    mic2_device_id = 6  # 面試官

    # Create a single queue for both microphones
    audio_queue = queue.Queue()

    # Initialize two recorders with silence detection and key-based recording
    recorder1 = AudioRecorder(audio_queue, AUDIO_DIR, device_id=mic1_device_id, source_label=role1)
    recorder2 = AudioRecorder(audio_queue, AUDIO_DIR, device_id=mic2_device_id, source_label=role2)

    # Start a single Gemini processing thread
    gemini_thread = threading.Thread(target=process_audio_with_gemini, args=(audio_queue,))
    gemini_thread.start()

    try:
        # Start both recorders in separate threads
        recorder_thread1 = threading.Thread(target=recorder1.start)
        recorder_thread2 = threading.Thread(target=recorder2.start)

        recorder_thread1.start()
        recorder_thread2.start()

        print("按住 's' 鍵開始錄音，放開 's' 鍵保存並處理音檔（僅保存有語音的片段），按 Ctrl+C 結束")
        while recorder_thread1.is_alive() or recorder_thread2.is_alive():
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("停止錄音")
        recorder1.stop()
        recorder2.stop()
        audio_queue.put(None)
        gemini_thread.join()