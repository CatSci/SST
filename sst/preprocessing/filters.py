import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Add filters")
    user_cat_input = None
    # st.write(df.columns)
    if modify:
        y_col_filters = ['Name']
        to_filter_columns = st.multiselect("Filter data on", y_col_filters)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 5:
                
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                
                df = df[df[column].isin(user_cat_input)]


    
    return df, user_cat_input

def filter_y_axis():
    values = ['Area', 'RT [min]', 'Tailing']
    y_label = st.selectbox('Select data for Y axis', (values))

    return y_label


def filter_x_axis():
    values = ['Time']
    x_label = st.selectbox('Select data for X axis', (values))

    return x_label

