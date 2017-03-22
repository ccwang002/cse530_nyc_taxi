from pathlib import Path
from fabric.api import local, task, lcd, env
from fabric.contrib.console import confirm

proj_p = Path(env.real_fabfile).parent

DB_NAME = "liang-bo.wang_project1"

def psql(cmd):
    local(f'psql -d {DB_NAME} {cmd}')


@task
def init_db():
    local(f'createdb {DB_NAME}')
    psql('-c "CREATE EXTENSION postgis;"')
    psql('-c "SELECT PostGIS_full_version();"')


@task
def load_zones():
    local(f'bash load_zones.sh')


@task
def reborn():
    confirm('Destory and re-create the current database?', False)
    local(f'dropdb {DB_NAME}')
    init_db()


@task
def create_table():
    psql('-f create_trip_table.sql')
    psql('-f create_weather_table.sql')


@task
def load_taxi_trips():
    local(
        f'python load_yellow_taxi_trips.py --db-name {DB_NAME} '
        'raw_trip_data/yellow_tripdata_2016-06.csv'
    )
    psql('-f update_taxi_trip_with_geom.sql')


@task
def load_weather():
    local(
        f'python load_weather.py --db-name {DB_NAME} '
        'raw_weather_data/ny_weather_2015-2016.csv'
    )
