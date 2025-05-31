from google import genai
from google.genai import types



client = genai.Client(api_key="AIzaSyBNcdvICYUvxcbkiNeVJOyfyldKvc2lEQU")
MODEL = "gemini-2.0-flash"

def funf(text):
    response = client.models.generate_content(
                    model=MODEL,
                    contents=[text],
                    config=types.GenerateContentConfig(
                        system_instruction="你是一個助手",
                        max_output_tokens=500,
                        temperature=0.1
                    )
                    
                )

    print(response.text)


while True:
    txt=input()
    funf(txt)