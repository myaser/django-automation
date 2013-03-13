import glob
import os
from fabric.api import execute, sudo
from deployment.fabvenv import virtualenv
from deployment import tasks_runner_factory, DevelopmentMethod, ProductionMethod
from deployment.settings import s


def install_dependcies():
    _install_apt()
    _install_pip()
    _install_npm()
#    _configure_solr()


def update_system():
    runner = tasks_runner_factory.get_fabric_method(super=True)
    runner.execute('apt-get update')
    runner.execute('apt-get upgrade')


def export_environment_variables():
    # TODO: make some file to collect environment variables,
    # it must be set in earlier stage than this
    runner = tasks_runner_factory.get_fabric_method()
    runner.execute('export STATIC_DEPS=true')


def _install_apt():
    # TODO: separate the next lines to be reused
    apt_requirements_regex = os.path.join(s.REQUIREMENTS_ROOT, '*.apt')
    apt_requirement_file_pathes = glob.glob(apt_requirements_regex)

    requirements = []
    for path in apt_requirement_file_pathes:
        with open(path) as apt_file:
            requirements.extend(
                [line.partition('#')[0].rstrip()
                 for line in apt_file.readlines()
                 if line.partition('#')[0].rstrip()
                 ])
    runner = tasks_runner_factory.get_fabric_method(super=True)
    runner.execute('apt-get install ' + " ".join(requirements))


def _install_pip():
    with virtualenv(s.get_virtual_env_path()):
        runner = tasks_runner_factory.get_fabric_method()
        print runner.__class__
        if runner.__class__ == DevelopmentMethod:
            runner.execute('pip install -r requirements/development.pip')
        elif runner.__class__ == ProductionMethod:
            runner.execute('pip install -r requirements/production.pip')


def _install_npm():
    with open(os.path.join(s.REQUIREMENTS_ROOT, 'packages.npm')) as npm_file:
        requirements = [line.partition('#')[0].rstrip()
                        for line in npm_file.readlines()
                        if line.partition('#')[0].rstrip()]
    runner = tasks_runner_factory.get_fabric_method()
    runner.execute('npm install ' + " ".join(requirements))


def _configure_solr():
    # import search engine configuration file
    raise NotImplementedError()
