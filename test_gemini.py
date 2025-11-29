import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv("GOOGLE_API_KEY")
print(f"DEBUG: API Key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"DEBUG: API Key length: {len(api_key)}")
    genai.configure(api_key=api_key)

# Mock DataFrame
data = {
    "municipio": ["Bucaramanga", "Floridablanca", "Giron"],
    "delito": ["HURTO", "HOMICIDIO", "LESIONES"],
    "anio": [2024, 2024, 2024],
    "cantidad": [100, 5, 20]
}
df = pd.DataFrame(data)

# Import the function from app.py (or recreate it for testing to avoid streamlit dependencies issues in this script if app.py has top-level streamlit calls)
# To be safe, I'll just copy the core logic here to test the API specifically.

def test_agent(question):
    print(f"\nTesting question: '{question}'")
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        response = model.generate_content(f"Answer this question: {question}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_agent("Hola, ¿estás funcionando?")
