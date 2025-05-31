from perplexipy import PerplexityClient

class Conversation:
    def __init__(self, api_key):
        self.client = PerplexityClient(api_key=api_key)
        self.messages = []

    def send(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        response = self.client.chat(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response

# 使用範例
conversation = Conversation(api_key="YOUR_API_KEY")
print("ASSISTANT:", conversation.send("What is quantum computing?"))
print("ASSISTANT:", conversation.send("What are its practical applications?"))
