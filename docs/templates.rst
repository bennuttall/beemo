=========
Templates
=========

.. currentmodule:: beemo

Beemo uses `Chameleon <https://chameleon.readthedocs.io/en/latest/>`_ page templates (``*.pt``
files). All site build templates receive a ``site`` argument — an instance of
:class:`~site_data.SiteData` — as well as ``post`` and ``page`` arguments (one will be the relevant
content object for that template; the other will be ``None``). This allows the layout template to
detect context regardless of which template is active. Template-specific variables are listed below.
The ``site`` instance exposes the following attributes that templates commonly use:

.. list-table::
   :header-rows: 1

   * - Attribute
     - Description
   * - ``site.posts``
     - All posts, sorted by ``published`` date (descending)
   * - ``site.pages``
     - All pages
   * - ``site.tags``
     - Dict mapping tag name → list of posts, sorted by number of posts then alphabetically
   * - ``site.config``
     - The active build configuration
   * - ``site.now``
     - The current UTC datetime (set at build time)

Site build templates
====================

These templates are placed in your configured ``templates_dir``.

layout
------

**File:** ``layout.pt``

The layout template is not rendered directly. It defines a ``layout`` macro that is passed into
all other site build templates so they can share a common page structure.

home
----

**File:** ``home.pt``

**Used for:** the site homepage (``index.html``).

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``site``
     - The ``SiteData`` instance
   * - ``page``
     - The homepage ``Page`` object
   * - ``layout``
     - The ``layout`` macro from ``layout.pt``

page
----

**File:** ``page.pt``

**Used for:** each individual page (one per page in ``pages_dir``). A page can override this with
a ``template`` field in its ``meta.yml``.

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``site``
     - The ``SiteData`` instance
   * - ``page``
     - The ``Page`` object for this page
   * - ``layout``
     - The ``layout`` macro from ``layout.pt``

post
----

**File:** ``post.pt``

**Used for:** each individual blog post. A post can override this with a ``template`` field in its
``meta.yml``.

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``site``
     - The ``SiteData`` instance
   * - ``post``
     - The ``Post`` object for this post
   * - ``prev_post``
     - The previous (older) ``Post``, or ``None``
   * - ``next_post``
     - The next (newer) ``Post``, or ``None``
   * - ``page``
     - Always ``None`` for this template
   * - ``layout``
     - The ``layout`` macro from ``layout.pt``

blog
----

**File:** ``blog.pt`` (optional)

**Used for:** the blog index page. If ``blog.pt`` does not exist, the ``posts`` template is used
instead (see below).

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``site``
     - The ``SiteData`` instance
   * - ``title``
     - Page title (``"Blog"``)
   * - ``link``
     - Path to the blog root
   * - ``layout``
     - The ``layout`` macro from ``layout.pt``

posts
-----

**File:** ``posts.pt``

**Used for:** the blog index (fallback when ``blog.pt`` is absent), year archive pages, month
archive pages, and tag pages.

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``site``
     - The ``SiteData`` instance
   * - ``title``
     - Page title (e.g. ``"Blog"``, ``"Archive: 2024"``, ``"Tag: python"``)
   * - ``link``
     - Path to this listing page
   * - ``posts``
     - List of ``Post`` objects to display (omitted for the blog index fallback)
   * - ``layout``
     - The ``layout`` macro from ``layout.pt``

tags
----

**File:** ``tags.pt``

**Used for:** the tags index page, listing all tags.

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``site``
     - The ``SiteData`` instance
   * - ``title``
     - Page title (``"Tags"``)
   * - ``link``
     - Path to the tags index
   * - ``layout``
     - The ``layout`` macro from ``layout.pt``

archive
-------

**File:** ``archive.pt``

**Used for:** the full blog archive page.

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``site``
     - The ``SiteData`` instance
   * - ``title``
     - Page title (``"Blog archive"``)
   * - ``link``
     - Path to the archive page
   * - ``layout``
     - The ``layout`` macro from ``layout.pt``

sitemap
-------

**File:** ``sitemap.pt``

**Used for:** generating ``sitemap.xml``.

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``site``
     - The ``SiteData`` instance
   * - ``years``
     - Set of years (integers) that have posts
   * - ``months``
     - Set of ``(year, month)`` tuples for all months that have posts

atom
----

**File:** ``atom.pt``

**Used for:** generating the Atom feed (``<blog_root>/atom.xml``).

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``site``
     - The ``SiteData`` instance

Post and Page objects
=====================

Both ``Page`` and ``Post`` share the following attributes:

.. list-table::
   :header-rows: 1

   * - Attribute
     - Description
   * - ``title``
     - Post or page title
   * - ``html``
     - Rendered HTML content
   * - ``text``
     - Plain text content (HTML tags stripped)
   * - ``excerpt``
     - Short excerpt (auto-derived from ``text`` if not set in ``meta.yml``)
   * - ``description``
     - Meta description (defaults to ``excerpt`` if not set)
   * - ``slug``
     - URL slug (derived from the content directory name)
   * - ``link``
     - Path relative to the output root
   * - ``images``
     - List of image file paths from the ``images/`` subdirectory
   * - ``cover_image``
     - Optional cover image filename
   * - ``og_image``
     - Optional Open Graph image filename
   * - ``author``
     - Optional author name

``Post`` has these additional attributes:

.. list-table::
   :header-rows: 1

   * - Attribute
     - Description
   * - ``published``
     - Publication datetime (UTC)
   * - ``modified``
     - Last-modified datetime (defaults to ``published``)
   * - ``modified_diff``
     - ``True`` if ``modified`` differs from ``published``
   * - ``tags``
     - List of tag strings