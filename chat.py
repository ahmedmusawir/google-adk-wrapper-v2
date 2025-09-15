# chat.py - Final version with double JSON parsing
import streamlit as st
import requests
import uuid
import logging
import json 

# --- Page Configuration ---
st.set_page_config(page_title="Cyberize Automation", page_icon="⚡")
st.title("⚡ Cyberize Agentic Automation")

# --- API Configuration ---
# Use the 127.0.0.1 address for reliability
N8N_WEBHOOK_URL = "http://127.0.0.1:5678/webhook/f11820f4-aaf0-4bb8-b536-b9097cc67877" 

# --- Session State Initialization ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"st-user-{uuid.uuid4()}"
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Helper Function to Call the n8n Webhook (Updated) ---
def call_n8n_webhook(agent_name, message, user_id):
    """
    Makes a POST request and correctly parses the double-layered JSON response.
    """
    payload = {
        "agent_name": agent_name,
        "message": message,
        "userId": user_id
    }
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=90)
        response.raise_for_status()

        # --- THIS IS THE NEW PARSING LOGIC ---
        # 1. Parse the outer JSON to get the 'data' string
        outer_data = response.json()
        data_string = outer_data.get("data")

        # 2. Parse the inner JSON string to get the final message
        if data_string:
            inner_data = json.loads(data_string)
            return inner_data.get("message", "Error: 'message' key not found in inner JSON.")
        else:
            return "Error: 'data' key not found in n8n response."
        # --- END OF NEW LOGIC ---

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to n8n webhook: {e}")
        return "Error: Could not reach the n8n orchestrator."
    except json.JSONDecodeError:
        st.error("Failed to decode the JSON response from n8n.")
        return "Error: Invalid JSON format received from n8n."


# --- Sidebar for Agent Selection ---
st.sidebar.title("Configuration")
agent_options = ["greeting_agent", "calc_agent", "jarvis_agent"]
selected_agent = st.sidebar.selectbox("Choose an agent:", options=agent_options)
st.sidebar.info(f"Chatting with: **{selected_agent}**")

# --- Main Chat Interface ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(f"Ask {selected_agent} a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Orchestrator is working..."):
        assistant_response = call_n8n_webhook(
            agent_name=selected_agent,
            message=prompt,
            user_id=st.session_state.user_id
        )

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.rerun()