python-stockfighter
====
A stockfighter API written in Python. Docs can be found `here <http://akshaynanavati.github.io/python-stockfighter>`_.

It wraps the api methods described `here <https://starfighter.readme.io/docs/>`_ with Python function calls using the requests_
library. This project is still a WIP, but the basic functionality exists. Things like tests,
documentation, and error handling are yet to be built. This project is simply meant to provide
a nice python api for accessing the HTTP API provided by stockfighter. Please do not commit
anything that might give away solutions to any of the stockfighter challenges.

Installing
----
This package is not yet on pypi. Thus, install it using pip editable:

    $ pip install -e git+git@github.com:akshaynanavati/python-stockfighter@<desired-version>#egg=python-stockfighter

i.e.

    $ pip install -e git+git@github.com:akshaynanavati/python-stockfighter@v0.0.1#egg=python-stockfighter

Repl
----
This library also provides a repl which can be run with `sfrepl.py` if this package is installed in the current `venv`.
The repl can be used to buy/sell stocks and view order status from the command line. Supported repl methods:

- ``{buy, sell} <order_type> <int> shares of <exchange>:<stock> at <price>``
- ``set account <account-number>``
- ``orderbook <exchange>:<stock>``

Contributing
----
Fork the repository, and open a PR for your feature(s). In the `Makefile` there are some convenience
options to expedite development.

.. _requests: http://docs.python-requests.org/en/latest/
