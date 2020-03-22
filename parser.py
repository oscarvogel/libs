#!/usr/bin/env python3.7 
"""Parser of data tables"""

import os
import numpy as np 
import pandas as pd 

from provincias import provincias as pcias
from provincias import status

DATA = './data'
infar = 'datos_infectologia_argentina.xlsx'

taburl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTfinng5SDBH9RSJMHJk28dUlW3VVSuvqaBSGzU-fYRTVLCzOkw1MnY17L2tWsSOppHB96fr21Ykbyv/pub?output=xls"


def parse_urltable(taburl=taburl, tabshape='wide'):
    #load table and replace Nan by zeros
    df_infar = pd.read_excel(taburl, sheet_name=0, nrows=96).fillna(0)
    #df_infar_t = pd.read_excel(os.path.join(DATA, infar), sheet_name=1)

    # Parsear provincias en codigos standard
    df_infar.rename(columns={'Provicia \\ día': 'Pcia_status'}, inplace=True)

    for irow, arow in df_infar.iterrows():
        pst = arow['Pcia_status'].split()
        stat = status.get(pst[-1])
        if stat is None:
            print(stat, pst[-1], 'stopped 0')
            break
        pcia = pst[:-2]
        if len(pcia)>1:
            provincia = ''
            for ap in pcia:
                provincia += ap + ' '
            provincia = provincia.strip()
        else:
            provincia = pcia[0].strip()
        p_code = pcias.get(provincia)

        df_infar.loc[arow.name, 'cod_provincia'] = p_code
        df_infar.loc[arow.name, 'cod_status'] = stat
        df_infar.loc[arow.name, 'provincia_status'] = p_code+'_'+stat

    index = pd.MultiIndex.from_frame(df_infar[['cod_provincia', 'cod_status']])
    df_infar.index = index
    df_infar.drop(columns=['cod_status', 'cod_provincia'], inplace=True)
    cols = list(df_infar.columns)
    df_infar = df_infar[[cols[-1]]+cols[:-1]]

    wide = df_infar
    long = df_infar.transpose()

    if tabshape=='wide':
        return(wide)
    elif tabshape=='long':
        return(long)
    else:
        print('returning wide and long table')
        return(wide, long)

if __name__=='__main__':
    print(parse_urltable())