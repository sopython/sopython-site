**so**\ python
==============

Cabbage, World!

Welcome to **so**\ python, the website of the Python community on `Stack Overflow`_.

Join us for chat in the `Python room`_!

.. _Stack Overflow: http://stackoverflow.com/
.. _Python room: http://chat.stackoverflow.com/rooms/6/python

Develop
-------

::

    git clone ssh://git@github.com/sopython/sopython-site sopy
    pip install -e git+ssh://git@github.com/mitsuhiko/flask#egg=flask
    pip install -e ./sopy
    createdb sopy
    sopy db upgrade
    sopy --debug run -h localhost
