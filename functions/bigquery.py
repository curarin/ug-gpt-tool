import pandas_gbq
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime
import streamlit as st
import json


bq_cost = "seo-datawarehouse-379113.ug_gpt_cost_db.cost_overview"

data = {
    "type": "service_account",
    "project_id": st.secrets["service_account"]["project_id"],
    "private_key_id": st.secrets["service_account"]["private_key_id"],
    "private_key": st.secrets["service_account"]["private_key"],
    "client_email": st.secrets["service_account"]["client_email"],
    "client_id": st.secrets["service_account"]["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": st.secrets["service_account"]["client_x509_cert_url"],
    "universe_domain": "googleapis.com"
}
service_account_json = json.dumps(data, indent=4)
service_account_info = json.loads(service_account_json)
current_date = datetime.now().strftime("%Y-%m-%d")

credentials = service_account.Credentials.from_service_account_info(service_account_info)

def to_bigquery(tool, total_cost, destination, tool_specific_data, lang_wanted):
    destination = destination.lower()
    data = {
        'date': current_date,
        'tool': tool,
        'total_cost': total_cost,
        'destination': destination,
        'tool_specific_data': tool_specific_data,
        'language_used': lang_wanted,
        'name': None
        }
    # Create a DataFrame
    df = pd.DataFrame(data, index=[0])
    pandas_gbq.to_gbq(df, bq_cost, project_id="seo-datawarehouse-379113", if_exists="append", credentials=credentials)

def fetch_total_cost_current_month():
    # Create a service account credentials object
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    # Define the BigQuery SQL query to get the sum of cost for the current month
    query = f"""
    SELECT *
    FROM `seo-datawarehouse-379113.ug_gpt_cost_db.cost_overview`
    WHERE DATE_TRUNC(date, MONTH) = DATE_TRUNC(CURRENT_DATE(), MONTH)
    """

    # Load the data from BigQuery into a Pandas DataFrame
    df = pd.read_gbq(query, project_id="seo-datawarehouse-379113", credentials=credentials)
    df_no_duplicates = df.drop_duplicates(subset=['total_cost', 'destination', 'tool_specific_data'])
    grouped_tool_cost = df_no_duplicates.groupby('tool')['total_cost'].sum().reset_index()
    total_sum = grouped_tool_cost['total_cost'].sum()
    total_row = pd.DataFrame({'': ['Gesamtkosten'], 'Kosten im aktuellen Monat (in USD)': [total_sum]})

    grouped_tool_cost = grouped_tool_cost.rename(columns={
        "tool": "GPT Tool Name",
        "total_cost": "Kosten im aktuellen Monat (in USD)"
    })

    st.write(grouped_tool_cost)
    st.write(total_row)