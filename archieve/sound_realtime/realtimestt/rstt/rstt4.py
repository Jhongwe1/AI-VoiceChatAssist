from RealtimeSTT import AudioToTextRecorder

def process_text(text):
    print(text)

if __name__ == '__main__':
    recorder = AudioToTextRecorder(
        model="tiny",                    # 強制使用最小模型
        device="cuda",                   # 強制 GPU 加速
        compute_type="int8",             # MX330 最佳計算類型
        language="zh",                   # 鎖定中文模式
        post_speech_silence_duration=0.1,  # 停頓 0.1 秒即觸發
        min_length_of_recording=0.2,     # 最短錄音 0.2 秒
        #silero_sensitivity=0.3,          # 超高敏感度 (0-1, 越低越敏感)
        batch_size=10,                    # 最小批次保障即時性
        beam_size=10,                     # 禁用光束搜索加速反應
        #enable_realtime_transcription=True,  # 啟用邊說邊轉
        #realtime_processing_pause=0.05   # 每 0.05 秒更新一次
    )
    print("開始監聽（極速模式）...")
    while True:
        recorder.text(process_text)
