# Local Development

1.  Check out the repo:
```bash
  $ git clone git://github.com/blackrobot/pong.git
```

1.  Create a virtual environment:
```bash
  $ mkvirtualenv pong
```

1.  Enter your vitrtual environment, and install the packages:
```bash
  $ workon pong
  $ pip install -r requirements.txt
```

1.  Grab some Sass
```bash
  $ gem install sass || sudo gem install sass
```

1.  Copy settings/local.py.example to local.py, and customize with your
database info:
```bash
  $ cp source/settings/local.py.example source/settings/local.py
```

1.  Create your database, then run syncdb and fake migrations:
```bash
  $ python manage.py syncdb --all
```

1.  Startup your server:
```bash
  $ python manage.py runserver
```
