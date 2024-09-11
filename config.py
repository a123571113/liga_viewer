import numpy as np

import data.data_pairing_list
import data.data_pairing_list2

BOATS = 6
FLIGHTS = 16
EVENTS1 = len(data.data_pairing_list.data)
EVENTS2 = len(data.data_pairing_list2.data)

BUCHSTABEN = {'OCS': BOATS + 1,
              'DSQ': BOATS + 1,
              'DNF': BOATS + 1,
              'DNC': BOATS + 1,
              'No result': np.nan,
              }

max_race_columns = 16
race_columns = ['Flight {}'.format(i) for i in range(1,max_race_columns+1)]

DISPLAY_COLORCODING = True
REFRESH_TIME = 60 # in seconds 