from pathlib import Path
from typing import Annotated

from typer import Argument


gz_arg = Annotated[Path | None, Argument(help="gz file or directory of gz files")]
