from pathlib import Path
from typing import Annotated, Optional

from typer import Option


pages_dir_opt = Annotated[Optional[Path], Option(help="Pages content directory")]
posts_dir_opt = Annotated[Optional[Path], Option(help="Posts content directory")]
static_dir_opt = Annotated[Optional[Path], Option(help="Static files directory")]
blog_root_opt = Annotated[Optional[Path], Option(help="URL path prefix for blog pages")]
logs_csv_dir_opt = Annotated[Optional[Path], Option(help="Output directory for CSV files")]
pattern_opt = Annotated[
    Optional[str], Option(help="Filename glob pattern when input is a directory")
]
analytics_csv_dir_opt = Annotated[Optional[Path], Option(help="Input CSV directory")]
templates_dir_opt = Annotated[Optional[Path], Option(help="Chameleon templates directory")]
manifest_opt = Annotated[Optional[Path], Option(help="Path to manifest.json from site build")]
output_dir_opt = Annotated[Optional[Path], Option(help="Output directory")]
base_url_opt = Annotated[Optional[str], Option(help="Site base URL e.g. https://bennuttall.com")]
title_opt = Annotated[Optional[str], Option(help="Analytics title")]
