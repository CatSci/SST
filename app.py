from sst.preprocessing.clean_data import merge_dataframe
from sst.preprocessing.control_chart import control_chart, split_dataframe, plot_control_chart
from sst.preprocessing.filters import filter_dataframe, filter_y_axis, filter_x_axis

import os, sys
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px



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


excel_files = st.file_uploader("Choose all CSV files", accept_multiple_files=True, type=['csv'])


if excel_files is not None:
    if not st.session_state["merged_done"]:
        merged_df = merge_dataframe(files=excel_files)

    df = merged_df.copy()  # Create a copy of the merged dataframe
    if "File Name" in df.columns:
        df["Time"] = df["File Name"].str.extract(r"(\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})")
        df["Date"] = df["File Name"].str.extract(r"(\d{4}-\d{2}-\d{2})")


        df, user_cat_input = filter_dataframe(df=df)
        # select what to display on y axis
        y_label = filter_y_axis()
        x_label = filter_x_axis()

        normalize_bool = st.checkbox('Do you want to normalize the data')
    



# if st.button('Single Control Chart'):
#   mean, upper_limit, lower_limit = control_chart(data= df, column_name= 'Area')
#   sns.set_style('darkgrid')
#   plot_control_chart(dataframe= df,
#                       upper_limit= upper_limit,
#                       mean= mean,
#                       lower_limit= lower_limit,
#                       category = 'Complete Data',
#                       y_axis= 'Area',
#                       x_axis = 'Time',
#                       x_axis_sep= 10)
  


if st.button('Multiple Control Charts'):
    # splitting dataframes
    # st.write(df)
    split_dataframes = split_dataframe(df= df, column_name= 'Name')
    # Accessing the individual dataframes
    for category in user_cat_input:
        dataframe = df[df['Name'] == category]
        
        col = 'Normalized' + ' ' + y_label
        dataframe[y_label] = pd.to_numeric(dataframe[y_label], errors='coerce')
        if normalize_bool:
          normalized_area = (dataframe[y_label] - dataframe[y_label].mean()) / dataframe[y_label].std()
          dataframe[col] = normalized_area
          mean, upper_limit, lower_limit = control_chart(data= dataframe, column_name= col)
          sns.set_style('darkgrid')

          plot_control_chart(dataframe= dataframe,
                            upper_limit= upper_limit,
                            mean= mean,
                            lower_limit= lower_limit,
                            category= category,
                            y_axis= col,
                            x_axis = x_label,
                            x_axis_sep= 3)
        else:
          mean, upper_limit, lower_limit = control_chart(data= dataframe, column_name= y_label)
          sns.set_style('darkgrid')

          plot_control_chart(dataframe= dataframe,
                            upper_limit= upper_limit,
                            mean= mean,
                            lower_limit= lower_limit,
                            category= category,
                            y_axis= y_label,
                            x_axis = x_label,
                            x_axis_sep= 3)

        




 

