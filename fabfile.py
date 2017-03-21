from pathlib import Path
from fabric.api import local, task, lcd, env
from fabric.contrib.console import confirm

proj_p = Path(env.real_fabfile).parent


@task
def reborn():
    confirm('Destory and re-create the current database?', False)
    local('dropdb liang-bo.wang_project1')
    local('createdb liang-bo.wang_project1')
