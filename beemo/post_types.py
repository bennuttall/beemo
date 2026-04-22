import re
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, ConfigDict, model_validator

from .settings import get_config
from .utils import get_excerpt, get_text


def get_build_config():
    return get_config().build


class PostType(BaseModel):
    model_config = ConfigDict(extra="allow")

    # allow access to extra fields without raising an error
    def __getattr__(self, name: str):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return None

    # given fields
    post_type: str
    slug: str | None = None
    title: str
    description: str | None = None
    html: str
    og_image: str | None = None
    template: str | None = None
    cover_image: str | None = None
    author: str | None = None
    images: list[Path] = []

    # calculated fields
    text: str | None = None
    excerpt: str | None = None
    link: Path | None = None

    @model_validator(mode="after")
    def set_text(self):
        self.text = get_text(self.html)
        return self

    @model_validator(mode="after")
    def set_excerpt(self):
        if not self.excerpt:
            self.excerpt = get_excerpt(self.text)
        self.excerpt = self.excerpt.replace("\n", " ").strip()
        return self

    @model_validator(mode="after")
    def set_description(self):
        if not self.description:
            self.description = self.excerpt
        return self

    @model_validator(mode="after")
    def validate_template(self):
        if self.template is not None:
            if self.template.endswith(".pt"):
                raise ValueError(f"Template should not include extension: {self.template}")
            template_path = get_build_config().templates_dir / f"{self.template}.pt"
            if not template_path.is_file():
                raise ValueError(f"Template not found: {self.template}")
        return self

    @property
    def output_path(self):
        return get_build_config().output_dir / self.link


class Page(PostType):
    post_type: str = "page"
    slug: str

    @model_validator(mode="after")
    def set_link(self):
        self.link = Path(self.slug)
        return self


class HomePage(Page):
    post_type: str = "page"
    slug: None = None

    @model_validator(mode="after")
    def set_link(self):
        self.link = Path()
        return self


class Post(PostType):
    # given fields
    slug: str
    published: datetime
    modified: datetime | None = None
    tags: list[str] = []

    # calculated fields
    post_type: str = "post"
    modified_diff: bool = False
    html_atom_safe: str | None = None
    link: Path | None = None

    @model_validator(mode="after")
    def set_timezone(self):
        self.published = self.published.replace(tzinfo=timezone.utc)
        return self

    @model_validator(mode="after")
    def set_link(self):
        config = get_build_config()
        post_path = Path(str(self.published.year)) / self.published.strftime("%m") / self.slug
        if config.pages_dir is None:
            self.link = post_path
        else:
            self.link = config.blog_root / post_path
        return self

    @model_validator(mode="after")
    def set_modified(self):
        if not self.modified:
            self.modified = self.published
        else:
            self.modified = self.modified.replace(tzinfo=timezone.utc)
        return self

    @model_validator(mode="after")
    def set_modified_diff(self):
        if self.modified and self.modified.date() != self.published.date():
            self.modified_diff = True
        return self

    @model_validator(mode="after")
    def validate_tags(self):
        for tag in self.tags:
            if not re.fullmatch(r"[a-z0-9-]+", tag):
                raise ValueError(f"Invalid tag: {tag}")
        return self

    @model_validator(mode="after")
    def set_html_atom_safe(self):
        html = self.html.replace("]]>", "]]&gt;")

        config = get_build_config()
        base_url = config.base_url
        if base_url is None:
            self.html_atom_safe = html
            return self

        post_url = f"{base_url}/{self.link}/"

        def make_absolute(match):
            attr, url = match.group(1), match.group(2)
            if re.match(r"https?://", url) or url.startswith("//") or url.startswith("/"):
                return match.group(0)
            if url.startswith("./"):
                url = url[2:]
            return f'{attr}="{post_url}{url}"'

        self.html_atom_safe = re.sub(r'(src|href)="([^"]*)"', make_absolute, html)
        return self
