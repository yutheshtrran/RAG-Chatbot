from google import genai

client = genai.Client(api_key="YOUR_API_KEY")
print(client.models.list())
