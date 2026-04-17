import streamlit as st
from datetime import datetime
from chatbot import get_response
import streamlit as st

# 🔹 Ye line sab se zaroori hai (Initialization)
if "messages" not in st.session_state:
    st.session_state.messages = []  # Khali list create kar di memory mein

# 🔹 Page Config (Professional Title)
st.set_page_config(page_title="Nexus AI | Enterprise Support", page_icon="⚡", layout="wide")

# 🔹 Advanced CSS (Glassmorphism & Better Spacing)
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
    .stApp { background: transparent; }

    .chat-box {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        transition: transform 0.2s ease;
    }
    .chat-box:hover { transform: translateY(-2px); border-color: #38bdf8; }

    .user { color: #38bdf8; font-size: 0.9rem; font-weight: 600; margin-bottom: 5px; }
    .bot { color: #10b981; font-size: 0.9rem; font-weight: 600; margin-bottom: 5px; }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #ef4444;
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# 🔹 Sidebar for Technical Depth (Impresses Clients)
with st.sidebar:
    st.title(" System Config")
    st.info("Model: **Llama-3.1 (Groq)**")
    st.info("Context: **Long-term Memory Enabled**")
    st.info("Architecture: **Agentic Workflow**")
    st.divider()
    if st.button("🗑️ Reset Session"):
        st.session_state.messages = []
        st.rerun()

# 🔹 Header Section (The Professional Hook)
st.title(" Nexus AI: Intelligent Enterprise Agent")
st.markdown("##### *Next-generation conversational intelligence tailored for your specific business logic.*")
st.divider()

# 🔹 Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Display Chat History (iMessage Style)
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        role_class = "user" if msg["role"] == "user" else "bot"
        icon = "🧑" if msg["role"] == "user" else "🤖"
        name = "You" if msg["role"] == "user" else "Nexus AI"

        st.markdown(f"""
        <div class='chat-box'>
            <div class='{role_class}'>{icon} {name} • <span style='opacity:0.5; font-size:0.7rem;'>{msg['time']}</span></div>
            <div style='line-height:1.6;'>{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

# 🔹 Chat Input (Fixed at Bottom)
user_input = st.chat_input("Ask Nexus AI anything about your data...")

if user_input:
    st.session_state.messages.append({
        "role": "user", "content": user_input, "time": datetime.now().strftime("%H:%M")
    })

    # Get Real AI response
    response = get_response(user_input, st.session_state.messages)

    st.session_state.messages.append({
        "role": "assistant", "content": response, "time": datetime.now().strftime("%H:%M")
    })
    st.rerun()