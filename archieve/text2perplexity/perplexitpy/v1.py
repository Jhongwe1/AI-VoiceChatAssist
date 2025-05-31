import requests

# ====== 初始化設定 ======
API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY = "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"  # 請換成你的 token
MODEL = "sonar"

# ====== 對話歷史紀錄格式 (system + user/assistant 對話串) ======
conversation_history = [
    {"role": "system", "content": "你是一個擁有電機工程相關博士學位的科技業主管 現在要協助應徵者工程學士通過科技公司的面試 你要直接輸出應徵者能直接複製的回復 給他2種不同選項"}
]

# ====== 發送請求給 API ======
def ask_perplexity(user_input):
    # 把新的 user 輸入加入對話紀錄
    conversation_history.append({"role": "user", "content": user_input})
    
    # 要送出的 payload
    payload = {
        "model": MODEL,
        "messages": conversation_history,
        "max_tokens": 500,
        "temperature": 0.5,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": True,
        "top_k": 4,
        "stream": False,
        "presence_penalty": 0.5,
        "response_format": {
          "type": "text"
        },
        "web_search_options": {"search_context_size": "low"}
    }


    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 發送 POST 請求
    response = requests.post(API_URL, json=payload, headers=headers)
    
    # 處理回應
    if response.status_code == 200:
        result = response.json()
        assistant_reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        print("AI 回應:", assistant_reply)

        # 把 assistant 回覆加入對話歷史
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply
    else:
        print("錯誤:", response.status_code, response.text)
        return None

# ====== 測試用：開始對話 ======
if __name__ == "__main__":
    while True:
        user_input = input("你問：")
        if user_input.lower() in ["exit", "quit"]:
            print(conversation_history)
            break
        ask_perplexity(user_input)
