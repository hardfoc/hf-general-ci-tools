"""Where the repository being documented is: the nearest directory, from the working directory up, with mkdocs.yml."""

from __future__ import annotations

import os
import pathlib


def repo_root() -> pathlib.Path:
    env = os.environ.get("HARDFOC_DOCS_ROOT")
    if env:
        return pathlib.Path(env).resolve()
    here = pathlib.Path.cwd().resolve()
    for d in (here, *here.parents):
        if (d / "mkdocs.yml").is_file():
            return d
    return here


SKIP_DIRS = {".git", "build", "site", "node_modules", ".venv", "venv", "third_party", "_doxygen", "lib", "external"}
