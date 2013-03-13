from functools import partial
from contextlib import contextmanager
import posixpath

from fabric.api import env
from fabric.context_managers import prefix, settings, hide
from deployment import tasks_runner_factory, DevelopmentMethod,\
    DevelopmentSuperMethod

runner = tasks_runner_factory.get_fabric_method()

# Default virtualenv command
env.virtualenv = 'virtualenv'

# URL of the standalone virtualenv.py
VIRTUALENV_PY_URL = \
    'https://raw.github.com/pypa/virtualenv/master/virtualenv.py'


@contextmanager
def virtualenv(path):
#    import pdb; pdb.set_trace()
    """Context manager that performs commands with an active virtualenv, eg:

    path is the path to the virtualenv to apply

    >>> with virtualenv(env):
            execute('python foo')

    It is highly recommended to use an absolute path, as Fabric's with cd()
    feature is always applied BEFORE virtualenv(), regardless of how they are
    nested.

    """
    activate = posixpath.join(path, 'bin/activate')
    if not exists(activate):
        raise OSError("Cannot activate virtualenv %s" % path)
    with prefix('. %s' % activate):
        yield


def _wget(url, out):
    """Helper for downloading a file, without requiring wget/curl etc."""
    cmd = (
        "python -c 'import urllib2,sys; "
        "print urllib2.urlopen(sys.argv[1]).read()' '{url}' >{out}"
    )
    runner(cmd.format(url=url, out=out))


def prepare_virtualenv():
    """Prepare a working virtualenv command.

    The command will be available as env.virtualenv.
    """
    with hide('output', 'running'):
        venv = runner('which virtualenv ; :')
        if venv:
            env.virtualenv = venv
            return

        if not exists('~/virtualenv.py'):
            _wget(VIRTUALENV_PY_URL, '~/virtualenv.py')
            runner('chmod 755 ~/virtualenv.py')
        else:
            mode = int(runner('stat -c %a ~/virtualenv.py'), 8)
            if mode & 0o2:
                raise IOError(
                    "~/virtualenv.py is world-writable. "
                    "Not using for security reasons."
                )
        env.virtualenv = '~/virtualenv.py'


def make_virtualenv(path, dependencies=[], eggs=[], system_site_packages=True):
    """Create or update a virtualenv in path.

    :param path: The path to the virtualenv. This path will be created if it
        does not already exist.
    :param dependencies: a list of paths or URLs to python packages to install.
    :param eggs: a list of paths or URLs to eggs to install. Eggs can be used
        to speed up deployments that require libraries to be compiled.
    :param system_site_packages: If True, the newly-created virtualenv will
        expose the system site package. If False, these will be hidden.

    """
    if not exists(path):
        version = tuple(runner('%s --version' % env.virtualenv).split('.'))
        if version >= (1, 7):
            args = '--system-site-packages' if system_site_packages else ''
        else:
            args = '--no-site-packages' if not system_site_packages else ''
        runner('{virtualenv} {args} {path}'.format(
            virtualenv=env.virtualenv,
            args=args,
            path=path
        ))
    else:
        # Update system-site-packages
        no_global_path = posixpath.join(path,
            'lib/python*/no-global-site-packages.txt'
        )
        if system_site_packages:
            runner('rm -f ' + no_global_path)
        else:
            runner('touch ' + no_global_path)

    with virtualenv(path):
        for e in eggs:
            with settings(warn_only=True):
                runner("easy_install '%s'" % e)
        for d in dependencies:
            runner("pip install '%s'" % d)


def exists(path, use_sudo=False, verbose=False):
    """
    Return True if given path exists on the current remote host.

    If ``use_sudo`` is True, will use `sudo` instead of `run`.

    `exists` will, by default, hide all output (including the run line, stdout,
    stderr and any warning resulting from the file not existing) in order to
    avoid cluttering output. You may specify ``verbose=True`` to change this
    behavior.
    """
    runner = tasks_runner_factory.get_fabric_method(super=use_sudo)
    if runner.__class__ == DevelopmentMethod or runner.__class__ == DevelopmentSuperMethod:
        func = partial(runner.execute, capture=True) #bind capture
        cmd = '[ -f %s ] && echo "Found" || echo "Not found"' % path
    else:
        func = runner.execute
        cmd = 'test -e "$(echo %s)"' % path

    # If verbose, run normally
    if verbose:
        with settings(warn_only=True):
            return not func(cmd).failed
    # Otherwise, be quiet
    with settings(hide('everything'), warn_only=True):
        return not func(cmd).failed
