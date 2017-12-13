sopython
========

Welcome to **so**\ python, the website of the Python community on
`Stack Overflow`_.

Join us for chat in the `Python room`_!

.. _Stack Overflow: https://stackoverflow.com/questions/tagged/python?sort=frequent
.. _Python room: https://chat.stackoverflow.com/rooms/6/python


Develop
-------

::

    git clone ssh://git@github.com/sopython/sopython-site
    cd sopython-site
    pip install -e '.[dev]'


Documentation
-------------

::

    cd docs/
    sphinx-build ./ ./_build/
