=====
beemo
=====

A Python-based static site generator. Bring your own content and templates and it'll quickly
generate you a deployable HTML website/blog. Also includes support for building a simple analytics
site based on the known site structure by processing Apache logs.

.. image:: https://raw.githubusercontent.com/bennuttall/beemo/refs/heads/main/beemo.png

PyPI
====

- `beemo <https://pypi.org/project/beemo/>`_

Features
========

- Content as HTML, markdown or reStructuredText
- Pages
- Posts
- Tags
- Archives (index, years and months)
- XML sitemap
- Atom feed
- Custom Chameleon templates
- Custom CSS, JS and other static files
- Apache log analytics (optional, via ``beemo[logs]``)

Install
=======

Install the latest release with:

.. code-block:: bash

   pip install beemo

For Apache log analytics, install the ``logs`` extra:

.. code-block:: bash

   pip install beemo[logs]

Development
-----------

Create a virtual environment and run ``make develop`` to install the library and its dependencies.

Examples
========

Sites built with Beemo:

- `bennuttall.com <https://bennuttall.com>`_ (`repo <https://github.com/bennuttall/web-content>`__)
- `blog.piwheels.org <https://blog.piwheels.org>`_ (`repo <https://github.com/piwheels/blog>`__)
- `pynw.org <https://pynw.org/>`_ (`repo <https://github.com/pythonnorthwestengland/pynw.org>`__)
- `pyjok.es <https://pyjok.es/>`_ (`repo <https://github.com/pyjokes/website>`__)

If you wish to use this project for your own website, these examples will be a useful reference.

Licence
=======

- `BSD-3-Clause <LICENSE.txt>`_

Table of Contents
=================

.. toctree::
   :maxdepth: 4
   :titlesonly:

   usage
   content
   templates
   config
   output
   analytics
   cli/index
   api/index