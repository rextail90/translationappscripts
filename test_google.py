# Test file for Google Translate API

from translators.google_api import GoogleTranslateAPITranslator
from config import GOOGLE_API_KEY

def test_google_translate():
    # Check if API key is set
    if not GOOGLE_API_KEY:
        print("ERROR: GOOGLE_API_KEY is not set in .env file")
        print("Please set GOOGLE_API_KEY in your .env file")
        return
    
    print("Testing Google Translate API...")
    print(f"API Key found: {GOOGLE_API_KEY[:10]}...")
    
    try:
        # Initialize translator
        translator = GoogleTranslateAPITranslator()
        print("Translator initialized successfully")
        
        # Test translation: Arabic to English
        arabic_text = "مرحبا"
        print(f"\nTranslating Arabic text: {arabic_text}")
        print("Source: Arabic")
        print("Target: English")
        
        result = translator.translate(arabic_text, "arabic", "english")
        
        print(f"\nTranslation result: {result}")
        print("\nTest completed successfully!")
        
    except ValueError as e:
        print(f"ERROR: {e}")
    except Exception as e:
        print(f"ERROR during translation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_google_translate()

