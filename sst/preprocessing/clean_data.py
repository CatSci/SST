import csv
import pandas as pd
import sys, os
from sst.exception import SSTException
from sst.logger import logging

import streamlit as st



def clean_dataframe(folder: str, files: list):
    all_df = []
    try:
        logging.info(f"[INFO] Cleaning Excel files started")
        for i in range(len(files)):
            with open(folder + files[i], 'r') as file:
                csv_reader = csv.reader(file)

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
            value = files[i].split('.csv')[0])

            all_df.append(df)
        
        logging.info(f"[INFO] Cleaning Excel files completed")
        return all_df

    except Exception as e:
        logging.error(f"[ERROR] Error occurred in clean_dataframe function !!")
        raise SSTException(e, sys)


def merge_dataframe(folder: str, files: str) -> pd.DataFrame:
    try:
        logging.info(f"[INFO] Merging all individual dataframe into singal dataframe started")
        merged_df = pd.DataFrame()
        all_df = clean_dataframe(folder= folder, files= files)
        # Merge DataFrames
        for df in all_df:
            merged_df = pd.concat([merged_df, df], ignore_index=True)

        logging.info(f"[INFO] Merging all individual dataframe into singal dataframe completed")
        return merged_df

    except Exception as e:
        logging.error(f"[Error] Error occurred in merged_dataframe function !!")
        raise SSTException(e, sys)



        
    