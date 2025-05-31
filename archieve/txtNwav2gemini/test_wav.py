from google import genai

client = genai.Client(api_key="AIzaSyBNcdvICYUvxcbkiNeVJOyfyldKvc2lEQU")

myfile = client.files.upload(file=r"C:\Users\Key20\Desktop\gemini\1.wav")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=["用中文回復對話 並多講一些其他相關內容", myfile]
)

print(response.text)