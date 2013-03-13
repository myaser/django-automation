from fabric.api import cd, settings

from deployment.git import pull
from deployment.db import migrate, syncdb
from deployment.gunicorn_server import restart_server
from deployment.dependencies import install_dependcies,\
    export_environment_variables
from deployment.quality import test, jenkins_test


def deploy():
    with cd('/var/www/kotob'):
        with settings(warn_only=True):
            export_environment_variables()
            pull()
            install_dependcies()
            migrate()
            restart_server()


def jenkins():
    export_environment_variables()
    install_dependcies()
    syncdb()
    jenkins_test()
