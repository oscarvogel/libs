Command line interface (CLI)
============================

After install arcovid19 you also have a command line app to download the
data as csv.

.. code-block:: console

    $ arcovid19 --help
    Usage: arcovid19 [OPTIONS]

    Retrieve and store the database as an as CSV file.

    Options:
    --url=STR    str The url for the excel table to parse. Default is ivco19 team table. (default: https://github.com/ivco19/libs/raw/master/databases/cases.xlsx)
    --out=STR    PATH (default=stdout) The output path to the CSV file. If it's not provided the data is printed in the stdout.
    --nocached   If you want to ignore the local cache or retrieve a new value.

    Other actions:
    -h, --help   Show the help









