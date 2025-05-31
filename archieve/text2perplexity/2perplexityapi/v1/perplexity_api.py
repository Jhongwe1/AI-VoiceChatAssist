import requests
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 讀取文字檔
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"檔案 {file_path} 不存在！")
        return None
    except Exception as e:
        print(f"讀取檔案時發生錯誤：{e}")
        return None

# 呼叫 Perplexity API
def call_perplexity_api(prompt):
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        print("未找到 Perplexity API key！")
        return None

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Perplexity API 請求失敗：{e}")
        return None

# 主程式
def main():
    file_path = "input.txt"
    prompt = read_text_file(file_path)
    if prompt:
        response = call_perplexity_api(prompt)
        if response:
            print("Perplexity API 回應：")
            print(response)

if __name__ == "__main__":
    main()