Deploy to Server
================

Build a Release
---------------

Use the standard setuptools to build a release.  Builds are placed in the dist directory.

.. code-block:: bash

    ./setup.py sdist

Virtualenv
----------

On production, the application is run as a distinct user.  That user's home directory is also the virtualenv for installation.  The bin directory is added to the path, so no activation is necessary. To install a new version of the software:

.. code-block:: bash

    # upload the sdist from the dev machine
    rsync -zP ./dist/sopy-1.1.tar.gz

    # on sopython.com
    sudo -iu sopython
    # uninstall the old version
    pip uninstall -y sopy
    # install the new build
    pip install ~davidism/sopy

Initial Setup
^^^^^^^^^^^^^

First create the user and virtualenv, and install the packages.

.. code-block:: bash

    sudo useradd -m -U -s /bin/bash sopython
    sudo -iu sopython
    virtualenv -p /usr/bin/python3 ./
    # add ``export PATH="$HOME/bin:$PATH"`` to .bashrc
    # then logout/login as sopython again
    pip install -U pip setuptools
    pip install ipython sphinx
    pip install ~davidism/sopy-1.1.tar.gz

The application configuration is located in ./var/sopy-instance/config.py

.. code-block:: python

    DEBUG = False
    SECRET_KEY = <str>
    SERVER_NAME = 'sopython.com'

    SE_API_KEY = <str>
    SE_CONSUMER_KEY = <int>
    SE_CONSUMER_SECRET = <str>

Supervisor
----------

Supervisor manages starting and restarting the application.  Restart the application when a new release is installed.  The in-memory code continues running until then.

.. code-block:: bash

    sudo supervisorctl restart sopy-uwsgi

Supervisor itself runs as a system service, but only needs to be reloaded if the configuration files change.

.. code-block:: bash

    sudo service supervisor restart

Configuration
^^^^^^^^^^^^^

./supervisor.conf

.. code-block:: ini

    [program:sopy-uwsgi]
    command = /home/sopython/bin/uwsgi --ini /home/sopython/uwsgi.ini
    priority = 944
    directory = /home/sopython
    user = sopython
    stopsignal = INT
    autostart = true
    autorestart = true
    startretries = 1
    redirect_stderr = true
    stdout_logfile = /home/sopython/uwsgi.log

Symlink this to /etc/supervisor/conf.d/sopy.conf.

.. code-block:: bash

    sudo ln -s supervisor.conf /etc/supervisor/conf.d/sopy.conf

uWSGI
-----

uWSGI runs the application in a multi-process/multi-thread setup.  It creates a socket that the web server will talk to to serve to the outside network.  It is controlled by Supervisor and is not controlled separately.

Configuration
^^^^^^^^^^^^^

./uwsgi.ini

.. code-block:: ini

    [uwsgi]
    master = true
    processes = 8
    threads = 2
    socket = /home/sopython/uwsgi.sock
    chmod-socket = 666
    vacuum = true
    chdir = /home/sopython
    virtualenv = /home/sopython
    module = sopy:create_app()

Nginx
-----

Nginx acts as a reverse proxy to the uWSGI application.  It runs as a system service and only needs to be reloaded if configuration changes.

.. code-block:: bash

    sudo service nginx reload

Configuration
^^^^^^^^^^^^^

./nginx.conf

.. code-block:: nginx

    server {
        listen 80 default_server;
        listen [::]:80 ipv6only=on default_server;

        server_name sopython.com;

        root /home/sopython;

        location /static {
            alias /home/sopython/lib/python3.4/site-packages/sopy/static;
        }

        location / {
            include uwsgi_params;
            uwsgi_param HTTP_HOST $server_name;
            uwsgi_pass unix:///home/sopython/uwsgi.sock;
        }
    }

Symlink this to /etc/nginx/sites-enabled/sopy.conf.

.. code-block:: bash

    sudo ln -s nginx.conf /etc/nginx/sites-enabled/sopy.conf

PostgreSQL
----------

Postgresql runs as a system service.  Normally, it will not need direct control.

.. code-block:: bash

    sudo service postgresql restart

Initial Data
^^^^^^^^^^^^

Create a blank database and run the migrations to build the schema.

.. code-block:: bash

    createdb sopy
    sopy db upgrade

Backup/Restore
^^^^^^^^^^^^^^

.. code-block:: bash

    # custom format (-Fc) doesn't work across postgresql major versions, but is much faster
    pg_dump -Fc sopy -f sopy.db
    # restore to a new, empty database (no tables, no data)
    pg_restore -d sopy sopy.db
