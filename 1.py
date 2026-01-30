
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# ---- Streamlit UI ----
st.set_page_config(page_title="OpenRouter Chat", page_icon="🤖")
st.title("🤖 OpenRouter Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Type your message....")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.write(user_input)

    payload = {
        # "model": "openai/o4-mini",
        "model": "meta-llama/llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 256,
        "reasoning": {"enabled": False}
    }

    # Call OpenRouter
    response = requests.post(URL, headers=HEADERS, json=payload)
    response_json = response.json()

    # Safe extraction
    if "choices" not in response_json:
        assistant_reply = "⚠️ Sorry, I couldn’t process that request right now."
    else:
        assistant_reply = response_json["choices"][0]["message"]["content"]

    # Save + display response
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )
    with st.chat_message("assistant"):
        st.write(assistant_reply)

