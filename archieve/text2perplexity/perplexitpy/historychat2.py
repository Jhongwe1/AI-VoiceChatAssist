from perplexipy import PerplexityClient

# 初始化客戶端
client = PerplexityClient(key='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')

# 初始化對話歷史
messages = []

# 添加第一條使用者訊息
messages.append({"role": "user", "content": "What is quantum computing?"})
response = client.chat(messages)
print("ASSISTANT:", response)

# 添加助手的回應
messages.append({"role": "assistant", "content": response})

# 添加後續的使用者問題
messages.append({"role": "user", "content": "What are its practical applications?"})
response = client.chat(messages)
print("ASSISTANT:", response)

# 添加助手的回應
messages.append({"role": "assistant", "content": response})
