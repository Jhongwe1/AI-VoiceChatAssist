import sounddevice as sd

devices = sd.query_devices()
print("可用輸入設備：")
for i, d in enumerate(devices):
    if d['max_input_channels'] > 0:
        print(f"{i}: {d['name']} (輸入通道: {d['max_input_channels']}, 預設採樣率: {d['default_samplerate']})")