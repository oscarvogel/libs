.. arcovid-libs documentation master file, created by
   sphinx-quickstart on Sat Mar 28 19:47:44 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Arcovid19
========================================

|Build Status| |Python 3| |BSD-3| |Documentation Status|

.. |Build Status| image:: https://travis-ci.org/ivco19/libs.svg?branch=master
   :target: https://travis-ci.org/ivco19/libs
.. |Python 3| image:: https://img.shields.io/badge/python-3.7+-blue.svg
   :target: https://badge.fury.io/py/arcovid19
.. |BSD-3| image:: https://img.shields.io/badge/License-BSD3-blue.svg
   :target: https://tldrlegal.com/license/bsd-3-clause-license-(revised)
.. |Documentation Status| image:: https://readthedocs.org/projects/arcovid19/badge/?version=latest
   :target: https://arcovid19.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Libs is a package to use the COV-19 data analysis tool. It has a module written in python called arcovid19 dedicated to the
analysis of all real cases of COVID-19 in Argentina.

Arcovid19 is made up of two classes CasesFrame and CasesPlot, these tools are used to report the analysis of COVID-19 data in Argentina
from tables and visualizations. Furthermore, the CasesFrame class inherits and adds functionalities to the DataFrame class of Pandas.

License
-------

arcovid19 is under
`The BSD-3 License <https://github.com/ivco19/libs/blob/master/LICENSE>`__

The BSD 3-clause license allows you almost unlimited freedom with the software so long as you include the BSD copyright and license notice in it (found in Fulltext).

Citation
--------

Please acknowledge arcovid19 in any research report or publication that requires citation of any author's work.
Our suggested acknowledgment is:

    The authors acknowledge the arcovid19 project that contributed to the research reported here. <https://github.com/ivco19/libs/>


**ABOUT THE DATA**


Please cite:

    Luczywo, N. A., Daza, V., Koraj, M., Dominguez, M., Lares, M., Paz, D. J.,
    Quiroga, R., Rios, M. E. D. L., Sánchez, B. O., Stasyszyn, F., &
    Cabral, J. B. (2020). Infecciones de COVID-19 en Argentina.
    Unpublished. https://doi.org/10.13140/RG.2.2.22519.78246


BibText::

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

Raw Data
--------

-  `Viewer <https://docs.google.com/spreadsheets/d/e/2PACX-1vTfinng5SDBH9RSJMHJk28dUlW3VVSuvqaBSGzU-fYRTVLCzOkw1MnY17L2tWsSOppHB96fr21Ykbyv/pub>`__
-  `CSV <https://raw.githubusercontent.com/ivco19/libs/master/databases/cases.csv>`__
-  `XLSX <https://raw.githubusercontent.com/ivco19/libs/master/databases/cases.xlsx>`__


Contact:
--------

For bugs or question please contact

- **Juan B. Cabral:** jbcabral@unc.edu.ar
- **Bruno Sánchez:** bruno.sanchez@duke.edu
- **Vanessa Daza:** vanessa.daza@unc.edu.ar


Contents:
---------

.. toctree::
    :maxdepth: 2

    install/install.rst
    tutorial/tutorial.rst
    api/modules.rst


