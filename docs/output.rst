============
Output files
============

``beemo build`` writes all output to ``output_dir``. Static files from ``static_dir`` are copied
in first; everything else is generated.

HTML pages
==========

.. list-table::
   :header-rows: 1

   * - Path
     - Description
   * - ``index.html``
     - Site homepage (requires ``pages_dir``)
   * - ``{slug}/index.html``
     - Individual pages (one per page in ``pages_dir``)
   * - ``{blog_root}/index.html``
     - Blog index
   * - ``{blog_root}/{year}/{month}/{slug}/index.html``
     - Individual blog posts
   * - ``{blog_root}/{year}/index.html``
     - Year archive pages
   * - ``{blog_root}/{year}/{month}/index.html``
     - Month archive pages
   * - ``{blog_root}/tags/index.html``
     - Tags index
   * - ``{blog_root}/tags/{tag}/index.html``
     - Individual tag pages
   * - ``{blog_root}/archive/index.html``
     - Full blog archive

``{blog_root}`` is the value of ``blog_root`` in the build config (default: empty, so paths start
from the output root).

Data files
==========

.. list-table::
   :header-rows: 1

   * - File
     - Description
   * - ``sitemap.xml``
     - XML sitemap listing all pages and posts
   * - ``{blog_root}/atom.xml``
     - Atom feed of blog posts
   * - ``posts.json``
     - JSON array of posts with ``title``, ``link``, and ``published`` fields
   * - ``manifest.json``
     - JSON array of all pages with URL, title, type, and (for posts) published date and tags;
       used by ``beemo analytics`` to enrich log data with page metadata
