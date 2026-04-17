======
Scribe
======

The Scribe is responsible for determining the site structure and contents. The Scribe passes itself
into each template, so the template author can use its attributes to display content, giving access
to the entire site content and config, regardless of which page is currently being written. 

For example, within a post template, you could use the following code to display a list of recent
posts in the sidebar:

.. code-block::

    <aside>
        <h2>Recent Posts</h2>
        <ul>
            <li tal:repeat="post scribe.posts[:10]"><a href="${post.url}">${post.title}</a></li>
        </ul>
    </aside>

.. currentmodule:: beemo.scribe

.. autoclass:: TheScribe
    :members: