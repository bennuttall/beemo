=============
Log analytics
=============

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
your other Chameleon templates. See :doc:`templates` for the full list of template variables.