import multiprocessing
from os import path

base = path.realpath(path.join(path.dirname(__file__), '..', '..', '..'))
pidfile = path.join(base, 'pids', 'gunicorn.pid')
errorlog = path.join(base, 'log', 'gunicorn.error.log')

# Lower this number if you have multiple production sites on the same server
workers = multiprocessing.cpu_count() * 2 + 1

user = 'djablons'
group = 'djablons'
bind = '127.0.0.1:8100'
accesslog = None
loglevel = 'info'
