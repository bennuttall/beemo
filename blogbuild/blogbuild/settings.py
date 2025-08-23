from functools import cache

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="blog_")

    output_dir: DirectoryPath
    content_dir: DirectoryPath


@cache
def get_settings() -> Settings:
    return Settings()
