import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator

import yaml
from chameleon import PageTemplateLoader
from structlog import get_logger

from .post_types import HomePage, Page, Post
from .settings import BuildConfig, get_config
from .utils import markdown_to_html, next_current_prev, rst_to_html


logger = get_logger()


class SiteData:
    def __init__(self, scribe: "TheScribe"):
        self.config: BuildConfig = scribe.config
        self.pages: list[Page] = scribe.pages
        self.posts: list[Post] = scribe.posts
        self.archive: dict[int, list[Post]] = scribe.archive
        self.tags: dict[str, list[Post]] = scribe.tags
        self.now: datetime = scribe.now


class TheScribe:
    def __init__(self):
        self.now = datetime.now(timezone.utc)
        self.config = get_config().build
        self.output_path = self.config.output_dir
        self.templates = PageTemplateLoader(
            search_path=[self.config.templates_dir],
            default_extension=".pt",
        )
        self.pages = list(self.iter_pages())
        self.posts = sorted(self.iter_posts(), key=lambda p: p.published, reverse=True)
        self.archive = self.get_archive()
        self.tags = self.get_tags()
        self.site_data = SiteData(self)

    def setup_output_path(self):
        logger.info("Setting up output path", output_path=str(self.output_path))
        shutil.rmtree(self.output_path, ignore_errors=True)
        self.output_path.mkdir(parents=True, exist_ok=True)

        for source_path in self.config.static_dir.rglob("*"):
            if source_path.is_file():
                relative_path = source_path.relative_to(self.config.static_dir)
                destination_path = self.output_path / relative_path
                destination_path.parent.mkdir(parents=True, exist_ok=True)

                logger.info(
                    "Copying static file",
                    src=str(source_path),
                    dest=str(destination_path),
                )
                shutil.copy2(source_path, destination_path)

    def iter_pages(self) -> Generator[Page, None, None]:
        if not self.config.pages_dir:
            return
        for page_dir in self.config.pages_dir.iterdir():
            if page_dir.stem != "home":
                page_data = self.parse_content(page_dir)
                yield validate_page(page_data, src_dir=page_dir)

    def iter_posts(self) -> Generator[Post, None, None]:
        if not self.config.posts_dir:
            return
        for meta_file in self.config.posts_dir.rglob("meta.yml"):
            post_dir = meta_file.parent
            post_data = self.parse_content(post_dir)
            yield validate_post(post_data, src_dir=post_dir)

    def parse_content(self, src_dir: Path) -> dict[str]:
        metadata_file = src_dir / "meta.yml"
        images_dir = src_dir / "images"
        html_file = src_dir / "index.html"
        md_file = src_dir / "index.md"
        rst_file = src_dir / "index.rst"

        if html_file.exists():
            html = html_file.read_text(encoding="utf-8")
        elif md_file.exists():
            html = markdown_to_html(md_file.read_text(encoding="utf-8"))
        elif rst_file.exists():
            html = rst_to_html(rst_file.read_text(encoding="utf-8"))
        else:
            logger.warning("No content file found", src_dir=str(src_dir))
            raise FileNotFoundError("No content file found")

        metadata = yaml.safe_load(metadata_file.read_text(encoding="utf-8"))

        if images_dir.exists() and images_dir.is_dir():
            images = [img for img in images_dir.iterdir() if img.is_file()]
        else:
            images = []

        return {"html": html, "images": images, "slug": src_dir.name, **metadata}

    def get_tags(self) -> dict[str, list[Post]]:
        tags = defaultdict(list)
        for post in self.posts:
            for tag in post.tags:
                tags[tag].append(post)
        # Sort tags by number of posts (descending) and then alphabetically
        return dict(sorted(tags.items(), key=lambda item: (-len(item[1]), item[0])))

    def get_homepage(self) -> HomePage:
        homepage_dir = self.config.pages_dir / "home"
        page_data = self.parse_content(homepage_dir)
        return validate_homepage(page_data, src_dir=homepage_dir)

    def get_archive(self) -> dict[int, list[Post]]:
        archive = defaultdict(list)

        for post in self.posts:
            year = post.published.year
            archive[year].append(post)

        return dict(archive)

    def write_homepage(self):
        """
        Render and write index.html using the home template.
        """
        logger.info("Writing homepage")
        homepage = self.get_homepage()
        html = self.templates["home"](
            layout=self.templates["layout"]["layout"],
            site=self.site_data,
            page=homepage,
            post=None,
        )
        output_path = self.output_path / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)

    def write_pages(self):
        logger.info("Writing pages", len=len(self.pages))
        for page in self.pages:
            template = page.template or "page"
            logger.info("Writing page", output_path=str(page.output_path), template=template)
            page.output_path.mkdir(parents=True, exist_ok=True)
            html = self.templates[template](
                layout=self.templates["layout"]["layout"],
                site=self.site_data,
                page=page,
                post=None,
            )
            html_path = page.output_path / "index.html"
            html_path.write_text(html)
            if page.images:
                img_dir = page.output_path / "images"
                img_dir.mkdir(parents=True, exist_ok=True)
                for img in page.images:
                    img_dest = img_dir / img.name
                    shutil.copy(img, img_dest)
                    logger.info("Copied image", path=str(img_dest))

    def write_posts(self):
        logger.info("Writing posts", len=len(self.posts))
        for next_post, post, prev_post in next_current_prev(self.posts):
            template = post.template or "post"
            logger.info("Writing post", output_path=str(post.output_path), template=template)
            post.output_path.mkdir(parents=True, exist_ok=True)
            html = self.templates[template](
                layout=self.templates["layout"]["layout"],
                site=self.site_data,
                post=post,
                prev_post=prev_post,
                next_post=next_post,
                page=None,
            )
            html_path = post.output_path / "index.html"
            html_path.write_text(html)
            if post.images:
                img_dir = post.output_path / "images"
                img_dir.mkdir(parents=True, exist_ok=True)
                for img in post.images:
                    img_dest = img_dir / img.name
                    shutil.copy(img, img_dest)
                    logger.info("Copied image", path=str(img_dest))

    def write_blog_index(self):
        """
        Render and write the blog index page using blog.pt or posts.pt.
        """
        link = self.config.blog_root
        logger.info("Writing blog index", link=str(link))
        blog_template = self.config.templates_dir / "blog.pt"
        template = "blog" if blog_template.exists() else "posts"
        html = self.templates[template](
            layout=self.templates["layout"]["layout"],
            site=self.site_data,
            title="Blog",
            link=link,
            page=None,
            post=None,
        )
        output_path = self.output_path / link / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)

    def write_year_indexes(self):
        logger.info("Writing year indexes")
        years = defaultdict(list)
        for post in self.posts:
            year = post.published.strftime("%Y")
            years[year].append(post)
        for year, posts in years.items():
            link = self.config.blog_root / year
            logger.info("Writing year index", year=year, post_count=len(posts), link=str(link))
            html = self.templates["posts"](
                layout=self.templates["layout"]["layout"],
                site=self.site_data,
                title=f"Archive: {year}",
                link=link,
                posts=posts,
                page=None,
                post=None,
            )
            output_path = self.output_path / link / "index.html"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html)

    def write_month_indexes(self):
        logger.info("Writing month indexes")
        months = defaultdict(list)
        for post in self.posts:
            year = post.published.strftime("%Y")
            month = post.published.strftime("%m")
            month_name = post.published.strftime("%B")
            months[(year, month, month_name)].append(post)
        for (year, month, month_name), posts in months.items():
            link = self.config.blog_root / year / month
            logger.info(
                "Writing month index", year=year, month=month, post_count=len(posts), link=str(link)
            )
            html = self.templates["posts"](
                layout=self.templates["layout"]["layout"],
                site=self.site_data,
                title=f"Archive: {month_name} {year}",
                link=link,
                posts=posts,
                page=None,
                post=None,
            )
            output_path = self.output_path / link / "index.html"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html)

    def write_tags_index(self):
        """
        Render and write the tags index page listing all tags.
        """
        link = self.config.blog_root / "tags"
        logger.info("Writing tags index", len=len(self.tags), link=str(link))
        html = self.templates["tags"](
            layout=self.templates["layout"]["layout"],
            title="Tags",
            link=link,
            site=self.site_data,
            page=None,
            post=None,
        )
        output_path = self.output_path / link / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)

    def write_tag_pages(self):
        logger.info("Writing tag pages", len=len(self.tags))
        for tag, posts in self.tags.items():
            link = self.config.blog_root / "tags" / tag
            logger.info("Writing tag page", tag=tag, post_count=len(posts), link=str(link))
            tag_str = tag.replace("-", " ")
            html = self.templates["posts"](
                layout=self.templates["layout"]["layout"],
                site=self.site_data,
                posts=posts,
                title=f"Tag: {tag_str}",
                link=link,
                page=None,
                post=None,
            )
            output_path = self.output_path / link / "index.html"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html)

    def write_archive_page(self):
        """
        Render and write the full blog archive page.
        """
        link = self.config.blog_root / "archive"
        logger.info("Writing archive page")
        html = self.templates["archive"](
            layout=self.templates["layout"]["layout"],
            site=self.site_data,
            title="Blog archive",
            link=link,
            page=None,
            post=None,
        )
        output_path = self.output_path / link / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)

    def write_sitemap(self):
        """
        Render and write sitemap.xml.
        """
        logger.info("Writing sitemap")
        years = {post.published.year for post in self.posts}
        months = {(post.published.year, post.published.strftime("%m")) for post in self.posts}
        html = self.templates["sitemap"](
            site=self.site_data,
            years=years,
            months=months,
            page=None,
            post=None,
        )
        output_path = self.output_path / "sitemap.xml"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)

    def write_atom_feed(self):
        """
        Render and write the Atom feed.
        """
        logger.info("Writing atom feed")
        html = self.templates["atom"](
            site=self.site_data,
            page=None,
            post=None,
        )
        output_path = self.output_path / self.config.blog_root / "atom.xml"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)

    def write_json(self):
        logger.info("Writing json")
        data = {
            "posts": [
                {
                    "title": post.title,
                    "link": str(post.link),
                    "published": post.published.isoformat(),
                }
                for post in self.posts
            ],
        }
        output_path = self.output_path / "posts.json"
        output_path.write_text(json.dumps(data, indent=4))

    def get_manifest_entries(self) -> list[dict]:
        entries = []

        def url(link: Path) -> str:
            s = str(link)
            return "/" if s == "." else f"/{s}/"

        if self.config.pages_dir is not None:
            homepage = self.get_homepage()
            entries.append({"url": "/", "title": homepage.title, "type": "page"})
            for page in self.pages:
                entries.append({"url": url(page.link), "title": page.title, "type": "page"})

        if self.config.posts_dir is not None:
            for post in self.posts:
                entries.append(
                    {
                        "url": url(post.link),
                        "title": post.title,
                        "type": "post",
                        "published": post.published.date().isoformat(),
                        "tags": post.tags,
                    }
                )

            blog = self.config.blog_root
            entries.append({"url": url(blog), "title": "Blog", "type": "index"})
            entries.append(
                {"url": url(blog / "archive"), "title": "Blog archive", "type": "archive"}
            )
            entries.append({"url": url(blog / "tags"), "title": "Tags", "type": "index"})

            for tag in self.tags:
                tag_str = tag.replace("-", " ")
                entries.append({"url": url(blog / "tags" / tag), "title": tag_str, "type": "tag"})

            years: dict = defaultdict(list)
            months: dict = defaultdict(list)
            for post in self.posts:
                y = post.published.strftime("%Y")
                m = post.published.strftime("%m")
                years[y].append(post)
                months[(y, m)].append(post)

            for y in years:
                entries.append({"url": url(blog / y), "title": f"Archive: {y}", "type": "archive"})
            for y, m in months:
                month_name = datetime.strptime(m, "%m").strftime("%B")
                entries.append(
                    {
                        "url": url(blog / y / m),
                        "title": f"Archive: {month_name} {y}",
                        "type": "archive",
                    }
                )

        return entries

    def write_manifest(self):
        logger.info("Writing manifest")
        output_path = self.output_path / "manifest.json"
        output_path.write_text(json.dumps(self.get_manifest_entries(), indent=4))

    def build_site(self):
        logger.info("Starting build process", output_dir=str(self.output_path))

        self.setup_output_path()
        if self.config.pages_dir is not None:
            self.write_homepage()
            self.write_pages()
        if self.config.posts_dir is not None:
            self.write_posts()
            self.write_blog_index()
            self.write_year_indexes()
            self.write_month_indexes()
            self.write_tags_index()
            self.write_tag_pages()
            self.write_archive_page()
            self.write_atom_feed()
            self.write_json()
        self.write_sitemap()
        self.write_manifest()


def validate_post(post_data: dict[str], src_dir: Path) -> Post:
    try:
        return Post.model_validate(post_data)
    except Exception as exc:
        logger.error("Failed to validate post", src_dir=str(src_dir))
        print(exc)
        sys.exit(1)


def validate_page(page_data: dict[str], src_dir: Path) -> Page:
    try:
        return Page.model_validate(page_data)
    except Exception as exc:
        logger.error("Failed to validate page", src_dir=str(src_dir))
        print(exc)
        sys.exit(1)


def validate_homepage(page_data: dict[str], src_dir: Path) -> HomePage:
    page_data.pop("slug", None)
    try:
        return HomePage.model_validate(page_data)
    except Exception as exc:
        logger.error("Failed to validate homepage", src_dir=str(src_dir))
        print(exc)
        sys.exit(1)


def main():
    TheScribe.build_site()
