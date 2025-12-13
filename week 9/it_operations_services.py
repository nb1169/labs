import pandas as pd
from app.data.it_tickets_data import load_it_tickets_data


def calculate_resolution_metrics():
    # load data and filter for resolved tickets.

    df = load_it_tickets_data()
    if df is None:
        return None

    # filter for resolved tickets.
    resolved_df = df[df['status'] == 'Resolved'].copy()

    return resolved_df


def get_delay_by_staff():
    # calculate average resolution time grouped by staff member.

    resolved_df = calculate_resolution_metrics()
    if resolved_df is None:
        return pd.DataFrame()

    # group by staff and calculate the mean duration
    delay_by_staff = resolved_df.groupby('staff_member')['resolution_duration'].mean().sort_values(
        ascending=False).reset_index()
    delay_by_staff.columns = ['Staff Member', 'Avg Resolution Time (Hours)']
    return delay_by_staff


def get_delay_by_priority():
    # calculate average resolution time grouped by ticket priority.

    resolved_df = calculate_resolution_metrics()
    if resolved_df is None:
        return pd.DataFrame()

    # group by priority and calculate the mean duration.
    delay_by_priority = resolved_df.groupby('priority')['resolution_duration'].mean().sort_values(
        ascending=False).reset_index()
    delay_by_priority.columns = ['Priority Level', 'Avg Resolution Time (Hours)']
    return delay_by_priority