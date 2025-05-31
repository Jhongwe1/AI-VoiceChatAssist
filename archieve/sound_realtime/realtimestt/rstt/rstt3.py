from RealtimeSTT import AudioToTextRecorder
import time

def process_text(text):
    # 轉換為繁體中文
    print(text)

if __name__ == '__main__':
    recorder = AudioToTextRecorder(
        model="tiny",         # MX330 建議用 tiny 或 base
        device="cuda",        # 強制用 GPU
        compute_type="int8",  # MX330 支援 int8
        batch_size=1,
        language="zh",
        initial_prompt="這是一段中文語音轉文字"
    )
    print("開始監聽，請說話...")
    try:
        while True:
            recorder.text(process_text)
            time.sleep(0.05)  # Slightly lower for faster response
    except KeyboardInterrupt:
        print("停止監聽")
        recorder.stop()
