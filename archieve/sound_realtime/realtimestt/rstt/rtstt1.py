from RealtimeSTT import AudioToTextRecorder
import time

def process_text(text):
    print(text)

if __name__ == '__main__':
    print("開始監聽，請說話...")

    # Configure AudioToTextRecorder for better accuracy on MX330
    recorder = AudioToTextRecorder(
        model="small",  # Upgrade to "small" or "medium" if VRAM allows; "base" is less accurate
        device="cuda",  # Use CUDA; switch to "cpu" if VRAM is insufficient
        compute_type="float32",  # Explicitly set to float32 due to MX330 limitations
        batch_size=8,  # Increase batch size for better context, adjust based on VRAM
        language="zh",  # Chinese language
        start_callback_in_new_thread=False,  # Keep main thread for compatibility
        beam_size=5,  # Enable beam search for better accuracy (if supported)
        #energy_threshold=0.5,  # Adjust for microphone sensitivity (tune based on environment)
        #pause_threshold=0.8  # Adjust pause detection for smoother transcription
    )

    try:
        while True:
            recorder.text(process_text)
            time.sleep(0.1)  # Prevent excessive CPU usage in loop
    except KeyboardInterrupt:
        print("停止監聽")
        recorder.stop()