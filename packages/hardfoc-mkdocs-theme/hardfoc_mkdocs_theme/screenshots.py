"""Screenshots of a built site at phone (375 px) and desktop (1280 px) widths, light and dark.

    hardfoc-docs screenshots SITE_DIR OUT_DIR [--page index.html --page quickstart/index.html ...]

Serves SITE_DIR on a local port, opens each page in Chromium (Playwright, ``pip install
hardfoc-mkdocs-theme[screenshots]`` then ``playwright install chromium``) and writes
``OUT_DIR/<page>-<phone|desktop>-<light|dark>.png`` (full page). Without --page it takes the home page and the first
two pages of the navigation.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import pathlib
import re
import threading

SIZES = {"phone": (375, 812), "desktop": (1280, 800)}


def pages(site: pathlib.Path) -> list[str]:
    home = (site / "index.html").read_text(errors="replace")
    links = re.findall(r'class="md-nav__link"[^>]*href="([^"#]+)"|href="([^"#]+)"[^>]*class="md-nav__link"', home)
    out = ["index.html"]
    for a, b in links:
        href = (a or b).strip()
        if href.startswith(("http", "/", "..")) or href in (".", "./"):
            continue
        page = href.rstrip("/") + "/index.html" if not href.endswith(".html") else href
        page = page.removeprefix("./")
        if page not in out and (site / page).is_file():
            out.append(page)
        if len(out) >= 3:
            break
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="hardfoc-docs screenshots", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", type=pathlib.Path)
    ap.add_argument("out", type=pathlib.Path)
    ap.add_argument("--page", action="append", default=[])
    ap.add_argument("--viewport-only", action="store_true", help="the first screen only, not the full page")
    args = ap.parse_args(argv)

    from playwright.sync_api import sync_playwright

    site = args.site.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):
            pass

    handler = functools.partial(Quiet, directory=str(site))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}/"
    targets = args.page or pages(site)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for name, (w, h) in SIZES.items():
                for scheme in ("light", "dark"):
                    ctx = browser.new_context(viewport={"width": w, "height": h}, color_scheme=scheme,
                                              device_scale_factor=2 if name == "phone" else 1,
                                              is_mobile=name == "phone", has_touch=name == "phone")
                    page = ctx.new_page()
                    for path in targets:
                        page.goto(base + path, wait_until="networkidle")
                        page.wait_for_timeout(300)
                        slug = path.removesuffix("index.html").strip("/").replace("/", "-") or "home"
                        target = args.out / f"{slug}-{name}-{scheme}.png"
                        page.screenshot(path=str(target), full_page=not args.viewport_only)
                        print(f"  wrote {target}")
                    ctx.close()
            browser.close()
    finally:
        server.shutdown()
    return 0
