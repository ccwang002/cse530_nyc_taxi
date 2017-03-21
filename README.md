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

Check if all the paths in `config.yaml` exist. If not, modify them with the correct paths.

[miniconda3]: https://conda.io/miniconda.html
[Anaconda3]: https://www.continuum.io/downloads


### Notebooks 

Some Jupyter notebooks are under `notebooks/` for data exploration.



### Load data

Once raw data is available, one could init the database and table by::


    createdb liang-bo.wang_project1
    fab reborn create_table

