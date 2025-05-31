import requests
import json

API_KEY = "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"
API_URL = "https://api.perplexity.ai/chat/completions"

# Initialize an empty conversation history
conversation_history = [
    {"role": "system", "content": "You are a helpful AI assistant that provides accurate information."}
]

def send_message(message):
    conversation_history.append({"role": "user", "content": message})
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "sonar-pro",  # Or your preferred model
        "messages": conversation_history,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response_json = response.json()

    # Check for 'choices' key
    if 'choices' not in response_json or not response_json['choices']:
        raise RuntimeError(f"No assistant response found: {response_json}")

    assistant_response = response_json['choices']['message']['content']
    conversation_history.append({"role": "assistant", "content": assistant_response})
    return assistant_response

# Example usage
response = send_message("What is quantum computing?")
print("ASSISTANT:", response)

response = send_message("What are its practical applications?")
print("ASSISTANT:", response)

# Print conversation history
print("\nCONVERSATION HISTORY:")
for message in conversation_history:
    print(f"{message['role'].upper()}: {message['content']}")
