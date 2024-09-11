import numpy as np

BOATS = 6
FLIGHTS = 16
race_columns = ['Flight {}'.format(i) for i in range(1,FLIGHTS+1)]

DISPLAY_COLORCODING = True
REFRESH_TIME = 60 # in seconds 

TEAMS_L1 = [
    'ASVW', 'BYC (BA)', 'BYC (BE)', 'BYCÜ', 'DYC',
    'FSC', 'JSC', 'KYC (BW)', 'KYC (SH)', 'MSC', 'MYC',
    'NRV', 'RSN', 'SMCÜ', 'SV03', 'SVI', 'VSaW', 'WYC'
]

TEAMS_L2 = [
    "ASV-HH", "BOH-YC", "BSC", "BuSC", "CYCM", "ENSFR", 
    "ETUF", "HSC", "KaR", "LSV", "LYC", "PYC", 
    "SCSz", "SCV",  "SVWu", "WSW", "WYD", "YCM"
]

BUCHSTABEN = {
    'OCS': BOATS + 1,
    'DSQ': BOATS + 1,
    'DNF': BOATS + 1,
    'DNC': BOATS + 1,
    'RET': BOATS + 1,
    'NSC': BOATS + 1,
    'No result': np.nan,
}

EVENTS_L1 = [
    ("event_01", "get_data_steady_event"),
    ("event_02", "get_data_steady_event"),
    ("event_03", "get_data_steady_event"),
    ("event_04", "get_data_steady_event"),
    ("event_05", "get_data_current_event"),
    ("event_06", "get_data_steady_event")
]

EVENTS_L2 = [
    ("event_01", "get_data_steady_event"),
    ("event_02", "get_data_steady_event"),
    ("event_03", "get_data_steady_event"),
    ("event_04", "get_data_current_event"),  
    ("event_05", "get_data_steady_event")
]