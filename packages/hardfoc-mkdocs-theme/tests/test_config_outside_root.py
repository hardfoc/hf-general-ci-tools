"""A site whose configuration is not at the repository root: ``_config/mkdocs.yml`` with ``docs_dir: ../docs``.

The repository root is the folder that holds docs_dir, so snippets, repository links, figures and ``hardfoc-docs``
behave exactly as with ``mkdocs.yml`` at the root.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from mkdocs.commands.build import build
from mkdocs.config import load_config

from hardfoc_mkdocs_theme import cli, paths

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"
SITE = (FIXTURES / "repo-site/mkdocs.yml").read_text()


def make_repo(root: pathlib.Path, body: str = "", where: str = "_config") -> pathlib.Path:
    (root / "docs").mkdir(parents=True)
    (root / "inc").mkdir()
    (root / "inc/x.hpp").write_text("// x\n")
    (root / "tests/docs").mkdir(parents=True)
    (root / "tests/docs/snippet.cpp").write_text("int before;\n// --8<-- [start:part]\nint snippet_body = 42;\n"
                                                 "// --8<-- [end:part]\n")
    (root / "docs/index.md").write_text(f"# Home\n\n{body}\n")
    if where == "_config":
        (root / "_config").mkdir()
        config = root / "_config/mkdocs.yml"
        config.write_text(SITE + "docs_dir: ../docs\nsite_dir: ../site\n")
    else:
        config = root / "mkdocs.yml"
        config.write_text(SITE)
    return config


class RootTest(unittest.TestCase):
    def test_root_of(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp).resolve()
            self.assertEqual(paths.root_of_config(make_repo(root)), root)
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp).resolve()
            self.assertEqual(paths.root_of_config(make_repo(root, where="root")), root)

    def test_docs_dir_quoted_and_commented(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp).resolve()
            (root / "_config").mkdir()
            cfg = root / "_config/mkdocs.yml"
            cfg.write_text("site_name: x\ndocs_dir: '../docs'  # the pages\n")
            self.assertEqual(paths.docs_dir_of(cfg), root / "docs")
            cfg.write_text("site_name: x\n")
            self.assertEqual(paths.docs_dir_of(cfg), root / "_config/docs")

    def test_found_from_anywhere_in_the_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp).resolve()
            make_repo(root)
            for cwd in (root, root / "docs", root / "_config", root / "tests/docs"):
                with mock.patch.dict(os.environ, {"HARDFOC_DOCS_ROOT": "", "HARDFOC_DOCS_CONFIG": ""}):
                    os.environ.pop("HARDFOC_DOCS_ROOT")
                    os.environ.pop("HARDFOC_DOCS_CONFIG")
                    old = os.getcwd()
                    os.chdir(cwd)
                    try:
                        self.assertEqual(paths.repo_root(), root, cwd)
                    finally:
                        os.chdir(old)

    def test_config_environment_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp).resolve()
            cfg = make_repo(root)
            with mock.patch.dict(os.environ, {"HARDFOC_DOCS_CONFIG": str(cfg)}):
                os.environ.pop("HARDFOC_DOCS_ROOT", None)
                self.assertEqual(paths.repo_root(), root)

    def test_nested_site_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp).resolve()
            make_repo(root)
            self.assertTrue(paths.is_site_root(root))
            self.assertFalse(paths.is_site_root(root / "docs"))


class CliConfigOptionTest(unittest.TestCase):
    def test_take_config(self):
        self.assertEqual(cli._take_config(["-f", "a.yml", "check"]), (["check"], "a.yml"))
        self.assertEqual(cli._take_config(["gen", "--check", "--config", "a.yml"]), (["gen", "--check"], "a.yml"))
        self.assertEqual(cli._take_config(["--config=a.yml", "figures"]), (["figures"], "a.yml"))
        self.assertEqual(cli._take_config(["gen"]), (["gen"], None))

    def test_missing_config_is_an_error(self):
        self.assertEqual(cli.main(["-f", "/nonexistent/mkdocs.yml", "check"]), 2)

    def test_check_runs_against_the_configured_repository(self):
        # A fresh interpreter: gen and figkit compute the root when they are first imported.
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp).resolve()
            cfg = make_repo(root, body="<!-- generated: examples -->\nstale\n<!-- /generated -->")
            env = {k: v for k, v in os.environ.items() if not k.startswith("HARDFOC_DOCS_")}
            run = [sys.executable, "-m", "hardfoc_mkdocs_theme.cli", "-f", str(cfg), "check"]
            r = subprocess.run(run, cwd="/", env=env, capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("docs/index.md", r.stdout + r.stderr)
            fill = [sys.executable, "-m", "hardfoc_mkdocs_theme.cli", "gen", "--config", str(cfg)]
            self.assertEqual(subprocess.run(fill, cwd="/", env=env, capture_output=True).returncode, 0)
            r = subprocess.run(run, cwd="/", env=env, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class BuildTest(unittest.TestCase):
    def build(self, body: str) -> str:
        tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(tmp.name)
        cfg_path = make_repo(root, body)
        cfg = load_config(str(cfg_path), strict=True)
        cfg.plugins.on_startup(command="build", dirty=False)
        with tmp, mock.patch.dict(os.environ, {"GITHUB_REPOSITORY": "hardfoc/hf-example", "GITHUB_SHA": "abc123"}):
            build(cfg)
            return (root / "site/index.html").read_text()

    def test_snippets_from_the_repository_root(self):
        out = self.build('```cpp\n--8<-- "tests/docs/snippet.cpp:part"\n```')
        self.assertIn("snippet_body", out)
        self.assertNotIn("before", out.split("md-content")[1])

    def test_repository_links(self):
        out = self.build("[x](../inc/x.hpp)")
        self.assertIn("https://github.com/hardfoc/hf-example/blob/abc123/inc/x.hpp", out)

    def test_missing_repository_file_fails_strict(self):
        from mkdocs.exceptions import Abort

        with self.assertRaises(Abort):
            self.build("[gone](../inc/missing.hpp)")


if __name__ == "__main__":
    unittest.main()
