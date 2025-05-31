import sounddevice as sd

def filter_devices():
    devices = sd.query_devices()
    filtered_devices = []
    seen_names = set()
    
    print("可用輸入設備：")
    for i, d in enumerate(devices):
        if d['max_input_channels'] > 0:
            device_name = d['name']
            
            # 清理設備名稱，移除多餘的括號內容來判斷是否重複
            # 例如：將 "Voicemeeter Out A1 (VB-Audio Voicemeeter VAIO)" 變成 "Voicemeeter Out A1"
            clean_name = device_name
            if "(VB-Audio Vo" in clean_name:
                clean_name = clean_name.split("(VB-Audio Vo")[0].strip()
            elif "(VB-Audio Voicemeeter VAIO)" in clean_name:
                clean_name = clean_name.split("(VB-Audio Voicemeeter VAIO)")[0].strip()
            elif "(USB PnP Audio Device(EEPROM))" in clean_name:
                clean_name = clean_name.split("(USB PnP Audio Device(EEPROM))")[0].strip()
            elif "(Realtek(R) Audio)" in clean_name:
                clean_name = clean_name.split("(Realtek(R) Audio)")[0].strip()
            
            # 只保留每個設備的第一個出現版本
            if clean_name not in seen_names:
                seen_names.add(clean_name)
                filtered_devices.append((i, d))
                # 顯示清理後的名稱
                print(f"{i}: {clean_name} (輸入通道: {d['max_input_channels']}, 預設採樣率: {d['default_samplerate']})")
    
    return filtered_devices

if __name__ == "__main__":
    filter_devices()
    filter_devices()