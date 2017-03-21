from pathlib import Path
from fabric.api import local, task, lcd, env
from fabric.contrib.console import confirm

proj_p = Path(env.real_fabfile).parent

DB_NAME = "liang-bo.wang_project1"

def psql(cmd):
    local(f'psql -d {DB_NAME} {cmd}')

@task
def reborn():
    confirm('Destory and re-create the current database?', False)
    local(f'dropdb {DB_NAME}')
    local(f'createdb {DB_NAME}')
    psql('-c "CREATE EXTENSION postgis;"')
    psql('-c "SELECT PostGIS_full_version();"')


@task
def create_table():
    psql('-f create_trip_table.sql')
