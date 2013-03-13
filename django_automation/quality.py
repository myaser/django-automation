from deployment import tasks_runner_factory
from deployment.fabvenv import virtualenv
from deployment.settings import s


def test():
    with virtualenv(s.get_virtual_env_path()):
        runner = tasks_runner_factory.get_fabric_method()
        runner.execute('python manage.py test')


def jenkins_test():
    with virtualenv(s.get_virtual_env_path()):
        runner = tasks_runner_factory.get_fabric_method()
        runner.execute('python manage.py test')