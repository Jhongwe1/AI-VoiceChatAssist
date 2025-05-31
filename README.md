# 通話/面試輔助 AI

一個智能通話助手，在重要通話或面試時為您提供即時回應建議。

## 專案簡介

這是一個能夠在通話過程中提供即時輔助的 AI 工具。當您在進行面試、商務談話或其他重要對話時，本工具能夠監聽通話內容並提供適當的回應建議，讓您在對話中更加自信和流暢。

![image](https://github.com/user-attachments/assets/7c37f8ec-bd91-42ee-be07-219d6df56ef1)

## 主要功能

- **即時語音監聽** - 捕捉通話雙方的音訊內容
- **語音轉文字** - 將音訊內容轉換為文字進行分析
- **AI 智能分析** - 基於對話內容提供回應建議
- **多輪對話支援** - 支援連續對話，不限於單次問答
- **即時回應** - 快速生成適當的回應建議

## 技術架構

### v1 - Whisper + Perplexity API
```
音訊輸入 → Virtual Audio Cable → Whisper 轉錄 → Perplexity API → AI 建議輸出
```

### v2 - Gemini API (推薦)
```
音訊輸入 → Virtual Audio Cable → 直接上傳至 Gemini API → AI 建議輸出
```

## 系統需求

### 必要軟體
- Python 3.8+
- Virtual Audio Cable (Voice Banana) - 虛擬音訊線路軟體
- gemini/perplexity api key

### Python 套件
```bash
pip install threading
pip install queue
pip install time
pip install os
pip install keyboard
pip install sounddevice
pip install numpy
pip install scipy
pip install google-generativeai
pip install requests
pip install faster-whisper
# 其他套件
```

## 安裝與設置

1. **下載並安裝 Virtual Audio Cable**
   ```
   前往 https://vb-audio.com/Cable/ 下載 Voice Banana
   安裝完成後重啟電腦
   ```

2. **設置音訊路由**
   - 將系統音訊輸出設定為 Virtual Audio Cable
   - 確保通話軟體的音訊能夠被捕獲
   - 使用device.py查看要在main.py輸入的虛擬音效

3. **配置/執行程式**
   python
   在main.py修改相關內容後 執行main.py
   PERPLEXITY_API_KEY = "your_perplexity_api_key"
   GEMINI_API_KEY = "your_gemini_api_key"
   mic1_device_id = 虛擬音效1  # 應徵者
   mic2_device_id = 虛擬音效2  # 面試官	
   


## 使用方法

1. 啟動程式後，系統會開始監聽音訊輸入
2. 開始您的通話或面試
3. AI 會即時分析對話內容並在控制台顯示建議回應
4. 支援多輪對話，可持續進行互動


## 使用場景

- **工作面試** - 獲得面試問題的回應建議
- **商務談判** - 在重要商務對話中獲得支援
- **學術討論** - 在學術交流中提供參考意見
- **日常對話** - 提升對話技巧和表達能力

## 開發過程

- 從 Whisper + Perplexity 的組合方案，升級到直接使用 Gemini API 處理音訊，大幅提升了處理效率
- 實現了連續對話功能，使得助手能夠理解對話脈絡
- 雖然製作gemini版的時候發現網路上已有類似產品，但自行開發讓我能夠完全掌控功能特性，便於未來擴展

## 未來規劃

- 新增 GUI 使用者介面
- 支援圖片輸入
- 新增對話記錄與分析功能
- 整合更多 AI 模型選項
- 開發行動端應用


