import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_questions(exam_type, subject, difficulty):
    # Using 1.5 Flash for speed and efficiency
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Custom persona logic to guide Gemini's behavior
    exam_context = {
        "UPSC": "Focus on conceptual depth, multi-statement analysis, and current affairs integration.",
        "JEE": "Focus on high-level Physics/Math application with technical accuracy.",
        "NEET": "Focus on Biology precision and Chemistry concepts.",
        "SSC CGL": "Focus on factual accuracy and logical reasoning patterns."
    }.get(exam_type, "Standard competitive exam format.")

    prompt = f"""
    You are an expert examiner for {exam_type}. 
    Subject: {subject}. Difficulty: {difficulty}.
    Context: {exam_context}

    Generate 5 MCQs. Return ONLY a JSON array with this structure:
    [
      {{
        "question": "The question text",
        "options": ["A", "B", "C", "D"],
        "answer": "The correct option text exactly",
        "explanation": "A high-quality educational explanation"
      }}
    ]
    """

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)

def get_chatbot_response(user_message, chat_history=None):
    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        system_instruction="You are PrepAI, an expert AI Tutor designed to help students prepare for competitive exams. Provide clear, accurate, and encouraging explanations."
    )
    
    formatted_history = []
    if chat_history:
        for msg in chat_history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg["content"]]})
            
    chat = model.start_chat(history=formatted_history)
    response = chat.send_message(user_message)
    return response.text