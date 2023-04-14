from sst.preprocessing.clean_data import merge_dataframe
import os, sys
import streamlit as st


folder = './sst/data/'
files = os.listdir('./sst/data/')

st.title("SST Visualization")
st.info('Please make sure to upload **all files** !!')

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

excel_files = st.file_uploader("Choose all CSV files", accept_multiple_files= True, type= ['csv'])

if st.button('Clean Data'):
    df = merge_dataframe(folder= folder, files= files)
    st.dataframe(df)

# if __name__ == "__main__":
#     df = merge_dataframe(folder= folder, files= files)