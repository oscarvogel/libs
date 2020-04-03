#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Mauricio Koraj, Vanessa Daza,
#                     Juan B Cabral, Mariano Dominguez, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Utilities to access different Argentina-Related databases of
COVID-19 data from the IATE task force.

"""

__all__ = [
    "DEFAULT_CACHE_DIR",
    "CACHE",
    "CACHE_EXPIRE",
    "CODE_TO_POVINCIA",
    "CasesPlot",
    "CasesFrame",
    "load_cases"]

__version__ = "0.4.1"


# =============================================================================
# IMPORTS
# =============================================================================

import os
import sys
import datetime as dt
import itertools as it

import logging

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import unicodedata

import attr

import diskcache as dcache


# =============================================================================
# CONSTANTS
# =============================================================================

ARCOVID19_DATA = os.path.expanduser(os.path.join('~', 'arcovid19_data'))

#: Default cache location, (default=~/arcovid_19_data/_cache_)
DEFAULT_CACHE_DIR = os.path.join(ARCOVID19_DATA, "_cache_")

#: Default cache instance
CACHE = dcache.Cache(directory=DEFAULT_CACHE_DIR, disk_min_file_size=0)

#: Time to expire of every load_cases call in seconds
CACHE_EXPIRE = 60 * 60  # ONE HOUR


CASES_URL = "https://github.com/ivco19/libs/raw/master/databases/cases.xlsx"


PROVINCIAS = {
    'CABA': 'CABA',
    'Bs As': 'BA',
    'Córdoba': 'CBA',
    'San Luis': 'SL',
    'Chaco': 'CHA',
    'Río Negro': 'RN',
    'Santa Fe': 'SF',
    'Tierra del F': 'TF',
    'Jujuy': 'JY',
    'Salta': 'SAL',
    'Entre Ríos': 'ER',
    'Corrientes': 'COR',
    'Santiago Est': 'SDE',
    'Neuquen': 'NQ',
    'Mendoza': 'MDZ',
    'Tucumán': 'TUC',
    'Santa Cruz': 'SC',
    'Chubut': 'CHU',
    'Misiones': 'MIS',
    'Formosa': 'FOR',
    'Catamarca': 'CAT',
    'La Rioja': 'LAR',
    'San Juan': 'SJU',
    'La Pampa': 'LPA'}


# this alias fixes the original typos
PROVINCIAS_ALIAS = {
    'Tierra del Fuego': "TF",
    'Neuquén': "NQ",
    "Santiago del Estero": "SDE"
}

#: List of Argentina provinces
CODE_TO_POVINCIA = {
    v: k for k, v in it.chain(PROVINCIAS.items(), PROVINCIAS_ALIAS.items())}

STATUS = {
    'Recuperado': 'R',
    'Recuperados': 'R',
    'Confirmados': 'C',
    'Confirmado': 'C',
    'Activos': 'A',
    'Muertos': 'D'}


logger = logging.getLogger("arcovid19")


# =============================================================================
# FUNCTIONS_
# =============================================================================

def from_cache(fname, on_not_found, cached=True, **kwargs):
    """Simple cache orchestration.

    """
    # start the cache orchestration
    key = dcache.core.args_to_key(
        base=("arcodiv19",), args=(fname,), kwargs=kwargs, typed=False)
    with CACHE as cache:
        cache.expire()

        value = (
            cache.get(key, default=dcache.core.ENOVAL, retry=True)
            if cached else dcache.core.ENOVAL)

        if value is dcache.core.ENOVAL:
            value = on_not_found()
            cache.set(
                key, value, expire=CACHE_EXPIRE,
                tag=f"{fname}", retry=True)

    return value


def safe_log(array):
    """Convert all -inf to 0"""
    with np.errstate(divide='ignore'):
        res = np.log(array.astype(float))
    res[np.isneginf(res)] = 0
    return res


# =============================================================================
# CASES
# =============================================================================

@attr.s(frozen=True, repr=False)
class CasesPlot:

    cstats = attr.ib()

    def __repr__(self):
        return f"CasesPlot({hex(id(self.cstats))})"

    def __call__(self, plot_name=None, ax=None, **kwargs):
        """x.__call__() == x()"""
        plot_name = plot_name or ""

        if plot_name.startswith("_"):
            raise ValueError(f"Invalid plot_name '{plot_name}'")

        plot = getattr(self, plot_name, self.grate_full_period_all)
        ax = plot(ax=ax, **kwargs)
        return ax

    def _plot_df(
        self, *, odf, prov_name, prov_code,
        confirmed, active, recovered, deceased
    ):
        columns = {}
        if confirmed:
            cseries = odf.loc[(prov_code, 'C')][self.cstats.dates].values
            columns[f"{prov_name} Confirmed"] = cseries
        if active:
            cseries = odf.loc[(prov_code, 'A')][self.cstats.dates].values
            columns[f"{prov_name} Active"] = cseries
        if recovered:
            cseries = odf.loc[(prov_code, 'R')][self.cstats.dates].values
            columns[f"{prov_name} Recovered"] = cseries
        if deceased:
            cseries = odf.loc[(prov_code, 'D')][self.cstats.dates].values
            columns[f"{prov_name} Deceased"] = cseries
        pdf = pd.DataFrame(columns)
        return pdf

    def grate_full_period_all(
        self, ax=None, argentina=True,
        exclude=None, **kwargs
    ):

        kwargs.setdefault("confirmed", True)
        kwargs.setdefault("active", False)
        kwargs.setdefault("recovered", False)
        kwargs.setdefault("deceased", False)

        exclude = [] if exclude is None else exclude

        if ax is None:
            ax = plt.gca()
            fig = plt.gcf()

            height = len(PROVINCIAS) - len(exclude) - int(argentina)
            height = 4 if height <= 0 else (height)

            fig.set_size_inches(12, height)

        if argentina:
            self.grate_full_period(provincia=None, ax=ax, **kwargs)

        exclude = [] if exclude is None else exclude
        exclude = [self.cstats.get_provincia_name_code(e)[1] for e in exclude]

        for code in sorted(CODE_TO_POVINCIA):
            if code in exclude:
                continue
            self.grate_full_period(provincia=code, ax=ax, **kwargs)

        labels = [d.date() for d in self.cstats.dates]
        ticks = np.arange(len(labels))

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, rotation=45)

        ax.set_title(
            "COVID-19 Grow in Argentina by Province\n"
            f"{labels[0]} - {labels[-1]}")
        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        return ax

    def grate_full_period(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, log=False, **kwargs
    ):
        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.cstats.get_provincia_name_code(provincia)

        ax = plt.gca() if ax is None else ax

        pdf = self._plot_df(
            odf=self.cstats.df, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased)
        pdf.plot.line(ax=ax, **kwargs)

        labels = [d.date() for d in self.cstats.dates]
        ticks = np.arange(len(labels))

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, rotation=45)

        ax.set_title(
            f"COVID-19 Grow in {prov_name}\n"
            f"{labels[0]} - {labels[-1]}")
        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        ax.legend()

        return ax

    def time_serie_all(
        self, ax=None, argentina=True,
        exclude=None, **kwargs
    ):
        kwargs.setdefault("confirmed", True)
        kwargs.setdefault("active", False)
        kwargs.setdefault("recovered", False)
        kwargs.setdefault("deceased", False)

        exclude = [] if exclude is None else exclude

        if ax is None:
            ax = plt.gca()
            fig = plt.gcf()

            height = len(PROVINCIAS) - len(exclude) - int(argentina)
            height = 4 if height <= 0 else (height)

            fig.set_size_inches(12, height)

        if argentina:
            self.time_serie(provincia=None, ax=ax, **kwargs)

        exclude = [] if exclude is None else exclude
        exclude = [self.cstats.get_provincia_name_code(e)[1] for e in exclude]

        for code in sorted(CODE_TO_POVINCIA):
            if code in exclude:
                continue
            self.time_serie(provincia=code, ax=ax, **kwargs)

        labels = [d.date() for d in self.cstats.dates]
        ticks = np.arange(len(labels))

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, rotation=45)

        ax.set_title(
            "COVID-19 cases by date in Argentina by Province\n"
            f"{labels[0]} - {labels[-1]}")
        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        return ax

    def time_serie(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, **kwargs
    ):
        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.cstats.get_provincia_name_code(provincia)

        ax = plt.gca() if ax is None else ax

        ts = self.cstats.restore_time_serie()
        pdf = self._plot_df(
            odf=ts, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased)
        pdf.plot.line(ax=ax, **kwargs)

        labels = [d.date() for d in self.cstats.dates]
        ticks = np.arange(len(labels))

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, rotation=45)

        ax.set_title(
            f"COVID-19 cases by date in {prov_name}\n"
            f"{labels[0]} - {labels[-1]}")
        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        ax.legend()

        return ax

    def barplot(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, **kwargs
    ):
        ax = plt.gca() if ax is None else ax

        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.cstats.get_provincia_name_code(provincia)

        ts = self.cstats.restore_time_serie()
        pdf = self._plot_df(
            odf=ts, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased)

        pdf.plot.bar(ax=ax, **kwargs)

        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        labels = [d.date() for d in self.cstats.dates]
        ax.set_xticklabels(labels, rotation=45)
        ax.legend()

        return ax

    def boxplot(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, **kwargs
    ):
        ax = plt.gca() if ax is None else ax

        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.cstats.get_provincia_name_code(provincia)

        ts = self.cstats.restore_time_serie()
        pdf = self._plot_df(
            odf=ts, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased)
        pdf.plot.box(ax=ax, **kwargs)

        ax.set_ylabel("N")

        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

        return ax


@attr.s(frozen=True, repr=False)
class CasesFrame:
    """Wrapper around the `load_cases()` table.

    This class adds functionalities around the dataframe.

    """

    df = attr.ib()
    plot = attr.ib(init=False)

    @plot.default
    def _plot_default(self):
        return CasesPlot(cstats=self)

    def __dir__(self):
        """x.__dir__() <==> dir(x)"""
        return super().__dir__() + dir(self.df)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return repr(self.df)

    def __getattr__(self, a):
        """x.__getattr__(y) <==> x.y

        Redirect all te missing calls to the internal datadrame.

        """
        return getattr(self.df, a)

    def __getitem__(self, k):
        """x.__getitem__(y) <==> x[y]"""
        return self.df.__getitem__(k)

    @property
    def dates(self):
        """Returns the dates for which we have data.

        Useful to use as time column (row) list for wide (long) format.

        """
        return [
            adate for adate in self.df.columns
            if isinstance(adate, dt.datetime)]

    @property
    def tot_cases(self):
        """Returns latest value of total confirmed cases"""
        return self.df.loc[('ARG', 'C'), self.dates[-1]]

    def get_provincia_name_code(self, provincia):
        """Resolve and validate the name and code of a given provincia
        name or code.

        """
        def norm(text):
            text = text.lower()
            text = unicodedata.normalize('NFD', text)\
                .encode('ascii', 'ignore')\
                .decode("utf-8")
            return str(text)
        prov_norm = norm(provincia)
        for name, code in PROVINCIAS.items():
            if norm(name) == prov_norm or norm(code) == prov_norm:
                return CODE_TO_POVINCIA[code], code

        for alias, code in PROVINCIAS_ALIAS.items():
            if prov_norm == norm(alias):
                return CODE_TO_POVINCIA[code], code

        raise ValueError(f"Unknown provincia'{provincia}'")

    def restore_time_serie(self):
        """Retrieve a new pandas.DataFrame but with observations
        by Date.
        """
        def _cumdiff(row):
            shifted = np.roll(row, 1)
            shifted[0] = 0
            diff = row - shifted
            return diff

        idxs = ~self.df.index.isin([('ARG', 'growth_rate_C')])
        cols = self.dates

        uncum = self.df.copy()
        uncum.loc[idxs, cols] = uncum.loc[idxs][cols].apply(_cumdiff, axis=1)
        return uncum

    def last_growth_rate(self, provincia=None):
        """Returns the last available growth rate for the whole country
        if provincia is None, or for only the named region.

        """
        return self.grate_full_period(provincia=provincia)[self.dates[-1]]

    def grate_full_period(self, provincia=None):
        """Estimates growth rate for the period where we have data

        """
        # R0 de Arg sí es None
        if provincia is None:
            idx_region = ('ARG', 'growth_rate_C')
            return(self.df.loc[idx_region, self.dates[1:]])

        pcia_code = self.get_provincia_name_code(provincia)[1]

        idx_region = (pcia_code, 'C')

        I_n = self.df.loc[idx_region, self.dates[1:]].values.astype(float)
        I_n_1 = self.df.loc[idx_region, self.dates[:-1]].values.astype(float)

        growth_rate = np.array((I_n / I_n_1) - 1)
        growth_rate[np.where(np.isinf(growth_rate))] = np.nan

        return pd.Series(index=self.dates[1:], data=growth_rate)


def load_cases(url=CASES_URL, cached=True):
    """Utility function to parse all the actual cases of the COVID-19 in
    Argentina.


    Parameters
    ----------

    url: str
        The url for the excel table to parse. Default is ivco19 team table.

    cached : bool
        If you want to use the local cache or retrieve a new value.

    Returns
    -------

    CasesFrame: Pandas-DataFrame like object with all the arcovid19 datatabase.

        It features a pandas multi index, with the following hierarchy:

        - level 0: cod_provincia - Argentina states
        - level 1: cod_status - Four states of disease patients (R, C, A, D)

    """
    df_infar = from_cache(
        fname="load_cases",
        on_not_found=lambda: pd.read_excel(url, sheet_name=0, nrows=96),
        cached=cached,
        url=url)

    # load table and replace Nan by zeros
    df_infar = df_infar.fillna(0)

    # Parsear provincias en codigos standard
    df_infar.rename(columns={'Provicia \\ día': 'Pcia_status'}, inplace=True)
    for irow, arow in df_infar.iterrows():
        pst = arow['Pcia_status'].split()
        stat = STATUS.get(pst[-1])

        pcia = pst[:-2]
        if len(pcia) > 1:
            provincia = ''
            for ap in pcia:
                provincia += ap + ' '
            provincia = provincia.strip()

        else:
            provincia = pcia[0].strip()

        provincia_code = PROVINCIAS.get(provincia)

        df_infar.loc[irow, 'cod_provincia'] = provincia_code
        df_infar.loc[irow, 'cod_status'] = stat
        df_infar.loc[irow, 'provincia_status'] = f"{provincia_code}_{stat}"

    # reindex table with multi-index
    index = pd.MultiIndex.from_frame(df_infar[['cod_provincia', 'cod_status']])
    df_infar.index = index

    # drop duplicate columns
    df_infar.drop(columns=['cod_status', 'cod_provincia'], inplace=True)
    cols = list(df_infar.columns)
    df_infar = df_infar[[cols[-1]] + cols[:-1]]

    # calculate the total number per categorie per state, and the global
    for astatus in np.unique(df_infar.index.get_level_values(1)):
        filter_confirmados = df_infar.index.get_level_values(
            'cod_status').isin([astatus])
        sums = df_infar[filter_confirmados].sum(axis=0)
        dates = [date for date in sums.index if isinstance(date, dt.datetime)]
        df_infar.loc[('ARG', astatus), dates] = sums[dates].astype(int)

        df_infar.loc[('ARG', astatus), 'provincia_status'] = f"ARG_{astatus}"

    n_c = df_infar.loc[('ARG', 'C'), dates].values
    growth_rate_C = (n_c[1:] / n_c[:-1]) - 1
    df_infar.loc[('ARG', 'growth_rate_C'), dates[1:]] = growth_rate_C

    return CasesFrame(df=df_infar)


# =============================================================================
# MAIN_
# =============================================================================

def main():
    from clize import run

    def _load_cases(*, url=CASES_URL, nocached=False, out=None):
        """Retrieve and store the database as an as CSV file.

        url: str
            The url for the excel table to parse. Default is ivco19 team table.

        out: PATH (default=stdout)
            The output path to the CSV file. If it's not provided the
            data is printed in the stdout.

        nocached:
            If you want to ignore the local cache or retrieve a new value.

        """
        cases = load_cases(url=url, cached=not nocached)
        if out is not None:
            cases.to_csv(out)
        else:
            cases.to_csv(sys.stdout)
    run(_load_cases)


if __name__ == '__main__':
    main()
