from datetime import datetime

from .post_types import HomePage, Page, Post
from .settings import BuildConfig


class SiteData:
    """
    A collection of site data to be passed to templates during rendering
    """

    def __init__(
        self,
        config: BuildConfig,
        homepage: HomePage,
        pages: list[Page],
        posts: list[Post],
        archive: dict[int, list[Post]],
        tags: dict[str, list[Post]],
        now: datetime,
    ):
        self._config = config
        self._homepage = homepage
        self._pages = pages
        self._posts = posts
        self._archive = archive
        self._tags = tags
        self._now = now

    @property
    def config(self) -> BuildConfig:
        """
        The build configuration parsed from ``config.yml``, as a :class:`~settings.BuildConfig`
        object. Contains all settings defined by the user.
        """
        return self._config

    @property
    def homepage(self) -> HomePage:
        """
        The homepage parsed from the "home" directory in ``pages_dir``. This is a
        :class:`~post_types.HomePage` object containing all metadata from ``meta.yml``, the HTML
        content, and any images.
        """
        return self._homepage

    @property
    def pages(self) -> list[Page]:
        """
        A list of all pages found in ``pages_dir``, excluding the homepage. Each item is a
        :class:`~post_types.Page` object containing all metadata from ``meta.yml``, the HTML
        content, and any images.
        """
        return self._pages

    @property
    def posts(self) -> list[Post]:
        """
        A list of all posts found in ``posts_dir``. Each item is a :class:`~post_types.Post` object
        containing all metadata from ``meta.yml``, the HTML content, and any images.
        """
        return self._posts

    @property
    def archive(self) -> dict[int, list[Post]]:
        """
        A dict mapping year to a list of posts published in that year. Each post is a
        :class:`~post_types.Post` object containing all metadata from ``meta.yml``, the HTML
        content, and any images.
        """
        return self._archive

    @property
    def tags(self) -> dict[str, list[Post]]:
        """
        A dict mapping tag name to list of posts with that tag. Tags are normalized to lowercase and
        spaces are replaced with dashes. The dict is sorted by number of posts (descending) and then
        alphabetically. Each post is a :class:`~post_types.Post` object containing all metadata from
        ``meta.yml``, the HTML content, and any images.
        """
        return self._tags

    @property
    def now(self) -> datetime:
        """
        The datetime when the build process started, in UTC. Useful for displaying "last updated"
        timestamps or calculating "time since published" for posts.
        """
        return self._now
