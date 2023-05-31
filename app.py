from sst.preprocessing.clean_data import merge_dataframe
from sst.preprocessing.control_chart import control_chart, split_dataframe, plot_control_chart
import os, sys
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt



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


excel_files = st.file_uploader("Choose all CSV files", accept_multiple_files= True, type= ['csv'])

if excel_files is not None:
  df = merge_dataframe(files= excel_files)
  if "File Name" in df.columns:
    df["Time"] = df["File Name"].str.extract(r"(\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})")
    df["Date"] = df["File Name"].str.extract(r"(\d{4}-\d{2}-\d{2})")


if st.button('Single Control Chart'):
  mean, upper_limit, lower_limit = control_chart(data= df, column_name= 'Area')
  sns.set_style('darkgrid')
  plot_control_chart(dataframe= df,
                      upper_limit= upper_limit,
                      mean= mean,
                      lower_limit= lower_limit,
                      category = 'Complete Data',
                      y_axis= 'Area',
                      x_axis = 'Time',
                      x_axis_sep= 10)
  



if st.button('Multiple Control Charts'):
    # splitting dataframes
    split_dataframes = split_dataframe(df= df, column_name= 'Name')
    # Accessing the individual dataframes
    for category, dataframe in split_dataframes.items():
        st.write()
        dataframe['Area'] = pd.to_numeric(dataframe['Area'], errors='coerce')

        normalized_area = (dataframe['Area'] - dataframe['Area'].mean()) / dataframe['Area'].std()
        dataframe['Normalized Area'] = normalized_area

        mean, upper_limit, lower_limit = control_chart(data= dataframe, column_name= 'Normalized Area')
        sns.set_style('darkgrid')

        plot_control_chart(dataframe= dataframe,
                           upper_limit= upper_limit,
                           mean= mean,
                           lower_limit= lower_limit,
                           category= category,
                           y_axis= 'Normalized Area',
                           x_axis = 'Time',
                           x_axis_sep= 3)

        




 

