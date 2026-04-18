======
Config
======

.. currentmodule:: beemo.settings

The :class:`BuildConfig` class contains the configuration for a Beemo site build. It is available as
the ``config`` attribute of the :class:`~beemo.site_data.SiteData` object passed into templates, so
template authors can use its attributes to display content.

.. autoclass:: BuildConfig()
    :members: pages_dir, posts_dir, static_dir, templates_dir, output_dir, blog_root, base_url
    :undoc-members:
    :show-inheritance: 