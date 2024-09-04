import streamlit as st
import pandas as pd
from pymongo import MongoClient

from config import *

uri = f"mongodb+srv://{st.secrets['database']['user']}:{st.secrets['database']['password']}@cluster0.3rpqm.mongodb.net/dsbl?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["dsbl"]

def load_data_mongo(event: str) -> pd.DataFrame:

    collection = db[event] 

    data = collection.find()

    data_list = list(data)

    df = pd.DataFrame(data_list)

    df.drop(["_id"], axis=1, inplace=True)

    print("[INFO] Data loaded from MongoDB.")

    return df


def load_data_parquet(event: str) -> pd.DataFrame:
    df = pd.read_parquet(path=f"./data/{event}.parquet")
    return df

def get_data_google(link_id: str, stupid_formatting: int = -1) -> pd.DataFrame:

    if stupid_formatting == 0:
        df = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/' +
            link_id  +
            '/export?gid=0&format=csv',
            skiprows=2,
        )
        df.drop(["Unnamed: 0", "Overall"], axis=1, inplace=True)

    elif stupid_formatting == 1:

        df = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/' +
            link_id  +
            '/export?gid=0&format=csv',
            skiprows=1,
        )
        df.drop(['Unnamed: 0', "Overall"], axis=1, inplace=True)
        
        df[14] = np.nan
        df[15] = np.nan
        df[16] = np.nan
        
    else:
        df = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/' +
            link_id  +
            '/export?gid=0&format=csv',
            skiprows=1,
        )
        df.drop(["1.", "Overall"], axis=1, inplace=True)
    
    print(df)
    columns = ["Teams", "SCP"]
    columns.extend([f'Flight {i}' for i in range(1, FLIGHTS + 1)])

    df.columns = columns

    print("[INFO] Data loaded from Google Docs.")
    return df