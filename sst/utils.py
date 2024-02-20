import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime

import streamlit as st
curr_path = os.getcwd()
env_path = curr_path + "/" + ".env"

load_dotenv(env_path)
url = os.environ.get("url")
token = os.environ.get("token")

def convert_date_format(date_range):
    dates = []
    for i in date_range:
       d_str = i.strftime("%Y-%m-%d")
       dates.append(d_str)

    return dates


def get_data(dates, hostname):

    if len(dates) == 2:
        # st.write(e_date)
        
        headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        }
        updated_url = url + "start_date=" + dates[0] + "&" + "end_date=" + dates[1] + "&" + "hostname=" + hostname
        
        response = requests.get(updated_url, headers=headers)
        # Check the response status code
        if response.status_code == 200:
            # The request was successful, and you can access the response content
            data = response.json()
            df = pd.DataFrame(data)
            return df


        elif response.status_code == 401:
            # Handle the unauthorized error
            st.error("Authentication failed. Check your token.")
        else:
            # Handle other errors
            st.error(f"Error: {response.status_code} - {response.text}")