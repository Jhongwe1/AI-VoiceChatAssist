import sounddevice as sd
import numpy as np
import threading
import scipy.io.wavfile

duration = 10  # 錄 30 秒
fs = 44100     # 採樣率

# 替換成你的裝置 ID
my_mic_device = 4
other_audio_device = 8

my_voice = []
other_voice = []

def record_from_device(device_id, storage_list):
    def callback(indata, frames, time, status):
        if status:
            print(f"Device {device_id} warning:", status)
        storage_list.append(indata.copy())

    with sd.InputStream(samplerate=fs, device=device_id, channels=1, callback=callback):
        sd.sleep(duration * 1000)

# 開兩條錄音執行緒
t1 = threading.Thread(target=record_from_device, args=(my_mic_device, my_voice))
t2 = threading.Thread(target=record_from_device, args=(other_audio_device, other_voice))

t1.start()
t2.start()
t1.join()
t2.join()

# 合併 & 儲存成 wav
my_voice_np = np.concatenate(my_voice)
other_voice_np = np.concatenate(other_voice)

scipy.io.wavfile.write("my_voice.wav", fs, my_voice_np)
scipy.io.wavfile.write("other_voice.wav", fs, other_voice_np)
