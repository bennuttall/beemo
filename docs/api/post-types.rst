==========
Post Types
==========

.. currentmodule:: beemo.post_types

Beemo uses `Pydantic`_ models to validate content metadata files.

.. _Pydantic: https://docs.pydantic.dev/latest/

Page and Post models are passed into Beemo templates, so template authors can use their attributes
to display content.

For example, within a post template, you could use the following code to display the post's title
and content:

.. code-block::

    <h1>${post.title}</h1>
    <div>${post.html}</div>

See :doc:`../templates` for more information on how to use these objects within templates.

.. autoclass:: Page()
    :members: post_type, slug, title, description, html, text, excerpt, og_image, template, cover_image, author, images, link
    :undoc-members:
    :show-inheritance:

.. autoclass:: HomePage()
    :members: post_type, slug, title, description, html, text, excerpt, og_image, template, cover_image, author, images, link
    :undoc-members:
    :show-inheritance:

.. autoclass:: Post()
    :members: post_type, slug, title, description, html, html_atom_safe, text, excerpt, og_image, template, cover_image, author, images, link, published, modified, modified_diff, tags
    :undoc-members:
    :show-inheritance:
    
.. note::

    Note that these models allow extra fields to be included in the metadata files, which can be
    accessed within templates. For example, if a post's metadata file includes a `hero_image` field,
    you could access it within a template using `${post.hero_image}`. However, no processing can
    take place so they will remain as strings.

    Also any metadata files which are missing these additional fields may cause template errors as
    they do not exist as attributes on other instances, so be sure to include them in all metadata
    files if you intend to use them within templates.