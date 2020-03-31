# ivco19 Libraries repo

[![Build Status](https://travis-ci.org/ivco19/libs.svg?branch=master)](https://travis-ci.org/ivco19/libs)
[![Python 3](https://img.shields.io/badge/python-3.7+-blue.svg)](https://badge.fury.io/py/arcovid19)
[![BSD-3](https://img.shields.io/badge/License-BSD3-blue.svg)](https://tldrlegal.com/license/bsd-3-clause-license-(revised))


This libraries contains the utilities to access different databases
of COVID-19 data from the IATE task force.

## Installation

```bash
$ pip install arcovid19
```

## Authors

- Dr. Juan B Cabral (CIFASIS-UNR, IATE-OAC-UNC).
- Sr. Mauricio Koraj (Liricus SRL.).
- Lic. Vanessa Daza (IATE-OAC-UNC, FaMAF-UNC).
- Dr. Mariano Dominguez (IATE-OAC-UNC, FaMAF-UNC).
- Dr. Marcelo Lares (IATE-OAC-UNC, FaMAF-UNC).
- Mgt. Nadia Luczywo (LIMI-FCEFyN-UNC, IED-FCE-UNC, FCA-IUA-UNDEF)
- Dr. Dante Paz (IATE-OAC-UNC, FaMAF-UNC).
- Dr. Rodrigo Quiroga (INFIQC-CFQ, FCQ-UNC).
- Dr. Martín de los Ríos (ICTP-SAIFR).
- Dr. Bruno Sanchez (Department of Physics, Duke University).
- Dr. Federico Stasyszyn (IATE-OAC, FaMAF-UNC).

## Functionalities

### `def load_cases(*, url=TABLA_URL, orientation='wide', out=None)`

Utility function to parse all the actual cases of the COVID-19 in
Argentina.

**Raw Data**

- [Viewer](https://docs.google.com/spreadsheets/d/e/2PACX-1vTfinng5SDBH9RSJMHJk28dUlW3VVSuvqaBSGzU-fYRTVLCzOkw1MnY17L2tWsSOppHB96fr21Ykbyv/pub)
- [CSV](https://docs.google.com/spreadsheets/d/e/2PACX-1vTfinng5SDBH9RSJMHJk28dUlW3VVSuvqaBSGzU-fYRTVLCzOkw1MnY17L2tWsSOppHB96fr21Ykbyv/pub?output=csv)
- [XLSX](https://docs.google.com/spreadsheets/d/e/2PACX-1vTfinng5SDBH9RSJMHJk28dUlW3VVSuvqaBSGzU-fYRTVLCzOkw1MnY17L2tWsSOppHB96fr21Ykbyv/pub?output=xlsx)


#### Parameters

url: str
    The url for the excel table to parse. Default is ivco19 team table

orientation: str, 'wide' or 'long'
    The format of the table. If wide, dates are going to be columns.
    If in turn, long, dates are going to be rows, regions are going to
    be columns. Under the hood is callin df.transpose() method from Pandas.

out: str, path to store the dataset or None.
    The dataset was stored as csv file. If its None the dataset was not
    stored.


#### Returns

df_infar: Pandas.DataFrame object

    A table parsing the Excel file spreadsheet 0 (called BD).
    It features a pandas multi index, with the following hierarchy:
        level 0: cod_provincia - Argentina states
        level 1: cod_status - Four states of disease patients (R, C, A, D)

### Notes

All by default all the values are cached for 1hr. Tho change the time
set the variable `arcovid19.CACHE_EXPIRE` to your desired time in seconds.

To clear all the cache run `arcovid19.CACHE.clear()`


## Citation

Please acknowledge arcovid19 in any research report or publication that requires citation of any author's work.
Our suggested acknowledgment is:

> The authors acknowledge the arcovid19 project that contributed to the research reported here. https://github.com/ivco19/libs/


### ABOUT THE DATA


Please cite:

> Luczywo, N. A., Daza, V., Koraj, M., Dominguez, M., Lares, M., Paz, D. J.,
> Quiroga, R., Rios, M. E. D. L., Sánchez, B. O., Stasyszyn, F., &
> Cabral, J. B. (2020). Infecciones de COVID-19 en Argentina.
> Unpublished. https://doi.org/10.13140/RG.2.2.22519.78246


```
    @misc{https://doi.org/10.13140/rg.2.2.22519.78246,
        doi = {10.13140/RG.2.2.22519.78246},
        url = {http://rgdoi.net/10.13140/RG.2.2.22519.78246},
        author = {
            Luczywo,  Nadia Ayelen and Daza,  Vanessa and Koraj,  Mauricio and
            Dominguez,  Mariano and Lares,  Marcelo and Paz,  Dante Javier and
            Quiroga,  Rodrigo and Rios,  Martín Emilio De Los and
            Sánchez,  Bruno Orlando and Stasyszyn,  Federico and
            Cabral,  Juan Bautista},
        language = {es},
        title = {Infecciones de COVID-19 en Argentina},
        publisher = {Unpublished},
        year = {2020}
    }
```



**Afiliations:**

- [Centro Franco Argentino de Ciencias de la Información y de Sistemas (CIFASIS-UNR)](https://www.cifasis-conicet.gov.ar/)
- [Instituto de Astronomía Téorico y Experimental (IATE-OAC-UNC)](http://iate.oac.uncor.edu/)
- [Facultad de Matemática Física y Computación (FaMAF-UNC)](https://www.famaf.unc.edu.ar/)
- [Laboratorio de Ingeniería y Mantenimiento Industrial (LIMI-FCEFyN-UNC)](https://fcefyn.unc.edu.ar/facultad/secretarias/investigacion-y-posgrado/-investigacion/laboratorio-de-ingenieria-y-mantenimiento-industrial/)
- [Instituto De Estadística Y Demografía - Facultad de Ciencias Económicas (IED-FCE-UNC)](http://www.eco.unc.edu.ar/instituto-de-estadistica-y-demografia)
- [Department of Physics, Duke University](https://phy.duke.edu/)
- [Facultad de Ciencias de la Administación (FCA-IUA-UNDEF)](https://www.iua.edu.ar/)
- [Instituto de Investigaciones en Físico-Química de Córdoba (INFIQC-CONICET)](http://infiqc-fcq.psi.unc.edu.ar/)
- [Liricus SRL](http://www.liricus.com.ar/)
- [ICTP South American Institute for Fundamental Research (ICTP-SAIFR)](ICTP-SAIFR)
