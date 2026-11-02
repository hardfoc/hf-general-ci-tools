"""hardfoc-docs screenshots: page selection, and main() without --page (it used to shadow pages())."""

from __future__ import annotations

import contextlib
import pathlib
import sys
import tempfile
import types
import unittest
from unittest import mock

from hardfoc_mkdocs_theme import screenshots


class FakePage:
    def __init__(self, log):
        self.log = log

    def goto(self, url, **_):
        self.log.append(url)

    def wait_for_timeout(self, _):
        pass

    def screenshot(self, path, **_):
        pathlib.Path(path).write_bytes(b"png")


class FakeBrowser:
    def __init__(self, log):
        self.log = log

    def new_context(self, **_):
        log = self.log
        return types.SimpleNamespace(new_page=lambda: FakePage(log), close=lambda: None)

    def close(self):
        pass


def fake_playwright(log):
    @contextlib.contextmanager
    def sync_playwright():
        yield types.SimpleNamespace(chromium=types.SimpleNamespace(launch=lambda: FakeBrowser(log)))

    mod = types.ModuleType("playwright.sync_api")
    mod.sync_playwright = sync_playwright
    return {"playwright": types.ModuleType("playwright"), "playwright.sync_api": mod}


class ScreenshotsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.site = pathlib.Path(self.tmp.name) / "site"
        for p in ("quickstart", "hardware", "porting"):
            (self.site / p).mkdir(parents=True)
            (self.site / p / "index.html").write_text("x")
        links = "".join(f'<a href="{p}/" class="md-nav__link">{p}</a>' for p in ("quickstart", "hardware", "porting"))
        (self.site / "index.html").write_text(f'<a href="https://x.org/" class="md-nav__link">x</a>{links}')

    def tearDown(self):
        self.tmp.cleanup()

    def test_pages_takes_home_and_first_two(self):
        self.assertEqual(screenshots.pages(self.site), ["index.html", "quickstart/index.html", "hardware/index.html"])

    def test_main_without_page_uses_the_default_pages(self):
        log: list[str] = []
        out = pathlib.Path(self.tmp.name) / "out"
        with mock.patch.dict(sys.modules, fake_playwright(log)):
            self.assertEqual(screenshots.main([str(self.site), str(out)]), 0)
        self.assertEqual(len(list(out.glob("*.png"))), 3 * 4)  # three pages, phone/desktop x light/dark
        self.assertTrue(any(u.endswith("/quickstart/index.html") for u in log))


if __name__ == "__main__":
    unittest.main()
