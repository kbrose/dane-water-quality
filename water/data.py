from pathlib import Path
import logging

import pandas as pd
from scipy.stats.mstats import gmean

from water.names import SITE_MAP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FOLDER = Path(__file__).parents[1] / 'data'


def load():
    """
    Load the transformed dataframe.
    """
    df = pd.read_excel(
        DATA_FOLDER / 'raw' / 'PHMDC Beach Data 2010-2018.xlsx'
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
        .dropna(subset=['result'])
        .sort_values(by=['collectdate', 'site'])
        .groupby(['collectdate', 'site'])
        .apply(lambda x: gmean(x['result']))
        .reset_index()
        .pivot(index='collectdate', columns='site', values=0)
    )
    return df
