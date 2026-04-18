========
SiteData
========

.. currentmodule:: beemo.site_data

A ``SiteData`` object is passed into each template, so the template author can use its attributes to
display content, giving access to the entire site content and config, regardless of which page is
currently being written.

For example, within a post template, you could use the following code to display a list of recent
posts in the sidebar:

.. code-block::

    <aside>
        <h2>Recent Posts</h2>
        <ul>
            <li tal:repeat="post site.posts[:10]"><a href="${post.link}">${post.title}</a></li>
        </ul>
    </aside>


.. autoclass:: SiteData()
    :members: config, homepage, posts, pages, tags, archive, now