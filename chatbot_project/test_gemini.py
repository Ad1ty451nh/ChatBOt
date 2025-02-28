import google.generativeai as genai

# Load Gemini API key
GEMINI_API_KEY = "AIzaSyAXHYO4AWe3KKKg9mqjebImGyExD7hxjO8"
genai.configure(api_key=GEMINI_API_KEY)

try:
    # Use a Gemini model
    model = genai.GenerativeModel("gemini-2.0-pro-exp")  # Change model if needed

    response = model.generate_content("Hello, how are you?")
    
    print("API is working! ✅")
    print("Response:", response.text)
except Exception as e:
    print("Error:", e)
