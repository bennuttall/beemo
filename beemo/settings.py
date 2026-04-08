from functools import cache
from pathlib import Path

import yaml
from pydantic import BaseModel, FilePath, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="beemo_")

    config: FilePath


class BuildConfig(BaseModel):
    pages_dir: Path | None = None
    posts_dir: Path | None = None
    static_dir: Path
    templates_dir: Path
    output_dir: Path
    blog_root: Path = Path()

    @model_validator(mode="after")
    def posts_or_pages_required(self):
        if self.posts_dir is None and self.pages_dir is None:
            raise ValueError("build: either posts_dir or pages_dir must be set")
        return self


class LogsConfig(BaseModel):
    logs_dir: Path
    csv_dir: Path
    pattern: str = "*.gz"


class AnalyticsConfig(BaseModel):
    csv_dir: Path
    output_dir: Path
    templates_dir: Path
    base_url: str = ""
    title: str = ""


class Config(BaseModel):
    root_path: Path
    build: BuildConfig | None = None
    logs: LogsConfig | None = None
    analytics: AnalyticsConfig | None = None

    @model_validator(mode="after")
    def resolve_paths(self):
        root = self.root_path
        if self.build:
            for attr in ("pages_dir", "posts_dir", "static_dir", "templates_dir", "output_dir"):
                p = getattr(self.build, attr)
                if p is not None and not p.is_absolute():
                    setattr(self.build, attr, root / p)
        if self.logs:
            for attr in ("logs_dir", "csv_dir"):
                p = getattr(self.logs, attr)
                if not p.is_absolute():
                    setattr(self.logs, attr, root / p)
        if self.analytics:
            for attr in ("csv_dir", "output_dir", "templates_dir"):
                p = getattr(self.analytics, attr)
                if not p.is_absolute():
                    setattr(self.analytics, attr, root / p)
        return self


@cache
def get_config() -> Config:
    settings = Settings()
    with open(settings.config, "r") as f:
        config = yaml.safe_load(f)
    config["root_path"] = settings.config.parent.absolute()

    # Merge top-level keys into sub-sections as defaults (sub-section values take precedence)
    known_keys = {"root_path", "build", "logs", "analytics"}
    top_level_defaults = {k: v for k, v in config.items() if k not in known_keys}
    for key in top_level_defaults:
        del config[key]
    for section in ("build", "logs", "analytics"):
        if config.get(section):
            for key, value in top_level_defaults.items():
                config[section].setdefault(key, value)

    return Config.model_validate(config)
