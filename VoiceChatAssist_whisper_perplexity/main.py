import threading
import queue
import time
import os
import keyboard
import requests
from transcriber import WhisperTranscriber
from recorder import AudioRecorder
import json


AUDIO_DIR = "recordings"
os.makedirs(AUDIO_DIR, exist_ok=True)

role1 = "應徵者"
role2 = "面試官"

# Perplexity API settings
API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY = "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"
MODEL = "sonar"

# Conversation container
conversation_container = []


#ai conversation history
conversation_history = [
    {"role": "system", "content": "你是一個擁有電機工程相關博士學位的科技業主管 現在要協助應徵者通過科技公司的面試 你要直接輸出應徵者能直接複製的回復 給他2種不同選項"}
]

def ask_perplexity(conversation):
    if not conversation:
        print("容器為空，無需傳送至 API")
        return None

    # Format conversation for API
    conversation_history.append({
        "role": "user",
        "content": "\n".join(conversation)
    })

    payload = {
        "model": MODEL,
        "messages": conversation_history,
        "max_tokens": 500,
        "temperature": 0.5,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": True,
        "top_k": 4,
        "stream": False,
        "presence_penalty": 0.5,
        "response_format": {
          "type": "text"
        },
        "web_search_options": {"search_context_size": "low"}
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            assistant_reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"AI 回應: {assistant_reply}")
            conversation_history.append({"role": "assistant", "content": assistant_reply})
            return assistant_reply
        else:
            print(f"API 錯誤: {response.status_code} {response.text}")
            return None
    except Exception as e:
        print(f"API 請求失敗: {e}")
        return None

def worker(audio_queue):
    transcriber = WhisperTranscriber()
    while True:
        item = audio_queue.get()
        if item is None:
            break
        audio_path, source = item
        for text, start, end in transcriber.transcribe(audio_path):
            formatted_text = f"[{source}] {text}"
            print(formatted_text)
            conversation_container.append(formatted_text)
        os.remove(audio_path)

if __name__ == "__main__":
    # Define device IDs for the two microphones
    mic1_device_id = 4  # 應徵者
    mic2_device_id = 6  # 面試官

    # Create a single queue for both microphones
    audio_queue = queue.Queue()

    # Create a shared flag for manual save trigger
    manual_save_event = threading.Event()

    # Initialize two recorders
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

        # Listen for key presses
        print("按空白鍵立即保存並轉錄當前語音片段，按 's' 鍵傳送容器內容至 API 並清空")
        while recorder_thread1.is_alive() or recorder_thread2.is_alive():
            if keyboard.is_pressed("space"):
                print("空白鍵觸發：立即保存語音片段")
                manual_save_event.set()
                time.sleep(0.5)
                manual_save_event.clear()
            if keyboard.is_pressed("s"):
                print("'s' 鍵觸發：傳送容器內容至 API")
                #print(conversation_history)
                ask_perplexity(conversation_container)
                conversation_container.clear()
                time.sleep(0.5)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("停止錄音")
        #print(conversation_history)
        with open("conversation_history.json", "w", encoding="utf-8") as f:
            json.dump(conversation_history, f, ensure_ascii=False, indent=4)
        recorder1.stop()
        recorder2.stop()
        audio_queue.put(None)
        transcriber_thread.join()