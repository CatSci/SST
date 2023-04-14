import csv
import pandas as pd
import sys, os
from sst.exception import SSTException
from sst.logger import logging

import streamlit as st
from io import StringIO


def clean_dataframe(files: list):
    all_df = []
    try:
        logging.info(f"[INFO] Cleaning Excel files started")
        progress_bar = st.progress(0)
        status_text = st.empty()
        merged_df = pd.DataFrame()
        for i, excel_file in enumerate (files):
            if excel_file is not None:
            # read the contents of the uploaded file using StringIO
                csv_contents = StringIO(excel_file.getvalue().decode('utf-8'))
                csv_reader = csv.reader(csv_contents)

                clean_data_dict = {}
                column_name = {}
                data_columns_len = 0
                for idx, row in enumerate(csv_reader):
                    if len(row) != 0 and row[0] == 'Name':
                        column_name['names'] = row
                        data_columns_len = len(row)

                    elif len(row) != 0 and len(row) == data_columns_len:
                        if row[0].split('C')[0] == 'Q':
                            clean_data_dict[idx] = row

                logging.info(f"[INFO] Converting Excel file into DataFrame")
                df = pd.DataFrame.from_dict(clean_data_dict, orient ='index', columns = column_name['names']).reset_index(drop = True)
                logging.info(f"[INFO] Adding file name as column")
                df.insert(0, 
                column = 'File Name',
                value = excel_file.name.split('.csv')[0])

                all_df.append(df)
                progress = (i + 1) / len(files)
                progress_bar.progress(progress)
                status_text.text(f"{int(progress*100)}% Cleaning Data Completed")
            else:
                st.error("File not uploaded")
        progress_bar.empty()
        status_text.empty()
        logging.info(f"[INFO] Cleaning Excel files completed")
        return all_df

    except Exception as e:
        logging.error(f"[ERROR] Error occurred in clean_dataframe function !!")
        raise SSTException(e, sys)


def merge_dataframe(files: str) -> pd.DataFrame:
    try:
        logging.info(f"[INFO] Merging all individual dataframe into singal dataframe started")
        all_df = clean_dataframe(files= files)
        progress_bar = st.progress(0)
        status_text = st.empty()
        merged_df = pd.DataFrame()
        # Merge DataFrames
        for i, df in enumerate(all_df):
            merged_df = pd.concat([merged_df, df], ignore_index=True)
            progress = (i + 1) / len(all_df)
            progress_bar.progress(progress)
            status_text.text(f"{int(progress*100)}% Merging all files Completed")

        progress_bar.empty()
        status_text.empty()
        logging.info(f"[INFO] Merging all individual dataframe into singal dataframe completed")

        return merged_df

    except Exception as e:
        logging.error(f"[Error] Error occurred in merged_dataframe function !!")
        raise SSTException(e, sys)



        
    
