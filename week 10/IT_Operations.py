import streamlit as st
import pandas as pd
import sys
import os

# path guarantee for absolute import
# ensures the project root directory is on the python path.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)


# import the service logic using the absolute path
from app.services.it_operations_services import get_delay_by_staff, get_delay_by_priority

st.set_page_config(page_title="it operations performance", layout="wide")

# ensure the user is logged in.
if not st.session_state.get("logged_in", False):
    st.warning("please log in to access the it operations performance dashboard.")
    st.stop()


st.header("IT OPERATIONS PERFORMANCE DASHBOARD")
st.markdown("Analysis of it ticket resolution")

# get the data from the service layer.
staff_data = get_delay_by_staff()
priority_data = get_delay_by_priority()

if staff_data.empty and priority_data.empty:
    st.error("error: could not load it ticket data. check files and logic.")
else:
    # using a two-column layout.
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("staff resolution time anomaly")
        # description of the staff resolution time anomaly chart.
        st.markdown(
            "this chart points out staff with the longest average resolution times."
        )

        # display the bar chart.
        st.bar_chart(staff_data, x='Staff Member', y='Avg Resolution Time (Hours)', color='#FF5733')

        # display raw data.
        st.dataframe(staff_data, hide_index=True)

    with col2:
        st.subheader("priority level delay bottleneck")
        # description of the priority level delay bottleneck chart.
        st.markdown(
            "this analysis highlights which priority level contributes most to delays."
        )

        # display the bar chart.
        st.bar_chart(priority_data, x='Priority Level', y='Avg Resolution Time (Hours)')

        # display raw data.
        st.dataframe(priority_data, hide_index=True)