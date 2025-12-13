import streamlit as st
import sqlite3
import sys
import os

# added the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir)
sys.path.append(project_root)

from app.data.db import connect_database
from app.services.user_service import login_user, setup_database_complete


st.set_page_config(page_title="Intelligence Platform", layout="centered")

# initialize session state variables if they don't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_role = None

# if user is already logged in, redirect them
if st.session_state.logged_in:
    st.switch_page("pages/1_Dashboard.py")
    st.stop()

st.title("Login")

with st.form("login_form"): # login form that asks for username and password
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    submitted = st.form_submit_button("Log In", type="primary")

    if submitted:
        # check if any fields are left empty
        if not login_username or not login_password:
            st.error("Enter details.")
            st.stop()

        try:
            # connect to the database
            conn = connect_database()
            setup_database_complete(conn)

            # call the secure login service function
            success, msg, user_data = login_user(conn, login_username, login_password)
            conn.close()

            if success:
                # on success, set session state variables
                st.session_state.logged_in = True
                st.session_state.username = user_data[1]
                st.session_state.user_role = user_data[3]

                st.success(f"Welcome, {st.session_state.username}!")
                # redirect to the main dashboard
                st.switch_page("pages/1_Dashboard.py")
            else:
                # show error message
                st.error(msg)

        # handle specific exceptions
        except sqlite3.OperationalError:
            st.error("Database setup failed. Please run main.py first.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")