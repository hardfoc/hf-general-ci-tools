"""``<!-- generated: examples -->``: the example applications of the repository, read from ``examples/*/app_config.yml``.

The file is the one the ESP-IDF project tools, CI and CMake read (``apps:`` with ``description``, ``source_file``,
``category``, ``ci_enabled``, ``featured``; ``metadata:`` with ``target``), so the table on the page cannot list an
app that does not build or miss one that does.
"""

from __future__ import annotations

import yaml

from hardfoc_mkdocs_theme.paths import repo_root


def _cell(s: str) -> str:
    return " ".join(str(s).split()).replace("|", "\\|")


def examples(page) -> str:
    root = repo_root()
    configs = sorted(root.glob("examples/*/app_config.yml"))
    if not configs:
        return "_No `examples/*/app_config.yml` in this repository._\n"
    out = []
    for cfg in configs:
        data = yaml.safe_load(cfg.read_text()) or {}
        meta = data.get("metadata") or {}
        apps = data.get("apps") or {}
        folder = cfg.parent.relative_to(root).as_posix()
        target = meta.get("target", "")
        if len(configs) > 1:
            out += [f"**`{folder}`**" + (f" (target `{target}`)" if target else ""), ""]
        out += ["| App | What it shows | Source | CI |", "| --- | --- | --- | --- |"]
        for name, app in apps.items():
            app = app or {}
            src = app.get("source_file", "")
            src_path = f"{folder}/main/{src}" if (root / folder / "main" / src).is_file() else f"{folder}/{src}"
            link = f"[`{src}`]({page.rel(src_path)})" if src else ""
            ci = "yes" if app.get("ci_enabled", True) else "no"
            star = " :material-star:{ title=\"featured\" }" if app.get("featured") else ""
            out.append(f"| `{name}`{star} | {_cell(app.get('description', ''))} | {link} | {ci} |")
        out.append("")
        default = meta.get("default_app") or next(iter(apps), "")
        if default:
            out += [
                f"Build and flash one (from `{folder}`, ESP-IDF environment loaded):",
                "",
                "```bash",
                f"./scripts/build_app.sh {default} Release",
                f"./scripts/flash_app.sh flash_monitor {default} Release",
                "```",
                "",
            ]
        out.append(f"Source of this table: [`{folder}/app_config.yml`]({page.rel(folder + '/app_config.yml')}).")
        out.append("")
    return "\n".join(out)


REGIONS = {"examples": examples}
