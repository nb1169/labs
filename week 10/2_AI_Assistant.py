import streamlit as st
import time
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

from app.services.ai_services import get_ai_response

# initializes login state to false if it doesnt exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# initializes the user role to none if it doesnt exist
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# sets the browser tab title
st.set_page_config(page_title="AI Security Assistant")

# ensure the user is logged in before displaying the page
if not st.session_state.get("logged_in", False):
    st.warning("please log in to access the ai security assistant.")
    st.stop()

st.title("AI Security Assistant")
st.markdown("Ask the soc expert for advice on incident response, threats, or mitigation strategies.")

# session state initialization for chat
# initialize messages list if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
# loop through existing messages and display them
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# handle user input
# check if the user has entered a new prompt
if prompt := st.chat_input("Ask a security question..."):

    # add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # get ai response from service layer
    with st.chat_message("assistant"):
        with st.spinner("thinking..."):
            # call the service layer function
            response = get_ai_response(st.session_state.messages)

            placeholder = st.empty()
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                placeholder.markdown(full_response + "▌")
                time.sleep(0.05)
            placeholder.markdown(full_response)

    # add ai response to history
    st.session_state.messages.append({"role": "assistant", "content": response})