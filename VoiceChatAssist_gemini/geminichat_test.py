from google import genai
from google.genai import types



client = genai.Client(api_key="AIzaSyBNcdvICYUvxcbkiNeVJOyfyldKvc2lEQU")
MODEL = "gemini-2.0-flash"

# 初始化對話歷史記錄
conversation_history = []

def funf(text):
    global conversation_history # 聲明使用全域變數

    # 將用戶輸入添加到對話歷史記錄中
    conversation_history.append(types.Content(role="user", parts=[types.Part(text=text)]))

    # 將完整的對話歷史記錄傳遞給模型
    response = client.models.generate_content(
        model=MODEL,
        contents=conversation_history, # 將整個歷史記錄傳入
        config=types.GenerateContentConfig(
            system_instruction="你是一個助手",
            max_output_tokens=500,
            temperature=0.1
        )
    )

    # 將模型的回答添加到對話歷史記錄中
    model_response_text = response.text
    conversation_history.append(types.Content(role="model", parts=[types.Part(text=model_response_text)]))

    print(model_response_text)

while True:
    txt=input()
    funf(txt)