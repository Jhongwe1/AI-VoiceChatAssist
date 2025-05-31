from perplexipy import PerplexityClient

# Initialize the client with your API key
client = PerplexityClient(key='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')

#client = PerplexityClient()





# Make a simple query
result = client.query('What is the capital of France?')
print(result)




"""
# Batch query example
results = client.queryBatch('Show me different ways of declaring a Python list')
for result in results:
    print(result)

# Streaming example
results = client.queryStreamable('Tell me why lists are important in programming')
for result in results:
    print(result)
"""


"""
# Get all supported models
models = client.models

print('Available models:')
for model in models.keys():
    print(f' - {model}')
"""

"""
try:
    # Attempt to use an invalid model
    client.model = "nonexistent-model"
    response = client.query("This will fail")
except Exception as e:
    print(f"ERROR: {e}")
    
    # Reset to a valid model
    client.model = "sonar"
    print("Reverted to default model:", client.model)
"""

'''
# Create a conversation with history management
conversation = client.createConversation()

# First user message
response = conversation.message("What is quantum computing?")
print("ASSISTANT:", response)

# Follow-up question (maintains conversation context automatically)
response = conversation.message("What are its practical applications?")
print("ASSISTANT:", response)

# You can review the conversation history
print("\nCONVERSATION HISTORY:")
for message in conversation.messages:
    print(f"{message['role'].upper()}: {message['content']}")

'''

'''
advanced_conversation = client.createConversation(
    model="sonar-pro",
    temperature=0.7,  # Controls randomness (0.0-1.0)
    max_tokens=4096,  # Maximum response length
    top_p=0.9,        # Nucleus sampling parameter
    presence_penalty=0.0,  # Penalizes repeated tokens
    frequency_penalty=0.0  # Penalizes frequent tokens
)

# You can also set system messages to guide the assistant's behavior
advanced_conversation.system_message = "You are a helpful AI assistant that specializes in explaining complex topics in simple terms. Use analogies when possible."

# Then use the conversation as normal
response = advanced_conversation.message("Explain quantum entanglement")
print(response)
'''