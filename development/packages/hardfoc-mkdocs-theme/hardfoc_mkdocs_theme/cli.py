"""``hardfoc-docs``: the documentation tasks of a HardFOC repository, run from anywhere inside it.

    hardfoc-docs figures [--check] [ids]   build (or check) the figkit figures under docs/diagrams/figures/
    hardfoc-docs gen [--check|--list]      fill (or check) the <!-- generated: name --> regions
    hardfoc-docs check                     both checks, as CI runs them before the build
    hardfoc-docs screenshots SITE OUT      phone and desktop screenshots, light and dark, of a built site
    hardfoc-docs pages SITE                the pages CI audits: the home page and the first navigation pages
"""

from __future__ import annotations

import sys


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
    argv = list(sys.argv[1:] if argv is None else argv)
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
        import pathlib

        from .screenshots import pages

        print("\n".join(pages(pathlib.Path(rest[0]))))
        return 0
    if cmd == "screenshots":
        from . import screenshots

        return screenshots.main(rest)
    print(f"hardfoc-docs: unknown command {cmd!r}\n{__doc__}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
