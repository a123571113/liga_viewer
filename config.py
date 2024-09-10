import numpy as np

BOATS = 6
FLIGHTS = 16
EVENTS = 6
TEAMS = ['ASVW', 'BYC (BA)', 'BYC (BE)', 'BYCÜ', 'DYC', 'FSC', 'JSC', 'KYC (BW)', 'KYC (SH)', 'MSC', 'MYC', 'NRV', 'RSN',
         'SMCÜ', 'SV03', 'SVI', 'VSaW', 'WYC']

BUCHSTABEN = {'OCS': BOATS + 1,
              'DSQ': BOATS + 1,
              'DNF': BOATS + 1,
              'DNC': BOATS + 1,
              'No result': np.nan,
              }

max_race_columns = 16
race_columns = ['Flight {}'.format(i) for i in range(1,max_race_columns+1)]

DISPLAY_COLORCODING = True
REFRESH_TIME = 10 # in seconds 