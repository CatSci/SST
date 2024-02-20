from sst.preprocessing.clean_data import merge_dataframe
from sst.preprocessing.control_chart import control_chart, split_dataframe, plot_control_chart
from sst.preprocessing.filters import filter_dataframe, filter_y_axis, filter_x_axis
from sst.utils import convert_date_format, get_data

import os, sys
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import datetime


# hide streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
# background-color: #ed9439;
st.markdown("""
<style>
.navbar {
  height: 80px;
  background-color: #ed9439;
  color: #ed9439;
}
.navbar-brand{
    font-size: 40px;
    margin-left:40px;
}
</style>""", unsafe_allow_html= True)


st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark">
  <a class="navbar-brand" href="#" target="_blank">CatSci</a>
  

</nav>
""", unsafe_allow_html=True)



st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ed9439;
    color:#0f1b2a;
    border:None;
}
div.stButton > button:first-child:focus {
    background-color: #ed9439;
    color:#0f1b2a;
    border:None;
}
</style>""", unsafe_allow_html=True)

st.title("SST Visualization")
st.info('Please make sure to upload **all files** !!')


# Define a session state variable to track if merging and preprocessing have been done
if "merged_done" not in st.session_state:
    st.session_state["merged_done"] = False

# Initialize the "merged_df" key in session state to an empty dataframe
if "merged_df" not in st.session_state:
    st.session_state["merged_df"] = pd.DataFrame()

# Get current year
start_year = 2023
end_year = datetime.datetime.now().year + 10

# # User input for the date range
# date_range = st.date_input(
#     "Select your vacation range",
#     (
#         datetime.date(start_year, 1, 1),
#         datetime.date(start_year, 7, 1)
#     ),
#     min_value=datetime.date(start_year, 1, 1),
#     max_value=datetime.date(end_year, 12, 1),
#     format="DD.MM.YYYY"
# )


# User input for the date range
date_range = st.date_input(
    "Select your vacation range",
    (
        datetime.date(start_year, 10, 1),
        datetime.date(start_year, 10, 31)
    ),
    min_value=datetime.date(start_year, 1, 1),
    max_value=datetime.date(end_year, 12, 1)
)

devices = {
    "Lancelot" : "DESKTOP-E75MDJA",
    "Gromit" : "DESKTOP-EFH253C",
    "Arthur dad" : "PC-CZC124813X",
    "Percy" : "DESKTOP-REMA8OU",
    "Wallece" : "DESKTOP-JKSM31H",
    "Merlin" : "DESKTOP-QFL5IDO",
}


hostname = st.selectbox(
    'From which device you want to extract data?',
    (devices.keys()))
    # ('DESKTOP-QFL5IDO', 'DESKTOP-REMA8OU', 'PC-CZC124813X', 'DESKTOP-E75MDJA'))

y_label = filter_y_axis()
# x_label = filter_x_axis()


# st.write(devices[hostname])


# st.write(devices.keys())
# st.write(devices.values())

if len(date_range) == 2:
    dates = convert_date_format(date_range)
else:
    st.error("Please select date")

if st.button("Plot Control Chart"):
    with st.spinner('Wait for it...'):
        data = get_data(dates = dates, hostname= devices[hostname])
        if len(data.index) != 0:
            user_cat_input = data['name'].unique()

            df = data.sort_values(by='date', ascending=True)

            split_dataframes = split_dataframe(df= df, column_name= 'name')
            # Accessing the individual dataframes
            for category in sorted(user_cat_input):
                dataframe = df[df['name'] == category]
                # st.dataframe(dataframe)
                
                dataframe[y_label] = pd.to_numeric(dataframe[y_label], errors='coerce')
                mean, upper_limit, lower_limit = control_chart(data= dataframe, column_name= y_label)
                sns.set_style('darkgrid')

                
                plot_control_chart(dataframe= dataframe,
                                upper_limit= upper_limit,
                                mean= mean,
                                lower_limit= lower_limit,
                                category= category,
                                y_axis= y_label,
                                x_axis_sep= 3)
        
        else:
            st.error("Data not found. Please change the Date or Device name")
        


        




 

