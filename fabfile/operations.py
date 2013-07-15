# -*- coding: utf-8 -*-

import os

from fabric.api import cd, env, hide, local, settings, task
from fabric.colors import blue, green, white, yellow
from fabric.utils import indent, puts

from .commands import git, nginx, pip, supervisor
from .utils import error, log_call, run, sudo, warning


__all__ = [
    'check_requirements', 'check_nginx', 'install_requirements', 'pull',
    'restart_celery', 'restart_django', 'restart_memcached', 'reload_nginx',
    'restart', 'tailgun', 'timestamp',
]


@task
def check_requirements(hide=False):
    """ This checks if the installed packages are different from those in the
    requirements.txt file.
    """
    command = "diff requirements.txt <(%s)" % pip("freeze", execute=False)

    with cd(env.app):
        out = run(command, quiet=True, show=False).strip()

        if hide:
            return out

        if out:
            diff = indent(out.splitlines(), strip=True)
            warning(["Installed packages are different from the "
                     "requirements.txt file:"] + diff)


@task
@log_call
def install_requirements():
    """ Installs the requirements from the requirements.txt file. This will run
    as the deploy user if on dev.
    """
    with cd(env.app):
        pip("install -r requirements.txt")


@task
@log_call
def pull():
    """ Git pulls on the remote host. """
    git("pull")


@task
@log_call
def restart_celery():
    """ Restarts the Celery Supervisor process. """
    supervisor("restart celery")


@task
@log_call
def restart_django():
    """ Restarts the Django Supervisor process. """
    supervisor("restart %(process)s" % env)


@task
@log_call
def restart_memcached():
    """ Restarts the Memcached server. """
    sudo("service memcached restart")


@task
@log_call
def reload_nginx():
    """ Restarts the nginx process. """
    check_nginx(log=False)
    nginx("reload")


@task
@log_call
def check_nginx():
    """ Checks the Nginx config. """
    with settings(hide('warnings', 'running', 'stdout', 'stderr')):
        result = sudo("service nginx configtest", quiet=True, show=False)

        if result.failed:
            error("Aborting! Nginx failed the configuration test!\n%s" %
                  result)


@task
@log_call
def restart_tomcat():
    """ Restarts the nginx process. """
    sudo("service tomcat6 restart")


@task(alias='re')
@log_call
def restart(*services):
    """ Restarts the given service. """
    options = {
        'celery': restart_celery,
        'django': restart_django,
        'memcached': restart_memcached,
        'nginx': reload_nginx,
        'tomcat': restart_tomcat,
    }

    funcs = []

    for service in services:
        func = options.get(service.lower())
        if not func:
            raise Exception("Unrecognized service %s", service)
        funcs.append(func)

    for func in funcs:
        func(log=False)


@task
@log_call
def rsync(remote_path, local_path, options="-avzr --progress"):
    """ Runs rsync with the remote path as the source, and the local path
    as the destination.
    """
    local("rsync %s %s:%s %s" % (
        options,
        env.host_string,
        remote_path,
        local_path,
    ))


@task
@log_call
def timestamp(_format='%Y-%m-%d %H:%M:%S', quiet=False):
    border = yellow
    sep = ' ⌚ '
    char = '•'
    side = border(char)

    stamp = run('date +"%s"' % _format, show=False, quiet=True)

    if not quiet:
        line = border(char * (
            len(' '.join([env.host_string, sep, stamp])) + 2))

        output = ' '.join([
            side,
            green(stamp, bold=True),
            blue(sep, bold=True),
            white(env.host_string, bold=True),
            side,
        ])

        puts('\n' + indent([line, output, line], spaces=4) + '\n',
             show_prefix=False)

    return stamp


@task
@log_call
def tailgun(log_file):
    """ Tails a given log file. If the given path is relative, the path is
    prepended with env.log.
    """
    if not log_file.startswith('/'):
        log_file = os.path.join(env.log, log_file)

    timestamp(log=False)

    with settings(output_prefix=False):
        sudo('true', quiet=True, show=False)
        sudo('tail -f %s' % log_file)
