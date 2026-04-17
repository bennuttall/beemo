=============
Configuration
=============

Beemo is configured with a YAML file. The config file has three optional sections: ``build``,
``logs``, and ``analytics``. All paths are relative to the config file.

The path to the config file must be set in the environment variable ``BEEMO_CONFIG``.

The config file can be structured in a way that avoids repetition — keys shared between sections can
be placed at the top level, and each section inherits the top-level value unless it defines its own.

Build
=====

Beemo has three modes for different types of websites:

Pages-only mode
---------------

For a simple website with static pages and no blog posts. Only the ``pages_dir`` key is required in
the config file:

.. code-block:: yaml

    build:
        pages_dir: content/pages
        static_dir: static
        templates_dir: templates
        output_dir: www

Blog-only mode
--------------

For a blog with no static pages. Only the ``posts_dir`` key is required in the config file:

.. code-block:: yaml

    build:
        posts_dir: content/posts
        static_dir: static
        templates_dir: templates
        output_dir: www

Pages + blog mode
-----------------

For a website with both static pages and blog posts. Both ``pages_dir`` and ``posts_dir`` keys are
required in the config file. Archives, tag indexes and such are generated automatically:

.. code-block:: yaml

    build:
        posts_dir: content/posts
        pages_dir: content/pages
        static_dir: static
        templates_dir: templates
        output_dir: www

Optional build keys
-------------------

``blog_root`` sets the path prefix for blog URLs (default: empty, i.e. posts at ``/year/month/slug/``):

.. code-block:: yaml

    build:
        blog_root: blog   # posts served at /blog/year/month/slug/

``base_url`` sets the site's base URL, made available to templates via ``site.config.base_url``:

.. code-block:: yaml

    build:
        base_url: https://mysite.com

Logs
====

When running the ``beemo logs`` command, the config file must have a ``logs`` section with the
following keys:

.. code-block:: yaml

    logs:
        logs_dir: apache2                  # directory of gzipped Apache log files
        pattern: "mysite.com-access*"      # glob filter for log filenames (default: *.gz)

Analytics
=========

When running the ``beemo analytics`` command, the config file must have an ``analytics`` section
with the following keys:

.. code-block:: yaml

    analytics:
        csv_dir: csv                       # input directory of CSV files from beemo logs
        templates_dir: templates           # Chameleon templates directory
        output_dir: analytics              # output directory for the analytics site
        manifest_path: www/manifest.json   # path to manifest.json produced by beemo build
        base_url: https://mysite.com
        title: ""                          # optional; derived from base_url if omitted