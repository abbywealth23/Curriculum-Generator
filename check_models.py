import google.generativeai as genai

# Your current API Key
API_KEY = "AIzaSyAtI1cY7Wv3F6GJrgXCischwKyALsCoY_Y" 

# Setup the library
genai.configure(api_key=API_KEY)

print("--- Listing Models (google.generativeai) ---")
try:
    # list_models returns a generator of model objects
    for m in genai.list_models():
        # We only show models that support 'generateContent'
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Name: {m.name}")
except Exception as e:
    print(f"Error: {e}")