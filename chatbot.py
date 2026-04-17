import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from supabase_manager import save_customer_lead

load_dotenv()

# 🔹 Fast LLM
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens=300
)

# 🔹 Load FAQ
def load_faq(file_path="faq.json"):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

faq_data = load_faq()

# 🔹 Language Detection
def detect_language(text):
    text = text.lower()
    words = text.split()

    roman_urdu_words = {
        "kya","hai","tum","mujhe","kar","jani","hn",
        "mera","ap","ka","kr","ho","acha","theek"
    }

    urdu_chars = any("\u0600" <= c <= "\u06FF" for c in text)

    if urdu_chars:
        return "urdu"

    roman_score = sum(word in roman_urdu_words for word in words)

    # 🔥 threshold lagao
    if roman_score >= 2:
        return "roman_urdu"

    return "english"
# 🔹 Lead Detection (IMPORTANT)
def extract_lead(text):
    if "@" in text:
        return text  # simple detection (improve later)
    return None

# 🔹 Main Response Function
def get_response(user_input, chat_history):

    language = detect_language(user_input)

    # 🔹 Language Rules
    if language == "roman_urdu":
        lang_instruction = """
        STRICT RULE:
        - Reply ONLY in Roman Urdu (WhatsApp style)
        - Do NOT use English sentences
        """
    elif language == "urdu":
        lang_instruction = """
        STRICT RULE:
        - Reply ONLY in Urdu script
        - Do NOT use Roman Urdu or English
        """
    else:
        lang_instruction = """
        STRICT RULE:
        - Reply ONLY in English
        - Do NOT use Urdu or Roman Urdu
        - Do NOT start with words like 'Salaam'
        """

    # 🔹 Strong Prompt
    system_prompt = f"""
You are Nexus AI, a fast and smart assistant.

Rules:
- Always reply FAST and clearly
- Never give incomplete sentences
- Keep answers short and human-like
- Match user's language

Language Rule:
{lang_instruction}
"""

    # 🔹 1. FAQ FIRST (⚡ speed boost)
    for item in faq_data:
        if user_input.lower() in item["question"].lower():
            return item["answer"]


    # 🔹 2. Lead Save (NO AGENT)
    lead = extract_lead(user_input)
    if lead:
        try:
            save_customer_lead(lead)
            if language == "roman_urdu":
                return "Perfect 👍 apki info save ho gai hai!"
            elif language == "urdu":
                return "آپ کی معلومات محفوظ ہو گئی ہیں۔"
            else:
                return "Your information has been saved successfully."
        except:
            pass

def get_response(user_input, chat_history):

    language = detect_language(user_input)

    # 🔹 Language Rules
    if language == "roman_urdu":
        lang_instruction = "Reply ONLY in Roman Urdu"
    elif language == "urdu":
        lang_instruction = "Reply ONLY in Urdu"
    else:
        lang_instruction = "Reply ONLY in English"

    # 🔹 Prompt
    system_prompt = f"""
You are Nexus AI.

Language Rule:
{lang_instruction}
"""

    # 🔹 FAQ
    for item in faq_data:
        if user_input.lower() in item["question"].lower():
            return item["answer"]

   # 🔹 LLM CALL
    messages = [SystemMessage(content=system_prompt)]

    # Aapka wahi language tag logic jo aapne fix kiya tha
    messages.append(
        HumanMessage(content=f"[LANG={language}] {user_input}")
    )

    for msg in chat_history[-4:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    try:
        # LLM ko call karna
        response = llm.invoke(messages)
        raw_content = response.content.strip()

        # ✨ Yahan se Cleaning shuru hoti hai (Thinking/JSON ko hatane ke liye)
        import re
        # Agar model ne galti se JSON ya Thinking tags diye, toh ye unhein khatam kar dega
        clean_content = re.sub(r'```json.*?```', '', raw_content, flags=re.DOTALL)
        clean_content = re.sub(r'\{.*?\}', '', clean_content, flags=re.DOTALL)
        # Thinking patterns ko mazeed saaf karna
        clean_content = re.sub(r'(Thought|Action|Action Input):.*?\n', '', clean_content, flags=re.IGNORECASE)

        return clean_content.strip()

    except Exception as e:
        # Professional English Error as you requested
        return "I apologize, but the system is currently experiencing a high volume of requests. Please try again in a moment."