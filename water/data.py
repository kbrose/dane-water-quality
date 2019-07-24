from pathlib import Path
import logging

import pandas as pd
from scipy.stats.mstats import gmean

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FOLDER = Path(__file__).parents[1] / 'data'

# Map all observed site values to a standard list
SITE_MAP = {
    'Bernies': 'bernies',
    'Vilas': 'vilas',
    'James Madison': 'james_madison',
    'Tenney': 'tenney',
    'Warner': 'warner',
    'BB Clarke': 'bb_clarke',
    'Olbrich': 'olbrich',
    'Esther': 'esther',
    'Olin': 'olin',
    'Hoofers Pier': 'hoofers_pier',
    'Memorial Union': 'memorial_union',
    'Hudson': 'hudson',
    'Brittingham': 'brittingham',
    'Spring Harbor': 'spring_harbor',
    'Marshall': 'marshall',
    'Mendota Co Park': 'mendota_co_park',
    'Stewart Lake Beach': 'stewart',
    'Yahara Mouth': 'yahara',
    'Goodland Park': 'goodland',
    'Vilas-Left': 'vilas',
    'Vilas-Right': 'vilas',
    'Vilas-Center': 'vilas',
    'Kegonsa': 'kegonsa',
    'Bernies-1': 'bernies',
    'Bernies-2': 'bernies',
    'Bernies-3': 'bernies',
    'Bernies-4': 'bernies',
    'Blind Dup': 'blind_dup',
    'BB Clarke-1': 'bb_clarke',
    'BB Clarke-2': 'bb_clarke',
    'BB Clarke-3': 'bb_clarke',
    'BB Clarke-4': 'bb_clarke',
    'BB Clarke-5': 'bb_clarke',
    'Starkweather Creek': 'starkweather_creek',
    '30" Outfall Below Vilas': 'vilas',
    'Wingra Creek': 'wingra_creek',
    'Law Park Shoreline': 'law_park',
    'IM-Center': 'im',
    'IM-North': 'im',
    'IM-East': 'im',
    'IM-West': 'im',
    'Picnic Point': 'picnic_point',
    'Porter Boathouse': 'porter_boathouse',
    '3819 Monona Dr.': 'monona_drive',
    'Warner Lagoon 1': 'warner_lagoon',
    'Warner Lagoon 2': 'warner_lagoon',
    'Warner Lagoon 3': 'warner_lagoon',
    'Brittingham-1': 'brittingham',
    'Brittingham-2': 'brittingham',
    'Brittingham-3': 'brittingham',
    'Brittingham-4': 'brittingham',
    'Right of Memorial Union Beach': 'memorial_union',
    'Vilas Right': 'vilas',
    'Vilas Center': 'vilas',
    'Vilas Left': 'vilas',
    'Wingra City Dock': 'wingra_city_dock',
    'Wingra Center of Lake': 'wingra_lake',
    'Brittingham 2': 'brittingham',
    'Badger Mill Creek': 'badger_mill_creek',
    'Law Park Shoreline- North': 'law_park',
    'Law Park Shoreline- Center': 'law_park',
    'Law Park Shoreline- South': 'law_park',
    'Maple Bluff-2': 'maple_bluff',
    '1339 Morrison': 'morrison',
    'Warner-1': 'warner',
    'Warner-2': 'warner',
    'Warner-3': 'warner',
    'Warner-4': 'warner',
    'Bernies #1 IN': 'bernies',
    'Bernies #2 OUT': 'bernies',
    'Goodland Park #1': 'goodland',
    'Goodland Park #2': 'goodland',
    'Goodland Park #3': 'goodland',
    'Goodland Park #4': 'goodland',
    'Goodland Park #5': 'goodland',
    'Goodland Park #6': 'goodland',
    'Mendota Co Park #7 Inlet': 'mendota_co_park',
    'Mendota Co Park #1': 'mendota_co_park',
    'Mendota Co Park #2': 'mendota_co_park',
    'Mendota Co Park #3': 'mendota_co_park',
    'Mendota Co Park #4': 'mendota_co_park',
    'Mendota Co Park #5': 'mendota_co_park',
    'Mendota Co Park #6': 'mendota_co_park',
    'Mendota Co Park #7': 'mendota_co_park',
    'Olin-1': 'olin',
    'Olin-2': 'olin',
    'Olin-3': 'olin',
    'Olin-4': 'olin',
    'Mendota Co Park Railing': 'mendota_co_park',
    'Vilas Lagoon': 'vilas',
    'Wingra (across from parking entry)': 'wingra',
    'Wingra Boat Ramp': 'wingra',
    'Wingra Beach West End': 'wingra',
    'Mendota Co Park Inlet': 'mendota_co_park',
    'IM Shore': 'im',
    'IM Shore #2': 'im',
    'IM-South': 'im',
    'Crew House': 'crew_house',
    'Olin Canoe Launch': 'olin',
    'Esther Shallow (1 ft)': 'esther',
    'Esther Medium (2 ft)': 'esther',
    'Esther Deep (3 ft)': 'esther',
    'Olin (1 ft)': 'olin',
    'Olin (2 ft)': 'olin',
    'Bernies-in': 'bernies',
    'Bernies-out': 'bernies',
    'Outfall South of Olbrich': 'olbrich',
    'IN 4656-003': 'im',
    '1M-East': 'im',
    '1M-South': 'im',
    '1M-West': 'im',
    'Marshall Park Boating Outlet': 'marshall',
    'Maple Bluff': 'maple_bluff',
    'Marshal': 'marshall',
    'Law Park Shoreline - East': 'law_park',
    'Law Park Shoreline - West': 'law_park',
    'Mendota Co Park (Outside inclosure)': 'mendota_co_park',
    'Yahara River': 'yahara',
    'Outfall Near Dam': '',
    'Vilas #1': 'vilas',
    'Vilas #2': 'vilas',
    'Vilas #3': 'vilas',
    'Vilas 1 (3Hr. Parking)': 'vilas',
    'Vilas 2 (2nd Tree)': 'vilas',
    'Vilas 3 (across from parking lot)': 'vilas',
    'Vilas 4 (right of ramp)': 'vilas',
    'Vilas 5 (tree in lot)': 'vilas',
    'Vilas 6 (beach)': 'vilas',
    'IM Turn #3': 'im',
    'IM Turn #4': 'im',
    'IM Turn #2': 'im',
    'Pipe at Goodland': 'goodland',
    'Goodland Park (inside)': 'goodland',
    'Goodland Park (outside)': 'goodland',
    'Goodland Park (pipe)': 'goodland',
    'Lake Mendota (not specified)': 'mendota_lake',
    'Goodland (in)': 'goodland',
    'Goodland (Out)': 'goodland',
    'Goodland (Pipe)': 'goodland',
    'IM Turn #1': 'im',
    'Frost Woods': 'forest_woods',
    'Schluter': 'schluter',
    'Law Park Pier': 'law_park',
    'Crystal Lake': 'crystal_lake',
    'Vilas Outfall': 'vilas',
    'Wingra NW': 'wingra_lake',
    'Yahara Heights Dog Park': 'yahara_heights_dog',
    'Memorial Union Terrace': 'memorial_union',
}


def load():
    """
    Load the transformed dataframe.
    """
    df = pd.read_excel(
        DATA_FOLDER / 'raw/PHMDC Beach Data 2010-2018.xlsx'
    )
    df.columns = df.columns.str.lower()
    df['site'] = pd.Series(SITE_MAP)[df['site']].values
    df = df[df['test'].str.contains('E Coli')]
    df['result'] = (
        df['result']
        .str.replace('<', '')  # things like "<10.0"
        .str.replace('>', '')  # things like ">2400"
        .str.replace(',', '')  # things like "12,345"
        .astype(float)
    )
    df = (
        df
        .sort_values(by=['collectdate', 'site'])
        .groupby(['collectdate', 'site'])
        .apply(lambda x: x['result'].mean()) # gmean(x['result'].dropna()))
        .reset_index()
        .pivot(index='collectdate', columns='site', values=0)
    )
    return df
