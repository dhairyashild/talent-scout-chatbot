import os
from dotenv import load_dotenv
import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"Testing new API key...")

if api_key:
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello from TalentScout!'"}],
            max_tokens=10
        )
        print("✅ OpenAI API Test Successful!")
        print("Response:", response.choices[0].message.content)
    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        print("Make sure you revoked the old key and created a new one!")
else:
    print("❌ No API key found")
