from fabric.api import settings, cd
from deployment.fabvenv import virtualenv


from deployment import tasks_runner_factory
from deployment.settings import s


def migrate():
    with settings(warn_only=True):
        with virtualenv(s.get_virtual_env_path()):
            with cd('/var/www/kotob'):
                runner = tasks_runner_factory.get_fabric_method()
                runner.execute('python manage.py schemamigrateall')
                runner.execute('python manage.py migrate')


def syncdb():
    with settings(warn_only=True):
        with virtualenv(s.get_virtual_env_path()):
            with cd('/var/www/kotob'):
                runner = tasks_runner_factory.get_fabric_method()
                runner.execute('python manage.py syncdb')
