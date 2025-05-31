import requests
import os
import glob
import argparse
from dotenv import load_dotenv
import logging
from datetime import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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
def call_perplexity_api(prompt, model="llama-3.1-sonar-small-128k-online", temperature=0.7, max_tokens=500):
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
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": prompt}
        ],
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

# 呼叫 Grok API
def call_grok_api(prompt, model="grok-3", temperature=0.7, max_tokens=500):
    api_key = os.getenv('XAI_API_KEY')
    if not api_key:
        logger.error("未找到 xAI API key")
        return None

    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        logger.error(f"Grok API 請求失敗：{e}")
        return None

# 儲存回應到檔案
def save_response(file_path, response, api_name):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"{api_name}_response_{timestamp}.txt")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f"Input File: {file_path}\n")
            file.write(f"API: {api_name}\n")
            file.write(f"Response:\n{response}\n")
        logger.info(f"回應已儲存至 {output_file}")
    except Exception as e:
        logger.error(f"儲存回應失敗：{e}")

# 主處理函數
def process_files(input_path, api_choice, model, temperature, max_tokens):
    # 判斷是單一檔案還是資料夾
    if os.path.isfile(input_path):
        files = [input_path]
    else:
        files = glob.glob(os.path.join(input_path, "*.txt"))
        if not files:
            logger.error(f"資料夾 {input_path} 中未找到任何 .txt 檔案")
            return

    for file_path in files:
        logger.info(f"正在處理檔案：{file_path}")
        prompt = read_text_file(file_path)
        if prompt:
            if api_choice.lower() == "perplexity":
                response = call_perplexity_api(prompt, model, temperature, max_tokens)
                api_name = "Perplexity"
            else:
                response = call_grok_api(prompt, model, temperature, max_tokens)
                api_name = "Grok"

            if response:
                logger.info(f"{api_name} API 回應：{response[:100]}...")  # 顯示前100字元
                save_response(file_path, response, api_name)

# 主程式
def main():
    parser = argparse.ArgumentParser(description="使用 Perplexity 或 Grok API 處理文字檔")
    parser.add_argument("input_path", help="輸入文字檔路徑或資料夾")
    parser.add_argument("--api", choices=["perplexity", "grok"], default="grok", help="選擇 API (perplexity 或 grok)")
    parser.add_argument("--model", help="指定模型 (預設：llama-3.1-sonar-small-128k-online 或 grok-3)")
    parser.add_argument("--temperature", type=float, default=0.7, help="生成溫度 (0.0-1.0)")
    parser.add_argument("--max-tokens", type=int, default=500, help="最大回應長度")

    args = parser.parse_args()

    # 設置預設模型
    model = args.model if args.model else ("llama-3.1-sonar-small-128k-online" if args.api == "perplexity" else "grok-3")

    process_files(args.input_path, args.api, model, args.temperature, args.max_tokens)

if __name__ == "__main__":
    main()