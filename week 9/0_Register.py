import streamlit as st
import sqlite3
import sys
import os

# ensure project root is on the path to find the app folder
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# import necessary functions from service and data layers
from app.services.user_service import register_user
from app.data.db import connect_database

# page setup
st.set_page_config(page_title="Register account", layout="centered")

st.title("Create a new account")

with st.form("Registration_form"): # starts a form
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    register_submitted = st.form_submit_button("Register account", type="primary")

    if register_submitted:
        # validation check to see if the fields were left empty or not
        if not new_username or not new_password or not confirm_password:
            st.error("Please fill in all fields.")
        # check if passwords match
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                # connect to the database
                conn = connect_database()
                # call the secure service function to register the user
                success, msg = register_user(conn, new_username, new_password, role='user')
                conn.close()

                if success:
                    st.success(msg)
                    st.info("Registration complete. Go to the home page to log in.")
                else:
                    st.error(msg)

            except sqlite3.OperationalError:
                st.error("database connection failed.")
            except Exception as e:
                st.error(f"an unexpected error occurred: {e}")

st.markdown("---")
st.markdown("already registered? navigate to the home page to log in.")