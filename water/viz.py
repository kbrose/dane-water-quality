from datetime import datetime
from typing import Any, Optional, Iterable

from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_exceedances(df: pd.DataFrame, site: str, ax: Axes):
    df_no_nan = df[site].dropna().copy()
    changes = (df_no_nan > 1000).astype(float).diff()
    changes[0] = float(df_no_nan.iloc[0] > 1000)
    changes[-1] = float(changes[-1] or df_no_nan.iloc[-1] > 1000)

    starts = df_no_nan[changes == 1].index.tolist()
    stops = df_no_nan[changes == -1].index.tolist()

    for start, stop in zip(starts, stops):
        if (stop - start).days > 100:
            # Last data points in a Summer were all above. Ignore this case.
            continue
        exceedance = df_no_nan.loc[
            (df_no_nan.index >= start) & (df_no_nan.index <= stop)
        ].copy()
        exceedance.index = (exceedance.index - exceedance.index[0]).days
        ax.plot(
            exceedance.index.values,
            exceedance.values.clip(0, 10_000),
            '.-',
            color=sns.color_palette()[0],
            alpha=0.5
        )
    # ax.set_yscale('log')
    ax.set_ylabel(' '.join(site.split('_')).title(), rotation=0)
    ax.yaxis.set_label_position("right")


def _filter_year(df: pd.DataFrame, yr: int) -> pd.Series:
    return (df.index >= str(yr)) & (df.index < str(yr + 1))


def plot_year(
    df: pd.DataFrame,
    yr: int,
    site: str,
    ax: Optional[Axes]=None,
    xlim: Optional[Iterable[Any]]=None,
    ylim: Optional[Iterable[Any]]=None
):
    x = df.loc[_filter_year(df, yr), site].dropna()
    x_interpolated = x.resample('D').mean().interpolate()
    if ax is None:
        _, ax = plt.subplots(1)
    ax.set_yscale('log')
    if not x.size:
        return
    ax.plot([x.index[0], x.index[-1]], [1000, 1000], 'k--', alpha=0.3)
    line = ax.plot(x_interpolated.index, x_interpolated.values, '-')[0]
    ax.plot(x.index, x.values, 'o', color=line.get_color())
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)


def plot_all_years_site(df: pd.DataFrame, site: str):
    years = list(range(2010, 2019))
    f, axs = plt.subplots(len(years), sharey=True, figsize=(14, 14))
    axs[0].set_title(' '.join(site.split('_')).title())
    for ax, yr in zip(axs, years):
        plot_year(df, yr, site, ax,
                  xlim=[datetime(yr, 5, 20), datetime(yr, 9, 10)],
                  ylim=[1, 10**5])
        ax.set_yticks([10, 10**4])
        ax.set_ylabel(yr)
