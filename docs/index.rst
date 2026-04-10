beemo
=====

A Python-based static site generator. Bring your own content and templates and it'll quickly
generate you a deployable HTML website/blog. Also includes support for building a simple analytics
site based on the known site structure by processing Apache logs.

.. image:: https://raw.githubusercontent.com/bennuttall/beemo/refs/heads/main/beemo.png

PyPI
----

- `beemo <https://pypi.org/project/beemo/>`_

Features
--------

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

Usage
-----

Create content directories e.g. ``posts``, ``pages``, ``static`` and ``templates``.

Posts
~~~~~

Populate your ``posts`` directory with your blog posts. Each post must be in its own directory but
can be organised in any hierarchy e.g. by year, year/month or just flat. Post directories must
contain a ``meta.yml`` and a content file (``index.html``, ``index.md`` or ``index.rst``), and can
contain images in an ``images`` directory, used within your post.

Pages
~~~~~

Populate your ``pages`` directory with your pages. Each page must be in its own directory. Page
directories must contain a ``meta.yml`` and a content file (``index.html``, ``index.md`` or
``index.rst``).

Static
~~~~~~

Any files in your ``static`` directory will be copied into the site build root. Keep your CSS files
and such in this directory.

Templates
~~~~~~~~~

Create Chameleon templates for your site in the ``templates`` directory. See the
`Chameleon docs <https://chameleon.readthedocs.io/en/latest/>`_ for reference.

Configuration
-------------

The Beemo config file is a YAML file with three optional sections: ``build``, ``logs``, and
``analytics``. All paths are relative to the config file.

Keys shared between sections can be placed at the top level to avoid repetition — each section
inherits the top-level value unless it defines its own.

Site build
~~~~~~~~~~

The ``build`` section configures the ``beemo build`` command. Here ``pages_dir`` and ``posts_dir``
are both specified — the site will be built with both pages and blog posts:

.. code-block:: yaml

   build:
     posts_dir: content/posts
     pages_dir: content/pages
     static_dir: static
     templates_dir: templates
     blog_root: blog
     output_dir: www

Omit ``pages_dir`` for blog-only mode, or omit ``posts_dir`` for pages-only mode. Either one must
be present. If ``posts_dir`` is specified, archives, tag indexes and such are generated
automatically.

Log analytics
~~~~~~~~~~~~~

Optional ``logs`` and ``analytics`` sections configure the ``beemo logs`` and ``beemo analytics``
commands. All directory paths are required — there are no hardcoded defaults.

.. code-block:: yaml

   logs:
     logs_dir: apache2                  # directory of gzipped Apache log files
     pattern: "mysite.com-access*"      # glob filter for log filenames (default: *.gz)

   analytics:
     output_dir: html/mysite            # output directory for the analytics site
     base_url: https://mysite.com
     title: ""                          # optional; derived from base_url if omitted

If ``templates_dir`` or ``csv_dir`` are shared between sections, they can be hoisted to the top
level to avoid repetition — each section inherits the top-level value unless it defines its own:

.. code-block:: yaml

   templates_dir: templates
   csv_dir: csv

   build:
     posts_dir: content/posts
     pages_dir: content/pages
     static_dir: static
     blog_root: blog
     output_dir: www

   logs:
     logs_dir: apache2
     pattern: "mysite.com-access*"

   analytics:
     output_dir: analytics
     base_url: https://mysite.com

The analytics output is a multi-page site:

.. code-block:: text

   output_dir/
   ├── index.html          ← last 30 days summary
   └── 2026/
       ├── index.html      ← full year
       ├── 03/
       │   └── index.html  ← March 2026
       └── 04/
           └── index.html  ← April 2026

The analytics template (``analytics.pt``) must be placed in your site's ``templates_dir`` alongside
your other Chameleon templates. It receives the following template variables:

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``report``
     - Analytics data dict (totals, hits by day/month, pages, UAs, referrers)
   * - ``nav``
     - Navigation context (breadcrumbs, year/month links, current page)
   * - ``json``
     - Python's ``json`` module, for serialising chart data
   * - ``datetime``
     - Python's ``datetime`` class, for formatting ISO date strings

Dates in ``report`` are ISO strings (``2026-03-01``) so templates can format them as needed.

Environment variables
~~~~~~~~~~~~~~~~~~~~~

The only environment variable required is ``BEEMO_CONFIG`` which must point to your site's config
file:

.. code-block:: bash

   export BEEMO_CONFIG=config.yml

Install
-------

Install the latest release with:

.. code-block:: bash

   pip install beemo

For Apache log analytics, install the ``logs`` extra:

.. code-block:: bash

   pip install beemo[logs]

Development
~~~~~~~~~~~

Create a virtual environment and run ``make develop`` to install the library and its dependencies.

Build
~~~~~

Build your site by running the command ``beemo build`` with the environment variable ``BEEMO_CONFIG``
set pointing at a valid config file. It will build your site into your configured ``output_dir``.

This can be served locally with e.g. ``python -m http.server -d www`` and viewed at e.g.
``http://localhost:8000``.

Log analytics
~~~~~~~~~~~~~

With ``beemo[logs]`` installed and ``logs``/``analytics`` sections in your config, run the full
pipeline:

.. code-block:: bash

   beemo logs       # process Apache gz logs → CSV files
   beemo analytics  # generate HTML analytics site

Both subcommands read their defaults from ``BEEMO_CONFIG``. Any setting can be overridden on the
command line — run with ``--help`` for details.

Process your Apache logs with ``beemo logs`` and build your analytics site with ``beemo analytics``
with the environment variable ``BEEMO_CONFIG`` set pointing at a valid config file. It will build
your analytics site into your configured ``output_dir``.

This can be served locally with e.g. ``python -m http.server -d analytics`` and viewed at e.g.
``http://localhost:8000``.

``beemo analytics`` is incremental: year and month pages are skipped if their output file is newer
than all source CSVs. The summary page (last 30 days) always regenerates.

Examples
--------

Sites built with Beemo:

- `bennuttall.com <https://bennuttall.com>`_ (`repo <https://github.com/bennuttall/web-content>`__)
- `blog.piwheels.org <https://blog.piwheels.org>`_ (`repo <https://github.com/piwheels/blog>`__)
- `pynw.org <https://pynw.org/>`_ (`repo <https://github.com/pythonnorthwestengland/pynw.org>`__)
- `pyjok.es <https://pyjok.es/>`_ (`repo <https://github.com/pyjokes/website>`__)

If you wish to use this project for your own website, these examples will be a useful reference.

Licence
-------

- `BSD-3-Clause <LICENSE.txt>`_
