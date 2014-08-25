Install for Development
=======================

Download Source
---------------

Clone the repository, create a virtualenv, then install it in editable mode to get started.  Assumes the use of `virtualenvwrapper`_.  Currently, the development version of Flask is required, this will change once Flask-1.0 is released. ::

    cd Projects/
    git clone ssh://git@github.com/sopython/sopython-site sopy
    cd sopy/
    mkvirtualenv -p /usr/bin/python3 sopy
    pip install https://github.com/mitsuhiko/flask/archive/master.zip
    pip install -e .

.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/

Create Database
---------------

Create a PostgreSQL database.  The application defaults to a local database named "sopy".  Then run the migrations to get the latest schema. ::

    createdb sopy
    sopy db upgrade

Run Server
----------

Run the local development server in debug mode.  Set the host to "localhost" instead of the default "127.0.0.1" so that cookies work in Chrome. ::

    sopy --debug run -h localhost

Configuration
-------------

Local configuration is read from "./instance/config.py" in the project folder.  This is not created by default.

The application uses OAuth with Stack Exchange for authentication.  This requires a registered application with Stack Apps, pointing to "localhost" for development.  If you do not provide credentials and are in debug mode, the application will fall back to fake authentication by just entering a Stack Overflow user id.  This should work for most development purposes.  Set the following configuration values if you have an application key::

    SE_API_KEY = <str>
    SE_CONSUMER_KEY = <int>
    SE_CONSUMER_SECRET = <str>

Update
------

Pull the latest changes and run any database migrations::

    git pull origin master
    sopy db upgrade

Making Changes
--------------

Keep features in separate branches if development will take a while.  When pulling, use the ``--rebase`` flag to avoid unnecessary merges if possible.  When making a new release, change the version information in setup.py, commit, tag with the same version, then update the version to "<next-version>-dev" and commit again.
