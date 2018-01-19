Welcome to fossir's documentation!
==================================


.. raw:: html
    :file: _static/github_star.html

.. image:: images/fossir.png
    :width: 300 px
    :align: center

.. epigraph:: *The effortless open source tool for event organization, archival and collaboration.*

|build-status| |license| |pypi-ver|

Welcome to fossir's documentation. This documentation is split into several parts, from `installing fossir <installation/>`_ to developing `fossir plugins <plugins>`_.
To dive into the internals of fossir, check out the `API documentation <api>`_. Read more about fossir in our `official website <https://getfossir.io>`_.


Installation / Configuration
++++++++++++++++++++++++++++

.. include:: installation/_intro.rst

.. toctree::
    :maxdepth: 2

    installation/index.rst


Server administration
+++++++++++++++++++++

.. include:: admin/_intro.rst

.. toctree::
    :maxdepth: 2

    admin/index.rst


Plugins
+++++++

.. include:: plugins/_intro.rst

.. toctree::
    :maxdepth: 2

    fossir plugins <plugins/index.rst>


HTTP API
++++++++

.. include:: http_api/_intro.rst

.. toctree::
    :maxdepth: 2

    HTTP API <http_api/index.rst>


API reference
+++++++++++++

.. include:: api/_intro.rst

.. toctree::
    :maxdepth: 2

    api/index.rst


What's New
++++++++++

.. toctree::
    :maxdepth: 2

    changelog.rst


Indices and tables
++++++++++++++++++

* :ref:`genindex`
* :ref:`modindex`

.. |build-status| image:: https://travis-ci.org/fossir/fossir.png?branch=master
                   :alt: Travis Build Status
                   :target: https://travis-ci.org/fossir/fossir
.. |pypi-ver| image:: https://img.shields.io/pypi/v/fossir.png
                   :alt: Available on PyPI
                   :target: https://pypi.python.org/pypi/fossir/
.. |license| image:: https://img.shields.io/github/license/fossir/fossir.png
                   :alt: License
                   :target: https://github.com/fossir/fossir/blob/master/COPYING
