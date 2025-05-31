import requests
import os
import glob
import argparse
from dotenv import load_dotenv
import logging
from datetime import datetime

# 設置日誌
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"perplexity_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 載入環境變數
load_dotenv()

# 讀取文字檔
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        logger.error(f"檔案 {file_path} 不存在")
        return None
    except Exception as e:
        logger.error(f"讀取檔案 {file_path} 時發生錯誤：{e}")
        return None

# 呼叫 Perplexity API
def call_perplexity_api(messages, model="llama-3.1-sonar-small-128k-online", temperature=0.7, max_tokens=500):
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        logger.error("未找到 Perplexity API key")
        return None

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        logger.error(f"Perplexity API 請求失敗：{e}")
        return None

# 儲存回應到檔案
def save_response(source, messages, response, api_name="Perplexity"):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"{api_name}_response_{timestamp}.txt")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f"Input Source: {source}\n")
            file.write(f"API: {api_name}\n")
            file.write("Conversation:\n")
            for msg in messages:
                file.write(f"{msg['role'].capitalize()}: {msg['content']}\n")
            file.write(f"Response: {response}\n")
        logger.info(f"回應已儲存至 {output_file}")
    except Exception as e:
        logger.error(f"儲存回應失敗：{e}")

# 處理動態輸入或資料夾
def process_input(input_dir, model, temperature, max_tokens):
    # 初始化對話歷史
    messages = [{"role": "system", "content": "Be precise and concise."}]
    
    # 檢查資料夾是否存在
    input_dir = input_dir or "input_files"
    if os.path.exists(input_dir):
        files = glob.glob(os.path.join(input_dir, "*.txt"))
        if files:
            logger.info(f"找到資料夾 {input_dir} 中的檔案，將逐一處理")
            for file_path in files:
                logger.info(f"正在處理檔案：{file_path}")
                prompt = read_text_file(file_path)
                if prompt:
                    messages.append({"role": "user", "content": prompt})
                    response = call_perplexity_api(messages, model, temperature, max_tokens)
                    if response:
                        print(f"Perplexity 回應：{response}")
                        logger.info(f"Perplexity API 回應：{response}")
                        messages.append({"role": "assistant", "content": response})
                        save_response(file_path, messages, response)
            return  # 處理完檔案後退出

    # 動態輸入循環
    print("進入持續對話模式（輸入 '退出' 或 'exit' 結束）：")
    while True:
        print("請輸入提示：")
        input_text = input().strip()
        if input_text.lower() in ["退出", "exit"]:
            logger.info("用戶結束對話")
            break
        if not input_text:
            print("請輸入有效提示，或輸入 '退出' 結束")
            continue
        
        logger.info("處理動態輸入")
        messages.append({"role": "user", "content": input_text})
        response = call_perplexity_api(messages, model, temperature, max_tokens)
        if response:
            #print(f"Perplexity 回應：{response}")
            logger.info(f"Perplexity API 回應：{response}")
            messages.append({"role": "assistant", "content": response})
            save_response("Dynamic Input", messages, response)
        else:
            print("無法獲取回應，請檢查 API key 或網路連線")

# 主程式
def main():
    parser = argparse.ArgumentParser(description="使用 Perplexity API 進行持續對話或處理文字檔")
    parser.add_argument("--input-dir", default="input_files", help="輸入資料夾路徑（預設：input_files）")
    parser.add_argument("--model", default="llama-3.1-sonar-small-128k-online", help="指定 Perplexity 模型")
    parser.add_argument("--temperature", type=float, default=0.7, help="生成溫度 (0.0-1.0)")
    parser.add_argument("--max-tokens", type=int, default=500, help="最大回應長度")

    args = parser.parse_args()
    process_input(args.input_dir, args.model, args.temperature, args.max_tokens)

if __name__ == "__main__":
    main()