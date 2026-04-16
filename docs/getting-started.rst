===============
Getting started
===============

Create content directories e.g. ``posts``, ``pages``, ``static`` and ``templates``.

Posts
=====

If you want to have a blog, create a ``posts`` directory and populate it with your blog posts. Each
post must be in its own directory but can be organised in any hierarchy e.g. by year, year/month or
just flat. Post directories must contain a ``meta.yml`` and a content file (``index.html``,
``index.md`` or ``index.rst``), and may contain images in an ``images`` directory, used within your
post.

Pages
=====

If you want to have pages, create a ``pages`` directory and populate it with your pages. Each page
must be in its own directory. Page directories must contain a ``meta.yml`` and a content file
(``index.html``, ``index.md`` or ``index.rst``), and may contain images in an ``images`` directory,
used within your page.

Static
======

Any files in your ``static`` directory will be copied into the site build root. Keep your CSS files
and such in this directory.

Templates
=========

Create Chameleon templates for your site in the ``templates`` directory. See the
`Chameleon docs <https://chameleon.readthedocs.io/en/latest/>`_ for reference, and :doc:`templates`
for the full list of templates and their variables.

Build
=====

Install Beemo:

.. code-block:: bash

   pip install beemo

Build your site by running the command ``beemo build`` with the environment variable
``BEEMO_CONFIG`` set pointing at a valid config file. It will build your site into your configured
``output_dir``.

You can then serve the built site locally with e.g. ``python -m http.server -d www`` and view it at
e.g. ``http://localhost:8000``. Make changes to your content or templates and rebuild to see them
reflected in the built site.

Deploy
======

Once you're happy with your site, you can deploy it to your hosting provider. This will depend on
your provider, but typically involves copying the contents of your ``output_dir`` to your hosting
provider's server, or building your site on the server and moving the built files to the appropriate
location.