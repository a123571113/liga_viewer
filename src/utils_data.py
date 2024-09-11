import streamlit as st
import pandas as pd
from pymongo import MongoClient

from config import *


@st.cache_resource
def init_connection_liga_1():
    uri = f"mongodb+srv://{st.secrets['database']['user']}:{st.secrets['database']['password']}@cluster0.3rpqm.mongodb.net/dsbl?retryWrites=true&w=majority"
    client = MongoClient(uri)
    return client

@st.cache_resource
def init_connection_liga_2():
    uri = f"mongodb+srv://{st.secrets['database']['user']}:{st.secrets['database']['password']}@cluster0.3rpqm.mongodb.net/dsbl2?retryWrites=true&w=majority"
    client = MongoClient(uri)
    return client


def load_data_mongo(event: str, database:str) -> pd.DataFrame:

    if database=="dsbl":
        client = init_connection_liga_1()

    elif database == "dsbl2":
        client = init_connection_liga_2()        

    else:
        print("[ERROR] Database does not exist")
        exit()

    db = client[database]

    collection = db[event] 

    data = collection.find()

    data_list = list(data)

    df = pd.DataFrame(data_list)

    df.drop(["_id"], axis=1, inplace=True)

    print(f"[INFO] Data from {database} - {event} loaded.")

    return df


def get_data_current_event(event: str, database: str) -> pd.DataFrame:
    return load_data_mongo(event=event, database=database)


@st.cache_data
def get_data_steady_event(event: str, database: str) -> pd.DataFrame:
    return load_data_mongo(event=event, database=database)
