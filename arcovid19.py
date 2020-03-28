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

"""Parser of COVID-19 data from the IATE task force.

"""


__all__ = ["load_cases"]

__version__ = "2020.03.24"


# =============================================================================
# IMPORTS
# =============================================================================

import os
from datetime import datetime
import logging

import numpy as np

import pandas as pd

import attr

import diskcache as dcache


# =============================================================================
# CONSTANTS
# =============================================================================

ARCOVID19_DATA = os.path.expanduser(os.path.join('~', 'arcovid19_data'))


DEFAULT_CACHE_DIR = os.path.join(ARCOVID19_DATA, "_cache_")


CACHE = dcache.Cache(directory=DEFAULT_CACHE_DIR, disk_min_file_size=0)


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

def from_cache(fname, on_not_found, **kwargs):
    """Simple cache orchestration.

    """
    # start the cache orchestration
    key = dcache.core.args_to_key(
        base=("arcodiv19",), args=(fname,), kwargs=kwargs, typed=False)
    with CACHE as cache:
        cache.expire()

        value = cache.get(key, default=dcache.core.ENOVAL, retry=True)
        if value is dcache.core.ENOVAL:
            value = on_not_found()
            cache.set(
                key, value, expire=CACHE_EXPIRE,
                tag=f"{fname}", retry=True)

    return value


# =============================================================================
# CASES
# =============================================================================

@attr.s(frozen=True, repr=False)
class CasesPlot:

    cstats = attr.ib()

    def __repr__(self):
        return f"CasesPlot({hex(id(self.cstats))})"


@attr.s(frozen=True, repr=False)
class CasesFrame:
    """Wrapper around the `load_cases()` table.

    This class adds functionalities around the dataframe.

    """

    df = attr.ib()
    cplot = attr.ib(init=False)

    @cplot.default
    def _plot_default(self):
        return CasesPlot(cstats=self)

    def __dir__(self):
        return super().__dir__() + dir(self.df)

    def __repr__(self):
        return repr(self.df)

    def __getattr__(self, a):
        """Redirect all te missing calls to the internal datadrame."""
        return getattr(self.df, a)

    @property
    def dates(self):
        """Returns the dates for which we have data.

        Useful to use as time column (row) list for wide (long) format.

        """
        return tuple(
            adate for adate in self.df.columns if isinstance(adate, datetime))

    @property
    def tot_cases(self):
        """Returns latest value of total confirmed cases

        """

        return self.df.loc[('ARG', 'C'), self.dates[-1]]

    def r0(self, provincia=None):
        """Calcula el R0 del pais o el R0 de la provincia si se le provee un nombre.

        """

        # R0 de Arg sí es None
        if provincia is None:
            dfrA = self.df[self.dates].copy()

            df1A = dfrA.reindex([('ARG', 'growth_rate_C')])

            IA_n = df1A.iloc[:, -1]
            IA_n_1 = df1A.iloc[:, -2]
            R0A = IA_n / IA_n_1

            return(R0A)

        # solo de una provincia si se la pasamos
        if provincia not in PROVINCIAS.values():
            # si aca pasaron el nombre de la provincia esto lo cambia
            # por el código
            provincia = PROVINCIAS.get(provincia)
        if provincia is None:
            # si llegamos aca es por que lo que nos pasaron no es ni
            # un nombre ni un código
            raise ValueError(f"Provincia '{provincia}' no es reconocida")

        dfr = self.df.copy()
        dfr = dfr.reset_index(level=['cod_provincia'])

        df1 = dfr.loc['C']
        df1.reset_index(level=['cod_status'])
        df1 = df1.set_index('cod_provincia')

        I_n = df1.iloc[:-2, -1]
        I_n_1 = df1.iloc[:-2, -2]
        R0 = I_n / I_n_1

        return(R0)


def load_cases(*, url=CASES_URL, out=None):
    """Utility function to parse all the actual cases of the COVID-19 in
    Argentina.


    Parameters
    ----------

    url: str
        The url for the excel table to parse. Default is ivco19 team table

    out: str, path to store the dataset or None.
        The dataset was stored as csv file. If its None the dataset was not
        stored.


    Returns
    -------

    df_infar: Pandas.DataFrame object

        A table parsing the Excel file spreadsheet 0 (called BD).
        It features a pandas multi index, with the following hierarchy:
            level 0: cod_provincia - Argentina states
            level 1: cod_status - Four states of disease patients (R, C, A, D)

    """
    df_infar = from_cache(
        fname="load_cases",
        on_not_found=lambda: pd.read_excel(url, sheet_name=0, nrows=96),
        url=url)

    # load table and replace Nan by zeros
    df_infar = df_infar.fillna(0)

    # Parsear provincias en codigos standard
    df_infar.rename(columns={'Provicia \\ día': 'Pcia_status'}, inplace=True)
    for irow, arow in df_infar.iterrows():
        pst = arow['Pcia_status'].split()
        stat = STATUS.get(pst[-1])

        if stat is None:
            logger.info(f"{stat}, {pst[-1]}, stopped 0")
            break

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
        dates = [adate for adate in sums.index if isinstance(adate, datetime)]
        df_infar.loc[('ARG', astatus), dates] = sums[dates].astype(int)

        df_infar.loc[('ARG', astatus), 'provincia_status'] = f"ARG_{astatus}"

    n_c = df_infar.loc[('ARG', 'C'), dates].values
    growth_rate_C = (n_c[1:] / n_c[:-1]) - 1
    df_infar.loc[('ARG', 'growth_rate_C'), dates[1:]] = growth_rate_C

    if out is not None:
        df_infar.to_csv(out)

    return CasesFrame(df=df_infar)


# =============================================================================
# MAIN_
# =============================================================================

if __name__ == '__main__':
    from clize import run
    run(load_cases)
