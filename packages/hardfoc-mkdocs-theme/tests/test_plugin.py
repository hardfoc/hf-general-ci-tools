"""The plugin's versioning switch: site_url and the version selector of versioned and unversioned sites."""

from __future__ import annotations

import os
import pathlib
import re
import tempfile
import unittest
from unittest import mock

from mkdocs.commands.build import build
from mkdocs.config import load_config

from hardfoc_mkdocs_theme.plugin import versioned_setting

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"


def built(name: str, env: dict | None = None) -> tuple[object, pathlib.Path, tempfile.TemporaryDirectory]:
    tmp = tempfile.TemporaryDirectory()
    with mock.patch.dict(os.environ, env or {}, clear=False):
        cfg = load_config(str(FIXTURES / name / "mkdocs.yml"), site_dir=tmp.name, strict=True)
        cfg.plugins.on_startup(command="build", dirty=False)
        build(cfg)
    return cfg, pathlib.Path(tmp.name), tmp


class VersionedSettingTest(unittest.TestCase):
    def test_precedence(self):
        with mock.patch.dict(os.environ, {"HARDFOC_DOCS_VERSIONED": ""}):
            self.assertTrue(versioned_setting(None, org_site=False))
            self.assertFalse(versioned_setting(None, org_site=True))
            self.assertTrue(versioned_setting(True, org_site=True))
            self.assertFalse(versioned_setting(False, org_site=False))
        with mock.patch.dict(os.environ, {"HARDFOC_DOCS_VERSIONED": "false"}):
            self.assertFalse(versioned_setting(True, org_site=False))
        with mock.patch.dict(os.environ, {"HARDFOC_DOCS_VERSIONED": "true"}):
            self.assertTrue(versioned_setting(False, org_site=True))


class SiteTest(unittest.TestCase):
    def test_org_site_is_unversioned(self):
        cfg, site, tmp = built("org-site", {"HARDFOC_DOCS_VERSIONED": ""})
        with tmp:
            self.assertEqual(cfg.site_url, "https://hardfoc.github.io/")
            self.assertNotIn("version", cfg.extra)
            self.assertIn("<loc>https://hardfoc.github.io/</loc>", (site / "sitemap.xml").read_text())
            self.assertNotIn("/latest/", (site / "index.html").read_text())

    def test_repo_site_is_versioned(self):
        cfg, site, tmp = built("repo-site", {"HARDFOC_DOCS_VERSIONED": ""})
        with tmp:
            self.assertEqual(cfg.site_url, "https://hardfoc.github.io/hf-example/latest/")
            self.assertEqual(cfg.extra["version"]["provider"], "mike")

    def test_workflow_switch_unversions_a_repo_site(self):
        cfg, site, tmp = built("repo-site", {"HARDFOC_DOCS_VERSIONED": "false"})
        with tmp:
            self.assertEqual(cfg.site_url, "https://hardfoc.github.io/hf-example/")
            self.assertNotIn("version", cfg.extra)


class RepositoryLinkTest(unittest.TestCase):
    """A link from docs/ to a repository file becomes a GitHub link; one to a file that does not exist fails."""

    def build_with(self, body: str):
        tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(tmp.name)
        (root / "docs").mkdir()
        (root / "inc").mkdir()
        (root / "inc/x.hpp").write_text("// x\n")
        (root / "lib/sub").mkdir(parents=True)  # a submodule that is not checked out: an empty folder
        (root / "mkdocs.yml").write_text((FIXTURES / "repo-site/mkdocs.yml").read_text())
        (root / "docs/index.md").write_text(f"# Home\n\n{body}\n")
        cfg = load_config(str(root / "mkdocs.yml"), site_dir=str(root / "site"), strict=True)
        cfg.plugins.on_startup(command="build", dirty=False)
        with tmp:
            build(cfg)
            return (root / "site/index.html").read_text()

    def test_existing_file_and_unchecked_submodule(self):
        out = self.build_with("[x](../inc/x.hpp) and [sub](../lib/sub/README.md)")
        self.assertIn("https://github.com/hardfoc/hf-example/blob/", out)

    def test_examples_in_code_are_left_alone(self):
        out = self.build_with("Write ``[`x.hpp`](../inc/missing.hpp)`` and `<!-- figure: id -->`; "
                              "[`x.hpp`](../inc/x.hpp) is a link.")
        self.assertIn("../inc/missing.hpp", out)
        self.assertIn("https://github.com/hardfoc/hf-example/blob/", out)

    def test_brackets_in_link_text(self):
        out = self.build_with("[`kTable[]`](../inc/x.hpp) and [a [b] c](../inc/x.hpp)")
        self.assertEqual(out.count("/inc/x.hpp\""), 2)
        self.assertNotIn("../inc/x.hpp", out)

    def test_missing_file_fails_strict(self):
        from mkdocs.exceptions import Abort

        with self.assertRaises(Abort):
            self.build_with("[gone](../quickstart.md)")


class Root404Test(unittest.TestCase):
    """The page GitHub Pages serves for a missing path of a versioned site, before it redirects."""

    page = (pathlib.Path(__file__).resolve().parents[1] / "hardfoc_mkdocs_theme/theme/root-404.html").read_text()

    def test_branded_and_self_contained(self):
        self.assertIn("Redirecting to the latest documentation", self.page)
        self.assertIn('<html lang="en" class="hf-pending">', self.page)
        self.assertIn("prefers-color-scheme: dark", self.page)
        self.assertIn("M35.74 14.39", self.page)  # the HardFOC mark, inline
        stylesheets = re.findall(r'<link rel="stylesheet" href="([^"]+)"', self.page)
        self.assertTrue(all(h.startswith("https://fonts.googleapis.com/") for h in stylesheets), stylesheets)
        self.assertNotRegex(self.page, r"<script[^>]+src=")

    def test_not_found_waits_for_the_redirect_decision(self):
        # Hidden while pending; revealed by the script, after two seconds at the latest, or without JavaScript.
        self.assertIn(".hf-pending #missing", self.page)
        self.assertIn("setTimeout(missing, 2000)", self.page)
        self.assertIn("<noscript>", self.page)


if __name__ == "__main__":
    unittest.main()
