import google.generativeai as genai

# Directly set the API key here
genai.configure(api_key="AIzaSyCExQgq_nAcXv3lLpVY0VDVVIMf6KnVV80")

# Convert the generator to a list
models = list(genai.list_models())

print("Available Gemini models:")
for m in models:
    print(m)
