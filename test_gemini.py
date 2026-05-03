import os
from ai_generator import get_questions, get_chatbot_response

print("Testing Gemini API...")
try:
    print("Testing Quiz Generation...")
    questions = get_questions("UPSC", "History", "Medium")
    print(f"Success! Received {len(questions)} questions.")
except Exception as e:
    print(f"Quiz Generation Error: {e}")

try:
    print("\nTesting Chatbot Response...")
    response = get_chatbot_response("Hello, what exams do you cover?")
    print(f"Success! Response: {response}")
except Exception as e:
    print(f"Chatbot Error: {e}")
