from RealtimeSTT import AudioToTextRecorder
import time


def process_text(text):
    print(text)

if __name__ == '__main__':
    print("開始監聽，請說話...")

    # Optimized configuration for fast speech on MX330
    recorder = AudioToTextRecorder(
        model="small",  # Stick with "small" due to VRAM; try "medium" if feasible
        device="cuda",  # Use CUDA; switch to "cpu" if VRAM is insufficient
        compute_type="float32",  # Required for MX330 (no efficient float16 support)
        batch_size=12,  # Increased for better context; reduce if memory errors occur
        language="zh",  # Chinese language
        start_callback_in_new_thread=False,  # Main thread for compatibility
        beam_size=10,  # Increase beam size for better decoding of fast speech
        #energy_threshold=0.3,  # Lower to capture fast speech better
        #pause_threshold=0.5,  # Shorter pause detection for rapid speech
        #min_speech_duration=0.1,  # Allow shorter speech segments
        #max_speech_duration=float('inf'),  # No upper limit for continuous speech
        #dynamic_energy_threshold=True  # Adapt to varying speech speeds
        post_speech_silence_duration=0.1,
        ###enable_realtime_transcription=True,  # Explicitly enable real-time mode
        #realtime_model_type="small",  # Ensure real-time model matches main model
        #realtime_processing_timeout=0.1
    )

    try:
        while True:
            recorder.text(process_text)
            time.sleep(0.05)  # Slightly lower for faster response
    except KeyboardInterrupt:
        print("停止監聽")
        recorder.stop()