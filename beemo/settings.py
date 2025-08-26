from functools import cache
from pathlib import Path

from pydantic import DirectoryPath, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="beemo_")

    pages_dir: DirectoryPath | None = None
    posts_dir: DirectoryPath | None = None
    static_dir: DirectoryPath
    templates_dir: DirectoryPath
    output_dir: DirectoryPath
    blog_root: str | None = None

    @field_validator("blog_root", mode="after")
    @classmethod
    def set_blog_root(cls, value):
        if value is None:
            return Path()
        return Path(value)


@cache
def get_settings() -> Settings:
    return Settings()
