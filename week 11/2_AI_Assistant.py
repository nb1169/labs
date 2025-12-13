# 2_AI_Assistant.py

import streamlit as st
import sys
import os

# added the project root directory (ensure pathing is correct)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

# NEW IMPORTS: use the new OOP service
from services.ai_assistant import AIAssistant

# --- initialize the ai assistant ---
# create a session state to hold the assistant object and chat history
if 'ai_assistant' not in st.session_state:
    st.session_state.ai_assistant = AIAssistant()
    st.session_state.messages = []

st.title("ai assistant")

# --- display chat history ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- handle user input ---
if prompt := st.chat_input("ask about an incident or ticket..."):
    # add user message to display and history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # get response from the oop service
    with st.spinner("ai thinking..."):
        # call the method on the OOP instance
        ai_response = st.session_state.ai_assistant.send_message(prompt)

    # add ai response to display and history
    with st.chat_message("assistant"):
        st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})