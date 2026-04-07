from functools import cache
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, FilePath, model_validator
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
    logs_dir: Path = Path("apache2")
    csv_dir: Path = Path("csv")
    pattern: str = "*.gz"


class ReportConfig(BaseModel):
    csv_dir: Path = Path("csv")
    output: Path = Path("html/summary.html")
    base_url: str = ""
    title: str = ""


class Config(BaseModel):
    root_path: Path
    build: BuildConfig | None = None
    logs: LogsConfig = Field(default_factory=LogsConfig)
    report: ReportConfig = Field(default_factory=ReportConfig)

    @model_validator(mode="after")
    def resolve_paths(self):
        root = self.root_path
        if self.build:
            b = self.build
            for attr in ("pages_dir", "posts_dir", "static_dir", "templates_dir", "output_dir"):
                p = getattr(b, attr)
                if p is not None and not p.is_absolute():
                    setattr(b, attr, root / p)
        for attr in ("logs_dir", "csv_dir"):
            p = getattr(self.logs, attr)
            if not p.is_absolute():
                setattr(self.logs, attr, root / p)
        for attr in ("csv_dir", "output"):
            p = getattr(self.report, attr)
            if not p.is_absolute():
                setattr(self.report, attr, root / p)
        return self


@cache
def get_config() -> Config:
    settings = Settings()
    with open(settings.config, "r") as f:
        config = yaml.safe_load(f)
    config["root_path"] = settings.config.parent.absolute()
    return Config.model_validate(config)
