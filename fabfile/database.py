# -*- coding: utf-8 -*-

import copy
import datetime
import os

from fabric.api import env, get, local, task

from .django import DJANGO_SETTINGS, get_settings
from .utils import log_call, run


__all__ = ['dump', 'restore']


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

MYSQL = 'mysql'
POSTGRES = 'postgres'

ENGINES = {
    'postgresql_psycopg2': POSTGRES,
    'mysql': MYSQL,
}
EXTENSIONS = {
    POSTGRES: 'pgsql',
    MYSQL: 'sql.bz2',
}


def get_dir(path):
    """ This looks for the given path, prefixed with the project path if
    relative. If it doesn't exist, it creates it and caches it. It then
    returns the full absolute path to the directory as a string. For safety
    it will not attempt to create any directories which are not relative
    to the base project dir.
    """
    if not path.startswith('/'):
        path = os.path.abspath(os.path.join(BASE_DIR, path))

    if path.startswith(BASE_DIR) and not os.path.exists(path):
        os.makedirs(path)

    return path


def get_db_type(db_settings):
    engine = db_settings['ENGINE'].split('.')[-1]
    return ENGINES[engine]


def get_db_settings(local=True, key='default'):
    if local:
        return DJANGO_SETTINGS.DATABASES[key]
    return get_settings(env.django_settings).DATABASES[key]


def get_latest_dump(ext):
    tmp = os.path.join(get_dir(env.db_dir), '*.{}'.format(ext))
    return local('ls -t {} | head -1'.format(tmp), capture=True).strip()


def get_remote_filename(name, ext):
    now = datetime.datetime.now()
    return os.path.join(env.backup, '{}.{}.{}'.format(
        name, now.strftime('%Y-%m-%d.%H%M%S'), ext,
    ))


def postgres_dump(key='default'):
    db = get_db_settings(local=False, key=key)
    print db

    default_args = [
        '--no-acl',
        '--no-owner',
        '--format=custom',
        '--username={USER}',
    ]

    if 'HOST' in db:
        default_args.append('--host={HOST}')
    if 'PORT' in db:
        default_args.append('--port={PORT}')

    filename = get_remote_filename(db['NAME'], EXTENSIONS[POSTGRES])

    cmd = "PGPASSWORD='{}' pg_dump {} {} > {}".format(
        db['PASSWORD'],
        ' '.join(default_args).format(**db),
        db['NAME'],
        filename,
    )
    run(cmd)

    # Download the Bzip file we just created
    get(filename, local_path=get_dir(env.db_dir))


def postgres_restore(key='default'):
    default_args = [
        '--clean',
        '--no-acl',
        '--no-owner',
        '--username={USER}',
        '--dbname={NAME}',
    ]

    db = get_db_settings(key=key)

    if 'HOST' in db:
        default_args.append('--host={HOST}')
    if 'PORT' in db:
        default_args.append('--port={PORT}')

    filename = get_latest_dump(EXTENSIONS[POSTGRES])
    cmd = 'pg_restore {} {}'.format(
        ' '.join(default_args).format(**db),
        filename,
    )

    local(cmd)


def mysql_command(db, append=None, execute=None, **kwargs):
    """ This takes a list of strings as the first argument, a django styled
    dictionary of django database settings, and keyword arguments representing
    the context for string replacement. It then returns a rendered string
    filled with variables from the db, and appends the space-joined
    list of strings from the first argument.
    """
    context = copy.deepcopy(db)
    context.update(kwargs)

    args = [a for a in ('USER', 'PASSWORD', 'HOST', 'PORT') if a in context]
    opts = ['--{0}={1}'.format(a.lower(), a) for a in args]

    if execute:
        if execute[0] not in ('"', "'"):
            execute = '"{}"'.format(execute)
        opts.extend(['-e', execute])
    else:
        opts.append('{NAME}')

    cmd = ' '.join(opts + (append or [])).format(**context)

    return cmd


def mysql_restore(key='default'):
    """ By default, this will download the latest PSQL dump from the server
    and install it locally. If filename is given, this will download and
    restore the dump at the given filename.
    """
    db = get_db_settings(key=key)
    filename = get_latest_dump(EXTENSIONS[MYSQL])
    cmd = 'bunzip2 < {} | mysql {}'.format(filename, mysql_command(db))
    local(cmd)


def mysql_dump(key='default'):
    """ This will download a MySQL database from the remote server. """
    db = get_db_settings(local=False, key=key)
    filename = get_remote_filename(db['NAME'], EXTENSIONS[MYSQL])

    # Run the MySQL dump command piped to the Bzip command
    run('mysqldump {} | bzip2 > {}'.format(mysql_command(db), filename))

    # Download the Bzip file we just created
    get(filename, local_path=get_dir(env.db_dir))


@task
@log_call
def dump(key='default'):
    db_type = get_db_type(get_db_settings(local=False, key=key))

    if db_type is MYSQL:
        mysql_dump(key=key)

    elif db_type is POSTGRES:
        postgres_dump(key=key)


@task
@log_call
def restore(key='default'):
    db_type = get_db_type(get_db_settings(local=False, key=key))

    if db_type is MYSQL:
        mysql_restore(key=key)

    elif db_type is POSTGRES:
        postgres_restore(key=key)
