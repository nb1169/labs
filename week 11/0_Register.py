# 0_Register.py

import streamlit as st
import sys
import os

# added the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

# NEW IMPORTS: use the new OOP services
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from app.data.db import DB_PATH

st.set_page_config(page_title="Register", layout="centered")

st.title("register new user")

# --- initialize the database and auth managers ---
# uses the DB_PATH defined in app/data/db.py
db_manager = DatabaseManager(DB_PATH)
auth_manager = AuthManager(db_manager)

with st.form("register_form"):
    new_username = st.text_input("username")
    new_password = st.text_input("password", type="password")
    confirm_password = st.text_input("confirm password", type="password")

    submitted = st.form_submit_button("register", type="primary")

    if submitted:
        if not new_username or not new_password or not confirm_password:
            st.error("please fill in all fields.")
        elif new_password != confirm_password:
            st.error("passwords do not match.")
        else:
            # call the oop service method for registration
            success, msg = auth_manager.register_user(new_username, new_password, role='user')

            if success:
                st.success(f"{msg} you can now log in.")
                st.balloons()
            else:
                st.error(msg)

db_manager.close()