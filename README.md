## Setup


### System requirement

Requires PostgreSQL 6.2 and PostGIS 2.3.2.


### Python

Require either [miniconda3] or [Anaconda3], which runs Python 3.6.

Create a new conda virtual environment with name `cse530`:

    conda env create -n cse530 -f conda_environment.yml

[miniconda3]: https://conda.io/miniconda.html
[Anaconda3]: https://www.continuum.io/downloads


### Construct the Database

One could run the following commands to construct the database named `liang-bo.wang_project1`:

    fab download_raw_data   # download raw data 
    fab init_db             # init the database
    fab create_table        # create the table
    fab load_taxi_trips     # load taxi trip data
    fab load_zones          # load zones shape data
    fab load_weather        # load weather data

which can be specified by one liner:

    fab download_raw_data init_db ... load_weather

To restart the database, replace `init_db` with `reborn`.


## Analysis

All analysis scripts to generate figures in the report are under `analysis/`.


## Misc.

### Notebooks

Some Jupyter notebooks are under `notebooks/` for data exploration.

