import streamlit as st
import pandas as pd
import time

from config import *

pd.set_option("future.no_silent_downcasting", True)

from src.utils_app import initialize_states, display_event, compute_overall, setup_page

setup_page()

initialize_states()
col1, col2 = st.columns([9, 1], vertical_alignment="center")

with col1:
    st.title("SEGEL-BUNDESLIGA 2024 (INOFFIZIELL)")

with col2:
    st.image("./data/logo_myc.png")

tab_event1, tab_event2, tab_event3, \
tab_event4, tab_event5, tab_event6, tab_overall = st.tabs(
    ["Event 1", "Event 2", "Event 3", "Event 4", "Event 5", "Event 6", "Saison 2024"]
)

with tab_event1:

    display_event(
        title="Event 01 Wannsee",
        data_event="data_event_01"
    )

with tab_event2:
    display_event(
        title="Event 02 Warnemünde",
        data_event="data_event_02"
    )

with tab_event3:
    display_event(
        title="Event 03 Kiel - KYC",
        data_event="data_event_03"
    )

with tab_event4:
    display_event(
        title="Event 04 Kiel",
        data_event="data_event_04"
    )

with tab_event5:
    display_event(
        title="Event 05 Starnberg - MYC",
        data_event="data_event_05"
    )

with tab_event6:
    display_event(
        title="Event 06 Starnberg - BYC",
        data_event="data_event_06"
    )

with tab_overall:
    compute_overall(events=EVENTS1) # FIXME: braucht EVENTS2 für 2. Liga

print("[INFO] Rerun")
time.sleep(REFRESH_TIME)
st.rerun()