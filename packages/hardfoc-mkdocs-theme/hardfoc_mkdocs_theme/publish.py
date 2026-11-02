"""Publish an unversioned site: the built site becomes the whole content of the deployment branch, at its root.

    hardfoc-docs publish-root SITE_DIR [--branch gh-pages] [--repo .] [--message "..."]

Run inside a clone of the repository. The deployment branch is fetched from ``origin`` (created as an orphan branch
when it does not exist), its content is replaced by SITE_DIR in one ordinary commit, and nothing is pushed: the
caller pushes (never with force). Kept from the branch: ``CNAME`` (a custom domain set in the Pages settings).
Always written: ``.nojekyll``, so GitHub Pages serves the files as they are. A site identical to the branch makes no
commit. Prints ``changed`` or ``unchanged``.

This is what ``ru-mkdocs-publish.yml`` runs with ``versioning: false``; a versioned site is published with mike.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile

KEEP = (".git", "CNAME")


def _git(repo: pathlib.Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=check)


def replace_tree(site: pathlib.Path, tree: pathlib.Path, keep: tuple[str, ...] = KEEP) -> None:
    """Make ``tree`` hold exactly the files of ``site`` (plus the ``keep`` entries already in it and ``.nojekyll``)."""
    for entry in tree.iterdir():
        if entry.name in keep:
            continue
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry)
        else:
            entry.unlink()
    for entry in site.iterdir():
        if entry.name in keep:
            continue
        dest = tree / entry.name
        if entry.is_dir() and not entry.is_symlink():
            shutil.copytree(entry, dest, symlinks=True)
        else:
            shutil.copy2(entry, dest, follow_symlinks=False)
    (tree / ".nojekyll").touch()


def publish_root(site: pathlib.Path, repo: pathlib.Path, branch: str, message: str) -> bool:
    """Commit ``site`` as the content of ``branch`` in ``repo``. True when a commit was made."""
    site, repo = site.resolve(), repo.resolve()
    if not (site / "index.html").is_file():
        raise SystemExit(f"publish-root: {site} has no index.html; is it a built site?")
    remote = _git(repo, "ls-remote", "--exit-code", "--heads", "origin", branch, check=False).returncode == 0
    with tempfile.TemporaryDirectory(prefix="publish-root-") as tmp:
        tree = pathlib.Path(tmp) / "tree"
        if remote:
            _git(repo, "fetch", "--no-tags", "origin", f"+refs/heads/{branch}:refs/heads/{branch}")
            _git(repo, "worktree", "add", "-q", str(tree), branch)
        elif _git(repo, "rev-parse", "--verify", "-q", f"refs/heads/{branch}", check=False).returncode == 0:
            _git(repo, "worktree", "add", "-q", str(tree), branch)
        else:
            _git(repo, "worktree", "add", "-q", "--orphan", "-b", branch, str(tree))
        try:
            replace_tree(site, tree)
            _git(tree, "add", "-A")
            if _git(tree, "diff", "--cached", "--quiet", check=False).returncode == 0:
                return False
            _git(tree, "commit", "-q", "-m", message)
            return True
        finally:
            _git(repo, "worktree", "remove", "--force", str(tree), check=False)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="hardfoc-docs publish-root", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", type=pathlib.Path)
    ap.add_argument("--branch", default="gh-pages")
    ap.add_argument("--repo", type=pathlib.Path, default=pathlib.Path("."))
    ap.add_argument("--message", default="Publish the site")
    args = ap.parse_args(argv)
    changed = publish_root(args.site, args.repo, args.branch, args.message)
    print("changed" if changed else "unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
