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

__version__ = "2020.03.22"


# =============================================================================
# IMPORTS
# =============================================================================

import os
from datetime import datetime

import numpy as np

import pandas as pd

import diskcache as dcache


# =============================================================================
# CONSTANTS
# =============================================================================

ARCOVID19_DATA = os.path.expanduser(os.path.join('~', 'arcovid19_data'))


DEFAULT_CACHE_DIR = os.path.join(ARCOVID19_DATA, "_cache_")


CACHE = dcache.Cache(directory=DEFAULT_CACHE_DIR, disk_min_file_size=0)


CACHE_EXPIRE = 60 * 60  # ONE HOUR


TABLA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTfinng5SDBH9RSJMHJk28dUlW3VVSuvqaBSGzU-fYRTVLCzOkw1MnY17L2tWsSOppHB96fr21Ykbyv/pub?output=xls"  # noqa


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


def load_cases(*, url=TABLA_URL, orientation='wide', out=None):
    """Utility function to parse all the actual cases of the COVID-19 in
    Argentina.


    Parameters
    ----------

    url: str
        The url for the excel table to parse. Default is ivco19 team table

    orientation: str, 'wide' or 'long'
        The format of the table. If wide, dates are going to be columns.
        If in turn, long, dates are going to be rows, regions are going to
        be columns. Under the hood is callin df.transpose() method from Pandas.

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
        url=TABLA_URL, orientation='wide', out=None)

    # load table and replace Nan by zeros
    df_infar = df_infar.fillna(0)

    # Parsear provincias en codigos standard
    df_infar.rename(columns={'Provicia \\ día': 'Pcia_status'}, inplace=True)

    for irow, arow in df_infar.iterrows():
        pst = arow['Pcia_status'].split()

        stat = STATUS.get(pst[-1])

        if stat is None:
            print(stat, pst[-1], 'stopped 0')
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

    index = pd.MultiIndex.from_frame(
        df_infar[['cod_provincia', 'cod_status']])

    df_infar.index = index

    df_infar.drop(columns=['cod_status', 'cod_provincia'], inplace=True)

    cols = list(df_infar.columns)

    df_infar = df_infar[[cols[-1]] + cols[:-1]]

    for astatus in np.unique(df_infar.index.get_level_values(1)):
        filter_confirmados = df_infar.index.get_level_values(
            'cod_status').isin([astatus])
        sums = df_infar[filter_confirmados].sum(axis=0)
        dates = [adate for adate in sums.index if isinstance(adate, datetime)]
        sums = sums[dates].astype(int)

        for date, suma in sums.iteritems():
            df_infar.loc[('ARG', astatus), date] = suma
        df_infar.loc[('ARG', astatus), 'provincia_status'] = f'ARG_{astatus}'

    if orientation == 'long':
        df_infar = df_infar.transpose()
    elif orientation != 'wide':
        raise ValueError("'orientation must be 'wide' or 'long'")

    if out is not None:
        df_infar.to_csv(out)
    return df_infar


# =============================================================================
# MAIN_
# =============================================================================

if __name__ == '__main__':
    from clize import run
    run(load_cases)
