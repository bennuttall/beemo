==========
Post Types
==========

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

.. currentmodule:: beemo.post_types

.. autoclass:: Page
    :members:
    :show-inheritance:

.. autoclass:: HomePage
    :members:
    :show-inheritance:

.. autoclass:: Post
    :members:
    :show-inheritance:

.. autoclass:: PostType
    :members:
    :show-inheritance: