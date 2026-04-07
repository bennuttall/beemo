from functools import cache
from pathlib import Path

import yaml
from pydantic import (
    BaseModel,
    DirectoryPath,
    Field,
    FilePath,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="beemo_")

    config: FilePath


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
    root_path: DirectoryPath
    pages_dir: DirectoryPath | None = None
    posts_dir: DirectoryPath | None = None
    static_dir: DirectoryPath
    templates_dir: DirectoryPath
    output_dir: DirectoryPath
    blog_root: Path = Path()
    logs: LogsConfig = Field(default_factory=LogsConfig)
    report: ReportConfig = Field(default_factory=ReportConfig)

    @field_validator(
        "pages_dir",
        "posts_dir",
        "static_dir",
        "templates_dir",
        "output_dir",
        mode="before",
    )
    @classmethod
    def make_relative(cls, value, info):
        if isinstance(value, str) and not Path(value).is_absolute():
            return info.data["root_path"] / value
        return value

    @model_validator(mode="after")
    def posts_or_pages_mode(self):
        if self.posts_dir is None and self.pages_dir is None:
            raise ValueError("Either posts_dir or pages_dir must be set")
        return self

    @model_validator(mode="after")
    def resolve_logs_report_paths(self):
        root = self.root_path
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
