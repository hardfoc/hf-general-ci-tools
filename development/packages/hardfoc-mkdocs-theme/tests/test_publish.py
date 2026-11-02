"""publish-root: the built site becomes the whole deployment branch, in an ordinary commit."""

from __future__ import annotations

import pathlib
import subprocess
import tempfile
import unittest

from hardfoc_mkdocs_theme.publish import publish_root


def git(cwd, *args) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True).stdout.strip()


class PublishRootTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = pathlib.Path(self.tmp.name)
        self.origin, self.clone, self.site = t / "origin.git", t / "clone", t / "site"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(self.origin)], check=True)
        subprocess.run(["git", "clone", "-q", str(self.origin), str(self.clone)], check=True, capture_output=True)
        for k, v in (("user.name", "test"), ("user.email", "test@example.invalid"), ("commit.gpgsign", "false")):
            git(self.clone, "config", k, v)
        (self.clone / "mkdocs.yml").write_text("site_name: x\n")
        git(self.clone, "add", "-A")
        git(self.clone, "commit", "-q", "-m", "source")
        git(self.clone, "push", "-q", "origin", "main")
        self.site.mkdir()
        (self.site / "index.html").write_text("<h1>v1</h1>")
        (self.site / "sub").mkdir()
        (self.site / "sub/index.html").write_text("sub")

    def tearDown(self):
        self.tmp.cleanup()

    def files(self) -> set[str]:
        return set(git(self.clone, "ls-tree", "-r", "--name-only", "gh-pages").splitlines())

    def push(self):
        git(self.clone, "push", "-q", "origin", "gh-pages")

    def test_creates_orphan_branch(self):
        self.assertTrue(publish_root(self.site, self.clone, "gh-pages", "Publish"))
        self.assertEqual(self.files(), {".nojekyll", "index.html", "sub/index.html"})
        # An orphan: no history shared with main.
        self.assertEqual(git(self.clone, "rev-list", "--count", "gh-pages"), "1")

    def test_replaces_old_site_and_is_idempotent(self):
        publish_root(self.site, self.clone, "gh-pages", "Publish")
        # A stale custom domain and an old file sit on the branch.
        git(self.clone, "worktree", "add", "-q", str(pathlib.Path(self.tmp.name) / "wt"), "gh-pages")
        wt = pathlib.Path(self.tmp.name) / "wt"
        (wt / "CNAME").write_text("docs.example.org\n")
        (wt / "old.html").write_text("old")
        git(wt, "add", "-A")
        git(wt, "commit", "-q", "-m", "manual")
        git(self.clone, "worktree", "remove", str(wt))
        self.push()
        git(self.clone, "branch", "-D", "gh-pages")  # the remote branch is the truth
        (self.site / "index.html").write_text("<h1>v2</h1>")
        (self.site / "sub/index.html").unlink()
        (self.site / "sub").rmdir()
        self.assertTrue(publish_root(self.site, self.clone, "gh-pages", "Publish 2"))
        self.assertEqual(self.files(), {".nojekyll", "index.html"})
        self.assertEqual(git(self.clone, "show", "gh-pages:index.html"), "<h1>v2</h1>")
        # A fast-forward of the remote branch: never needs a force push.
        git(self.clone, "merge-base", "--is-ancestor", "origin/gh-pages", "gh-pages")
        self.push()
        self.assertFalse(publish_root(self.site, self.clone, "gh-pages", "Publish 3"))

    def test_custom_domain_comes_from_the_site(self):
        (self.site / "CNAME").write_text("docs.example.org\n")
        publish_root(self.site, self.clone, "gh-pages", "Publish")
        self.assertEqual(git(self.clone, "show", "gh-pages:CNAME"), "docs.example.org")

    def test_refuses_a_folder_that_is_not_a_site(self):
        (self.site / "index.html").unlink()
        with self.assertRaises(SystemExit):
            publish_root(self.site, self.clone, "gh-pages", "Publish")


if __name__ == "__main__":
    unittest.main()
