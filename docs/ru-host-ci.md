# ru-host-ci

Build, test and analyse a CMake project on the host, with clang-tidy 18 and cppcheck over the compiler's own
compile database.

`ru-host-ci.yml` runs the native (host) half of a C/C++ project's CI in one job:

1. **Configure.** Uses `cmake --preset <preset>` when `preset` is set, otherwise
   `cmake -S <source_dir> -B <build_dir> -G Ninja`. Either way it passes
   `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`.
2. **Build.** Runs `cmake --build <build_dir> --parallel`.
3. **Test.** Runs `ctest --test-dir <build_dir> --output-on-failure`.
4. **Select files.** Picks translation units from `compile_commands.json`.
   A unit is analysed if its path relative to the repository root matches
   `tidy_paths`. Units that match `exclude_paths` and anything generated in
   the build tree are dropped. The selection is written as a filtered
   database, so both analysers see exactly the same files.
5. **Analyse.** Runs **clang-tidy 18** (`-p <build_dir>`) and **cppcheck**
   (`--project=<filtered database>`) on that set. Both see the include paths
   and defines the compiler sees, so no configuration is guessed.
6. **Report.** Findings appear as annotations. The reports, the file list and
   the database are uploaded as an artifact. With `fail_on_findings: true`
   (the default), any finding fails the job.

clang-tidy exits 0 even when it prints warnings, so the workflow counts
`file:line:col: warning|error: ... [check]` lines itself. It ignores compiler
warnings echoed as `clang-diagnostic-*`, except `clang-diagnostic-error`.
cppcheck findings are lines of severity error, warning, performance,
portability or style; `information` lines (analysis limits) do not count.

## Minimal caller

```yaml
jobs:
  host:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-host-ci.yml@v1
    permissions:
      contents: read
    with:
      preset: host-debug
      build_dir: build/host-debug           # the preset's binaryDir, from the repo root
      tidy_paths: "^(src|include|apps)/"
      cppcheck_suppressions: tools/lint/cppcheck-suppressions.txt
```

## Inputs

<!-- generated: inputs-ru-host-ci -->
| Input | Type | Default | Description |
| --- | --- | --- | --- |
| `preset` | string | empty | CMake configure preset (from CMakePresets.json in source_dir). Empty: configure with -S source_dir -B build_dir. |
| `source_dir` | string | `.` | CMake source directory, relative to the repository root |
| `build_dir` | string | `build/host` | Build directory, relative to the repository root. With a preset this must be the preset's binaryDir; compile_commands.json is read from here. |
| `cmake_args` | string | empty | Extra arguments for the configure step (space separated) |
| `build_type` | string | `Debug` | CMAKE_BUILD_TYPE when no preset is used |
| `run_tests` | boolean | `true` | Run ctest after the build |
| `ctest_args` | string | empty | Extra arguments for ctest (space separated) |
| `tidy_paths` | string | empty | Python regular expression matched (re.search) against each translation unit's path relative to the repository root. Only matching files are given to clang-tidy and cppcheck. Empty: every file in the database. |
| `exclude_paths` | string | `(^\|/)(third_party\|external\|vendor\|_deps)/` | Python regular expression; translation units whose relative path matches are never analysed, and findings in matching files are not counted. The build directory is always excluded. |
| `run_clang_tidy` | boolean | `true` | Run clang-tidy 18 on the selected files |
| `clang_tidy_config` | string | empty | Path to a .clang-tidy file. Empty: clang-tidy's normal lookup from each source file |
| `run_cppcheck` | boolean | `true` | Run cppcheck on the selected files |
| `cppcheck_suppressions` | string | empty | Path to a cppcheck --suppressions-list file (optional) |
| `cppcheck_enable` | string | `warning,performance,portability` | cppcheck --enable value |
| `fail_on_findings` | boolean | `true` | Fail the job when clang-tidy or cppcheck report findings |
| `apt_packages` | string | empty | Extra apt packages to install before configuring (space separated) |
| `submodules` | string | `false` | actions/checkout submodules value: false, true or recursive |
| `runs_on` | string | `ubuntu-24.04` | Runner label (Ubuntu 24.04 or newer, for clang-tidy-18 from apt) |
| `artifact_name` | string | `host-ci-reports` | Name of the uploaded report artifact |
<!-- /generated -->

Outputs: `tidy_findings` and `cppcheck_findings`, the counts of findings (empty when a tool did not run).

## Jobs and permissions

<!-- generated: jobs-ru-host-ci -->
| Job | Permissions | Steps |
| --- | --- | --- |
| `host` (build, test, analyse) | `contents: read` | `actions/checkout`; Install toolchain and analysers; Configure (compile_commands.json exported); Build; Test (ctest); Select files to analyse; clang-tidy 18; cppcheck; Upload reports; Enforce zero findings |
<!-- /generated -->

## Self-test

`ci-host-ci.yml` runs the workflow twice on `tests/fixtures/host-ci`:

- with the preset on clean code, where it must pass with `fail_on_findings: true`
  (the vendored file with a defect is excluded by the default `exclude_paths`);
- through `-S/-B` with seeded defects, where both analysers must report findings.

## When it fails

| Symptom | Cause | Fix |
| --- | --- | --- |
| `compile_commands.json` not found | `build_dir` is not the preset's `binaryDir` | Set `build_dir` to the preset's `binaryDir`, from the repository root |
| clang-tidy reports errors in third-party headers | The headers are not under an excluded path | Extend `exclude_paths`, or mark them `SYSTEM` in CMake |
| cppcheck reports a finding the code means | A known false positive | Add it to the `cppcheck_suppressions` file with the path |
| No files analysed | `tidy_paths` matches nothing | Check the regex against paths relative to the repository root |
