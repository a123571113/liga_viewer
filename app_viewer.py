import streamlit as st
import pandas as pd
import time

from config import *

pd.set_option("future.no_silent_downcasting", True)

from src.utils_app import initialize_states, display_event, display_overall, setup_page

setup_page()

initialize_states()
col1, col2 = st.columns([9, 1], vertical_alignment="center")

with col1:
    st.title("SEGEL-BUNDESLIGA 2024 (INOFFIZIELL)")

with col2:
    st.image("./data/logo_myc.png")

tab_L1_event1, tab_L1_event2, tab_L1_event3, tab_L1_event4, tab_L1_event5, tab_L1_event6, \
tab_L2_event1, tab_L2_event2, tab_L2_event3, tab_L2_event4, tab_L2_event5, \
tab_overall = st.tabs(
    [
        "L1 Event 1", "L1 Event 2", "L1 Event 3", "L1 Event 4", "L1 Event 5", "L1 Event 6",
        "L2 Event 1", "L2 Event 2", "L2 Event 3", "L2 Event 4", "L2 Event 5",
        "Saison 2024"
    ]
)

with tab_L1_event1:
    display_event(
        title="Event 01 Wannsee",
        data_event="data_L1_event_01",
        liga=1
    )
with tab_L1_event2:
    display_event(
        title="Event 02 Warnemünde",
        data_event="data_L1_event_02",
        liga=1
    )
with tab_L1_event3:
    display_event(
        title="Event 03 Kiel - KYC",
        data_event="data_L1_event_03",
        liga=1
    )
with tab_L1_event4:
    display_event(
        title="Event 04 Kiel",
        data_event="data_L1_event_04",
        liga=1
    )
with tab_L1_event5:
    display_event(
        title="Event 05 Starnberg - MYC",
        data_event="data_L1_event_05",
        liga=1
    )
with tab_L1_event6:
    display_event(
        title="Event 06 Starnberg - BYC",
        data_event="data_L1_event_06",
        liga=1
    )


with tab_L2_event1:
    display_event(
        title="Event 01 Wannsee",
        data_event="data_L2_event_01",
        liga=2
    )
with tab_L2_event2:
    display_event(
        title="Event 02 Warnemünde",
        data_event="data_L2_event_02",
        liga=2
    ) 
with tab_L2_event3:
    display_event(
        title="Event 03 Kiel",
        data_event="data_L2_event_03",
        liga=2
    )
with tab_L2_event4:
    display_event(
        title="Event 04 Starnberg - MYC",
        data_event="data_L2_event_04",
        liga=2
    )
with tab_L2_event5:
    display_event(
        title="Event 05 Starnberg - BYC",
        data_event="data_L2_event_05",
        liga=2
    )



with tab_overall:
    display_overall()

# print("[INFO] Rerun")
# time.sleep(REFRESH_TIME)
# st.rerun()