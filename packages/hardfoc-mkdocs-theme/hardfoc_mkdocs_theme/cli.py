"""``hardfoc-docs``: the documentation tasks of a HardFOC repository, run from anywhere inside it.

    hardfoc-docs [-f CONFIG] COMMAND ...

    hardfoc-docs figures [--check] [ids]   build (or check) the figkit figures under docs/diagrams/figures/
    hardfoc-docs gen [--check|--list]      fill (or check) the <!-- generated: name --> regions
    hardfoc-docs check                     both checks, as CI runs them before the build
    hardfoc-docs screenshots SITE OUT      phone and desktop screenshots, light and dark, of a built site
    hardfoc-docs pages SITE                the pages CI audits: the home page and the first navigation pages
    hardfoc-docs publish-root SITE         commit SITE as the whole deployment branch (unversioned sites)

-f/--config CONFIG (before or after the command) names the site configuration, e.g. ``_config/mkdocs.yml``; the
repository root is then the folder that holds its docs_dir. Without it the nearest mkdocs.yml or _config/mkdocs.yml
from the working directory up is used.
"""

from __future__ import annotations

import os
import pathlib
import sys


def _take_config(argv: list[str]) -> tuple[list[str], str | None]:
    """Remove ``-f PATH`` / ``--config PATH`` / ``--config=PATH`` from ``argv``; return the rest and the path."""
    rest, config, i = [], None, 0
    while i < len(argv):
        a = argv[i]
        if a in ("-f", "--config"):
            if i + 1 >= len(argv):
                raise SystemExit(f"hardfoc-docs: {a} needs a path")
            config, i = argv[i + 1], i + 2
            continue
        if a.startswith("--config="):
            config = a.split("=", 1)[1]
        else:
            rest.append(a)
        i += 1
    return rest, config


def _check() -> int:
    from .paths import repo_root

    root = repo_root()
    rc = 0
    if (root / "docs/diagrams/figures").is_dir():
        from .figkit import build

        rc |= build.main(["--check"])
    from . import gen

    rc |= gen.main(["--check"])
    return rc


def main(argv: list[str] | None = None) -> int:
    argv, config = _take_config(list(sys.argv[1:] if argv is None else argv))
    if config is not None:
        path = pathlib.Path(config).resolve()
        if not path.is_file():
            print(f"hardfoc-docs: no site configuration at {config}", file=sys.stderr)
            return 2
        # Read by paths.repo_root(); the figure and region modules compute the root when they are imported, below.
        os.environ["HARDFOC_DOCS_CONFIG"] = str(path)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "figures":
        from .figkit import build

        return build.main(rest)
    if cmd == "gen":
        from . import gen

        return gen.main(rest)
    if cmd == "check":
        return _check()
    if cmd == "pages":
        from .screenshots import pages

        print("\n".join(pages(pathlib.Path(rest[0]))))
        return 0
    if cmd == "publish-root":
        from . import publish

        return publish.main(rest)
    if cmd == "screenshots":
        from . import screenshots

        return screenshots.main(rest)
    print(f"hardfoc-docs: unknown command {cmd!r}\n{__doc__}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
