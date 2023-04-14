from sst.preprocessing.clean_data import merge_dataframe
import os, sys
import streamlit as st



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
  <a class="navbar-brand" href="https://catsci-sst-visualization.streamlit.app/" target="_blank">CatSci</a>
  

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

if st.button('Clean Data'):
    df = merge_dataframe(files= excel_files)
    st.dataframe(df)

# if __name__ == "__main__":
#     df = merge_dataframe(folder= folder, files= files)