"""Where the repository being documented is.

The repository root is the folder that holds the site's ``docs_dir``. With ``mkdocs.yml`` at the root (the default
``docs_dir: docs``) that is the folder of ``mkdocs.yml``; with the configuration in a tool folder, for example
``_config/mkdocs.yml`` with ``docs_dir: ../docs``, it is the parent of that folder.

How the configuration is found, first match wins:

1. ``HARDFOC_DOCS_ROOT``: the root itself.
2. ``HARDFOC_DOCS_CONFIG`` (set by ``hardfoc-docs -f PATH``): the root of that configuration.
3. From the working directory up, the nearest folder with ``mkdocs.yml`` or ``_config/mkdocs.yml``.
"""

from __future__ import annotations

import os
import pathlib
import re

CONFIG_NAMES = ("mkdocs.yml", "_config/mkdocs.yml")
"""Where a repository keeps its site configuration, relative to the repository root."""

_DOCS_DIR = re.compile(r"^docs_dir\s*:\s*(?P<v>[^#\n]*?)\s*(?:#.*)?$", re.M)


def docs_dir_of(config: pathlib.Path) -> pathlib.Path:
    """The ``docs_dir`` a configuration file names (MkDocs' default ``docs``), resolved against its folder."""
    value = "docs"
    try:
        m = _DOCS_DIR.search(config.read_text())
    except OSError:
        m = None
    if m and m.group("v"):
        value = m.group("v").strip("'\"")
    return (config.parent / value).resolve()


def root_of(config_dir: pathlib.Path, docs_dir: pathlib.Path) -> pathlib.Path:
    """The repository root for a configuration in ``config_dir`` whose pages are in ``docs_dir``.

    The folder of the configuration when ``docs_dir`` lies inside it (``mkdocs.yml`` at the root), otherwise the
    folder that holds ``docs_dir`` (``_config/mkdocs.yml`` with ``docs_dir: ../docs``).
    """
    config_dir, docs_dir = config_dir.resolve(), docs_dir.resolve()
    if config_dir in docs_dir.parents:
        return config_dir
    return docs_dir.parent


def root_of_config(config: pathlib.Path) -> pathlib.Path:
    config = config.resolve()
    return root_of(config.parent, docs_dir_of(config))


def config_path() -> pathlib.Path | None:
    """The site configuration in use, or None when there is none."""
    env = os.environ.get("HARDFOC_DOCS_CONFIG")
    if env:
        return pathlib.Path(env).resolve()
    here = pathlib.Path.cwd().resolve()
    for d in (here, *here.parents):
        for name in CONFIG_NAMES:
            if (d / name).is_file():
                return d / name
    return None


def repo_root() -> pathlib.Path:
    env = os.environ.get("HARDFOC_DOCS_ROOT")
    if env:
        return pathlib.Path(env).resolve()
    config = config_path()
    if config is not None:
        return root_of_config(config)
    return pathlib.Path.cwd().resolve()


def is_site_root(folder: pathlib.Path) -> bool:
    """True when ``folder`` has its own site configuration (another site, e.g. a template or a fixture)."""
    return any((folder / name).is_file() for name in CONFIG_NAMES)


SKIP_DIRS = {".git", "build", "site", "node_modules", ".venv", "venv", "third_party", "_doxygen", "lib", "external"}
