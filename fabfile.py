# -*- coding: UTF-8 -*-
import os
from fabric.api import env
from deployment.settings import s
from deployment.dependencies import (install_dependcies, update_system,
                 export_environment_variables, )
from deployment.git import (pull)
from deployment.gunicorn_server import (restart_server)
from deployment.db import (syncdb, migrate)
from deployment.shortcuts import (deploy, jenkins)
from deployment.quality import (test, jenkins_test)


def production(user):
    s.set_environment(s.DEPLOYMENT)
    env.hosts = ['kotob.me']
    env.directory = '/var/www/kotob'
    env.activate = 'source /var/venv/kotob/bin/activate'
    env.user = str(user)


def local(virtual_env_path):
    s.set_environment(s.LOCAL, virtual_env=virtual_env_path,
                  settings=os.path.join(s.PROJECT_ROOT, 'kotob/settings.py'))
