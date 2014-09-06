Using the Shell
===============

Even during development, the application is installed like a full package with pip (``pip install -e .``).  This makes working with the application consistent between development and production, as well as simplifies imports with other tools such as Sphinx and pytest.

The ``sopy`` command is available in the virtualenv to perform various tasks at the terminal.  Run ``sopy --help`` for a full list of sub-commands.

Common Commands
---------------

Activate the virtualenv first.  If you are using virtualenvwrapper, ``workon sopy``.  If you are on production, the virtualenv *is* the home folder of the application user, ``sudo -iu sopython``.

Start a shell::

    sopy shell

Add a user (by Stack Overflow id) to the approved group.  This can be done using the web interface as well. ::

    sopy auth load_user USER_ID
    sopy auth set_group USER_ID approved

List the editors with this query in the python shell::

    from sopy.auth.models import Group
    Group.query.filter_by(name='editor').one().users

Generate a database migration after making changes to the model code::

    sopy db revision 'description of changes'
    # the apply the migration
    sopy db upgrade
