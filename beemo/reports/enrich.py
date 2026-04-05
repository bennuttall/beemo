import json
from pathlib import Path


class Manifest:
    def __init__(self, manifest_path: Path):
        entries = json.loads(manifest_path.read_text())
        self._pages = {e["url"]: e for e in entries}

    def get(self, url_path: str) -> dict | None:
        """Look up a URL path, trying with and without trailing slash."""
        return (
            self._pages.get(url_path)
            or self._pages.get(url_path.rstrip("/") + "/")
            or self._pages.get(url_path.rstrip("/"))
        )
