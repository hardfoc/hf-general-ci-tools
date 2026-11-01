#!/usr/bin/env python3
"""Tests for the self-CI check scripts. Run: python .github/scripts/test_checks.py"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script: str, *args: str, cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, os.path.join(HERE, script), *args],
                          cwd=cwd, capture_output=True, text=True)


README = textwrap.dedent("""\
    <!-- permissions-table:start -->
    | Workflow | Caller must grant |
    |---|---|
    | `ru-x.yml` | {row} |
    <!-- permissions-table:end -->
    """)

WORKFLOW = textwrap.dedent("""\
    on: {{ workflow_call: {{}} }}
    {top}jobs:
      a:
        runs-on: ubuntu-latest
        {perms}
        steps: [{{ run: "true" }}]
    """)


class PermissionsContract(unittest.TestCase):
    def check(self, row: str, perms: str, top: str = "", caller: str | None = None) -> subprocess.CompletedProcess:
        d = tempfile.mkdtemp()
        wf = os.path.join(d, "wf")
        os.makedirs(wf)
        with open(os.path.join(d, "README.md"), "w") as fh:
            fh.write(README.format(row=row))
        with open(os.path.join(wf, "ru-x.yml"), "w") as fh:
            fh.write(WORKFLOW.format(top=top, perms=perms))
        if caller is not None:
            with open(os.path.join(wf, "ci-x.yml"), "w") as fh:
                fh.write(caller)
        return run("check_permissions.py", "--readme", os.path.join(d, "README.md"), "--workflows", wf)

    def test_match_passes(self):
        r = self.check("`contents: read`", "permissions: { contents: read }")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_job_asks_more_than_documented_fails(self):
        r = self.check("`contents: read`", "permissions: { contents: read, pull-requests: write }")
        self.assertEqual(r.returncode, 1)
        self.assertIn("startup_failure", r.stdout)

    def test_documented_more_than_needed_fails(self):
        r = self.check("`contents: write`", "permissions: { contents: read }")
        self.assertEqual(r.returncode, 1)
        self.assertIn("shrink the row", r.stdout)

    def test_missing_job_permissions_fails(self):
        r = self.check("`contents: read`", "")
        self.assertEqual(r.returncode, 1)

    def test_top_level_permissions_fails(self):
        r = self.check("`contents: read`", "permissions: { contents: read }", top="permissions: { contents: read }\n")
        self.assertEqual(r.returncode, 1)

    def test_empty_permissions_is_none(self):
        r = self.check("none", "permissions: {}")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_local_caller_granting_too_little_fails(self):
        caller = "on: push\npermissions: { contents: read }\njobs:\n  c:\n    uses: ./.github/workflows/ru-x.yml\n"
        r = self.check("`contents: write`", "permissions: { contents: write }", caller=caller)
        self.assertEqual(r.returncode, 1)
        self.assertIn("grants", r.stdout)


class RunTails(unittest.TestCase):
    def check(self, script: str) -> subprocess.CompletedProcess:
        d = tempfile.mkdtemp()
        p = os.path.join(d, "w.yml")
        with open(p, "w") as fh:
            fh.write("jobs:\n  a:\n    steps:\n      - run: |\n" + textwrap.indent(script, " " * 10))
        return run("check_run_tails.py", p)

    def test_bare_and_list_at_end_fails(self):
        self.assertEqual(self.check('echo a\n[ -n "$X" ] && echo set\n').returncode, 1)

    def test_and_list_with_or_passes(self):
        self.assertEqual(self.check('[ -n "$X" ] && echo set || true\n').returncode, 0)

    def test_and_list_not_last_passes(self):
        self.assertEqual(self.check('[ -n "$X" ] && echo set\necho done\n').returncode, 0)

    def test_if_block_passes(self):
        self.assertEqual(self.check('if [ -n "$X" ]; then\n  echo set\nfi\n').returncode, 0)


def gate_script() -> str:
    import yaml
    path = os.path.join(HERE, "..", "workflows", "ru-ci-gate.yml")
    with open(path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    for step in doc["jobs"]["gate"]["steps"]:
        if step.get("name") == "Evaluate needed jobs":
            return step["run"]
    raise AssertionError("gate step not found")


CALLER = textwrap.dedent("""\
    on: pull_request
    jobs:
      build: {runs-on: ubuntu-latest, steps: [{run: "true"}]}
      docs: {runs-on: ubuntu-latest, steps: [{run: "true"}]}
      ci-gate:
        needs: [build, docs]
        if: always()
        uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-ci-gate.yml@v1
    """)


class CiGate(unittest.TestCase):
    def gate(self, needs: dict, allow: str = "", caller: str | None = None) -> subprocess.CompletedProcess:
        import json
        d = tempfile.mkdtemp()
        env = {**os.environ, "NEEDS_JSON": json.dumps(needs), "ALLOW_SKIPPED": allow,
               "VERIFY_NEEDS": "true" if caller is not None else "false",
               "WORKFLOW_REF": "o/r/.github/workflows/ci.yml@refs/pull/1/merge",
               "GITHUB_REPOSITORY": "o/r", "GITHUB_STEP_SUMMARY": os.path.join(d, "summary.md")}
        if caller is not None:
            bindir = os.path.join(d, "bin")
            os.makedirs(bindir)
            with open(os.path.join(d, "caller.yml"), "w") as fh:
                fh.write(caller)
            with open(os.path.join(bindir, "gh"), "w") as fh:
                fh.write(f"#!/bin/sh\ncat '{os.path.join(d, 'caller.yml')}'\n")
            os.chmod(os.path.join(bindir, "gh"), 0o755)
            env["PATH"] = bindir + os.pathsep + env["PATH"]
        return subprocess.run(["bash", "-e", "-c", gate_script()], env=env, capture_output=True, text=True)

    def test_all_success_passes(self):
        r = self.gate({"build": {"result": "success"}, "docs": {"result": "success"}})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_failure_fails(self):
        r = self.gate({"build": {"result": "failure"}, "docs": {"result": "success"}})
        self.assertEqual(r.returncode, 1)
        self.assertIn("'build' finished with 'failure'", r.stdout)

    def test_cancelled_fails(self):
        self.assertEqual(self.gate({"build": {"result": "cancelled"}}).returncode, 1)

    def test_skip_not_allowed_fails(self):
        r = self.gate({"build": {"result": "success"}, "docs": {"result": "skipped"}})
        self.assertEqual(r.returncode, 1)

    def test_allowed_skip_passes(self):
        r = self.gate({"build": {"result": "success"}, "docs": {"result": "skipped"}}, allow="docs")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_unknown_allowed_job_fails(self):
        r = self.gate({"build": {"result": "success"}}, allow="dcos")
        self.assertEqual(r.returncode, 1)

    def test_empty_needs_fails(self):
        self.assertEqual(self.gate({}).returncode, 1)

    def test_caller_complete_passes(self):
        r = self.gate({"build": {"result": "success"}, "docs": {"result": "success"}}, caller=CALLER)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_caller_missing_need_fails(self):
        caller = CALLER.replace("needs: [build, docs]", "needs: [build]")
        r = self.gate({"build": {"result": "success"}}, caller=caller)
        self.assertEqual(r.returncode, 1)
        self.assertIn("does not list these jobs in needs: docs", r.stdout)

    def test_caller_without_always_fails(self):
        caller = CALLER.replace("    if: always()\n", "")
        r = self.gate({"build": {"result": "success"}, "docs": {"result": "success"}}, caller=caller)
        self.assertEqual(r.returncode, 1)
        self.assertIn("always()", r.stdout)


if __name__ == "__main__":
    unittest.main()
