==============
Adding content
==============

Posts and pages are each stored as a directory containing a ``meta.yml`` file and a content file.
The content file can be HTML (``index.html``), Markdown (``index.md``), or reStructuredText
(``index.rst``). An optional ``images/`` subdirectory holds image files used within the content.

The directory name is used as the slug for both posts and pages.

Posts
=====

Post directories can be organised in any hierarchy inside ``posts_dir`` — by year, year/month, or
flat. Beemo finds them by searching recursively for ``meta.yml`` files.

Example layout:

.. code-block:: text

   posts/
   └── 2026/
       └── 04/
           └── my-first-post/
               ├── meta.yml
               ├── index.md
               └── images/
                   └── photo.jpg

**meta.yml fields:**

.. list-table::
   :header-rows: 1

   * - Field
     - Required
     - Description
   * - ``title``
     - Yes
     - Post title
   * - ``published``
     - Yes
     - Publication date/time (e.g. ``2026-04-17`` or ``2026-04-17 12:00:00``)
   * - ``modified``
     - No
     - Last-modified date/time (defaults to ``published``)
   * - ``tags``
     - No
     - List of tag strings (lowercase alphanumeric and hyphens only)
   * - ``description``
     - No
     - Meta description (defaults to auto-derived ``excerpt``)
   * - ``excerpt``
     - No
     - Short summary (auto-derived from content if omitted)
   * - ``author``
     - No
     - Author name
   * - ``cover_image``
     - No
     - Filename of cover image (from ``images/``)
   * - ``og_image``
     - No
     - Filename of Open Graph image (from ``images/``)
   * - ``template``
     - No
     - Custom template name to use instead of ``post`` (without ``.pt`` extension)

Example ``meta.yml`` for a post:

.. code-block:: yaml

   title: My first post
   published: 2026-04-17
   tags:
     - python
     - beemo
   cover_image: images/photo.jpg

Pages
=====

Page directories sit directly inside ``pages_dir``. There is one special directory named ``home``
which provides the content for the site homepage — it is served at ``/`` and does not use the
directory name as a slug. All other directories become individual pages, served at ``/{dirname}/``.

Example layout:

.. code-block:: text

   pages/
   ├── home/
   │   ├── meta.yml
   │   └── index.html
   └── about/
       ├── meta.yml
       └── index.md

**meta.yml fields:**

.. list-table::
   :header-rows: 1

   * - Field
     - Required
     - Description
   * - ``title``
     - Yes
     - Page title
   * - ``description``
     - No
     - Meta description (defaults to auto-derived ``excerpt``)
   * - ``excerpt``
     - No
     - Short summary (auto-derived from content if omitted)
   * - ``author``
     - No
     - Author name
   * - ``cover_image``
     - No
     - Filename of cover image (from ``images/``)
   * - ``og_image``
     - No
     - Filename of Open Graph image (from ``images/``)
   * - ``template``
     - No
     - Custom template name to use instead of ``page`` (without ``.pt`` extension)

Example ``meta.yml`` for a page:

.. code-block:: yaml

   title: About
