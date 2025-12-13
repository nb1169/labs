# Home.py
import streamlit as st
import sqlite3
import sys
import os

# added the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir)
sys.path.append(project_root)

# NEW IMPORTS: use the new service classes
from app.data.db import connect_database
from app.data.db import DB_PATH # import db path for DatabaseManager init
from app.services.user_service import setup_database_complete
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager


st.set_page_config(page_title="Intelligence Platform", layout="centered")

# initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_role = None

# if user is already logged in, redirect them
if st.session_state.logged_in:
    st.switch_page("pages/1_Dashboard.py")
    st.stop()

st.title("Login")

# setup the database and auth managers
db_manager = DatabaseManager(DB_PATH)
auth_manager = AuthManager(db_manager)

with st.form("login_form"): # login form that asks for username and password
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    submitted = st.form_submit_button("Log In", type="primary")

    if submitted:
        if not login_username or not login_password:
            st.error("enter details.")
            st.stop()

        try:
            # ensure database is set up before trying to log in (uses old procedural setup)
            conn = connect_database()
            setup_database_complete(conn)
            conn.close()

            # call the secure login service (OOP)
            user = auth_manager.login_user(login_username, login_password)

            if user:
                # on success, set session state variables using user object getter methods
                st.session_state.logged_in = True
                st.session_state.username = user.get_username()
                st.session_state.user_role = user.get_role()

                st.success(f"welcome, {st.session_state.username}!")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("user not found or incorrect password.")

        # handle specific exceptions
        except sqlite3.OperationalError:
            st.error("database setup failed. please run main.py first.")
        except Exception as e:
            st.error(f"an unexpected error occurred: {e}")
        finally:
            db_manager.close() # ensure connection is closed