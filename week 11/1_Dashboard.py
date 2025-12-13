import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.incidents import get_all_incidents, delete_incident
from app.services.user_service import setup_database_complete
import plotly.express as px

# checks if user is logged in
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access the Dashboard.")
    st.stop()

# page setup
st.set_page_config(page_title="Cyber Dashboard", layout="wide")
st.title("Cyber Incident Data Viewer")
st.caption(f"Logged in as: {st.session_state.username}")


# simple data loading function
def load_incident_data():
    conn = connect_database()
    setup_database_complete(conn)
    df_incidents = get_all_incidents(conn)
    conn.close()
    df_incidents['timestamp'] = pd.to_datetime(df_incidents['timestamp'])
    return df_incidents


df_incidents = load_incident_data()

# logout Button
if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.switch_page("Home.py")

st.divider()

st.header("Incident Analysis")
chart_col1, chart_col2 = st.columns(2) # creates 2 columns side by side

# threat Trend
with chart_col1:
    st.subheader("Incident Volume Over Time")
    # Group data by the week of the year to show trends simply
    df_trend = df_incidents.groupby(df_incidents['timestamp'].dt.to_period('W')).size().reset_index(name='Count')
    df_trend['timestamp'] = df_trend['timestamp'].astype(str)  # convert period values to string to put in the chart

    fig_trend = px.line(
        df_trend,
        x='timestamp',
        y='Count',
        title='Weekly Incident Count (Phishing Surge Analysis)'  # title for the chart
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# bar chart
with chart_col2:
    st.subheader("Incidents by Category")
    # Group by category to show which type has the most volume
    df_category = df_incidents['category'].value_counts().reset_index(name='Count')

    fig_category = px.bar(
        df_category,
        x='category',
        y='Count',
        title='Distribution of Incidents by Type'
    )
    st.plotly_chart(fig_category, use_container_width=True)

st.divider()

# displays the data
st.subheader("Current Incident Records")
st.dataframe(df_incidents, use_container_width=True) # makes a table that fills the width


st.header("Incident Deletion Console")

# Check if data exists before showing the delete form
if not df_incidents.empty:
    incident_id_list = df_incidents['incident_id'].unique()

    with st.form("delete_form", clear_on_submit=True):   # opens the form to delete
        delete_id = st.selectbox("Select ID to Delete", incident_id_list)

        if st.form_submit_button("Delete Incident", type="primary", help="This action is irreversible."): # submit button
            conn = connect_database()
            rows = delete_incident(conn, delete_id)
            conn.close()
            if rows > 0: # if one row is deleted then prints a message showing a record was permanently deleted
                st.warning(f"Incident {delete_id} permanently deleted.")
                # Refresh data display
                st.rerun()
else:
    st.info("No incidents found in the database.")