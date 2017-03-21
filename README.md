## Setup

### Rawdata

Download all the files in `raw_taxi_trip_data_urls.txt` under `./raw_trip_data`

`bash ./download_raw_data.sh`


### Database

PostgreSQL 6.2 and PostGIS 2.3.2.


### Python

Require either [miniconda3] or [Anaconda3], which runs Python 3.6.

Create a new conda virtual environment with name `cse530`:

    conda env create -n cse530 -f conda_environment.yml

[miniconda3]: https://conda.io/miniconda.html
[Anaconda3]: https://www.continuum.io/downloads


### Load data

Once raw data is available, one could run the following commands:

    fab init_db             # init the database
    fab create_table        # create the table
    fab load_taxi_trips     # load taxi trips

To restart, replace `init_db` with `reborn`:

    fab reborn create_table load_taxi_trips



## Misc.

### Notebooks

Some Jupyter notebooks are under `notebooks/` for data exploration.

