import whisper
import os
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

# 載入模型
model = whisper.load_model("base")  # 你也可以用 "small", "medium", "large"

# 進行語音辨識
result = model.transcribe("test.wav")
print("辨識結果：")
print(result["text"])

import torch
print(torch.cuda.is_available())  # 應輸出 True
print(torch.__version__)          # 應顯示 cuXXX 後綴（如 cu118）
print(torch.cuda.get_device_name(0))  # 應顯示 "GeForce MX330"
