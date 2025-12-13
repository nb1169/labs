# IT_Operations.py

import streamlit as st
import pandas as pd
import sys
import os

# added the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

# NEW IMPORTS: use the new OOP services
from services.database_manager import DatabaseManager
from app.data.db import DB_PATH

st.set_page_config(page_title="it operations dashboard", layout="wide")

# check if user is logged in
if not st.session_state.get("logged_in"):
    st.error("please log in via the home page.")
    st.stop()

st.title("it operations dashboard")

# --- initialize the database manager ---
db_manager = DatabaseManager(DB_PATH)

try:
    # 1. fetch all ticket objects from the database manager
    tickets_list = db_manager.get_all_tickets()

    if not tickets_list:
        st.warning("no it tickets found in the database.")
        st.stop()

    # 2. convert list of ittICKET objects to a dataframe for display and charting
    data_for_display = []
    for ticket in tickets_list:
        # use the getter methods of the ITTicket object
        data_for_display.append({
            'ticket id': ticket.get_ticket_id(),
            'title': ticket.get_title(),
            'priority': ticket.get_priority(),
            'status': ticket.get_status(),
            'assigned to': ticket.get_assigned_to(),
            # add other fields as needed for display/charts
        })

    tickets_df = pd.DataFrame(data_for_display)

    # --- dashboard components ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ticket priority distribution")
        priority_counts = tickets_df['priority'].value_counts().reset_index()
        priority_counts.columns = ['priority', 'count']
        st.bar_chart(priority_counts, x='priority', y='count', color='#00aaff')

    with col2:
        st.subheader("staff assignment breakdown")
        staff_counts = tickets_df['assigned to'].value_counts().reset_index()
        staff_counts.columns = ['staff member', 'count']
        st.bar_chart(staff_counts, x='staff member', y='count', color='#ff6347')

    st.subheader("raw ticket data")
    st.dataframe(tickets_df, use_container_width=True)

finally:
    db_manager.close()