---
layout: default
title: "📦 Release Management"
description: "Automated GitHub release creation with ru-release.yml reusable workflow"
nav_order: 6
---

# 📦 Release Management

**Automated GitHub release creation with `ru-release.yml` reusable workflow**

---

## 🎯 Overview

The `ru-release.yml` workflow provides automated GitHub release creation with:

- ✅ **Auto-generated release notes** from GitHub's built-in feature
- ✅ **Tag-based releases** with automatic source code archives
- ✅ **Draft and prerelease** support for controlled releases
- ✅ **Minimal configuration** - just tag and release
- ✅ **Professional release notes** generated from PR and commit history

---

## 🚀 Quick Start

### Basic Release Workflow

```yaml
# .github/workflows/release.yml
name: 📦 Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-release.yml@v1
    permissions:
      contents: write
```

### Advanced Configuration

```yaml
# .github/workflows/release.yml
name: 📦 Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-release.yml@v1
    with:
      draft: ${{ contains(github.ref_name, 'rc') }}
      prerelease: ${{ contains(github.ref_name, 'beta') || contains(github.ref_name, 'alpha') }}
    permissions:
      contents: write
```

---

## ⚙️ Configuration

### Inputs

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `draft` | boolean | `false` | Create as draft release (not publicly visible) |
| `prerelease` | boolean | `false` | Mark as pre-release (shown with warning) |
| `tag_name` | string | `github.ref_name` | Custom tag name (usually automatic) |

### Permissions Required

```yaml
permissions:
  contents: write  # Required for creating releases
```

---

## 📋 Usage Patterns

### 1. Production Releases

```yaml
name: Production Release
on:
  push:
    tags: ['v[0-9]+.[0-9]+.[0-9]+']  # v1.0.0, v2.1.3, etc.

jobs:
  release:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-release.yml@v1
    with:
      draft: false
      prerelease: false
    permissions:
      contents: write
```

### 2. Beta/RC Releases

```yaml
name: Pre-Release
on:
  push:
    tags: ['v*-beta*', 'v*-rc*']  # v1.0.0-beta1, v2.0.0-rc1

jobs:
  prerelease:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-release.yml@v1
    with:
      prerelease: true
    permissions:
      contents: write
```

### 3. Draft Reviews

```yaml
name: Draft Release
on:
  workflow_dispatch:  # Manual trigger
    inputs:
      tag:
        description: 'Release tag'
        required: true
        type: string

jobs:
  draft:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-release.yml@v1
    with:
      draft: true
      tag_name: ${{ inputs.tag }}
    permissions:
      contents: write
```

### 4. Combined CI + Release

```yaml
name: CI and Release
on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

jobs:
  # Run tests first
  test:
    if: github.event_name != 'push' || !startsWith(github.ref, 'refs/tags/')
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-lint.yml@v1
    with:
      source_dirs: "src/"

  # Only release on tags
  release:
    if: startsWith(github.ref, 'refs/tags/')
    needs: [test]
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-release.yml@v1
    permissions:
      contents: write
```

---

## 🔄 Release Process

### What Happens

1. **Checkout**: Repository code is checked out with full history
2. **Release Creation**: GitHub release is created with:
   - **Tag**: From `inputs.tag_name` or the git tag that triggered the workflow
   - **Title**: Auto-generated from tag name
   - **Notes**: Auto-generated from PRs and commits since last release
   - **Assets**: Source code archives (`.zip` and `.tar.gz`) automatically included

### Auto-Generated Release Notes

GitHub automatically generates release notes including:
- **Pull Requests** merged since the last release
- **New Contributors** with their first contributions
- **Commit History** formatted professionally
- **Comparison Links** to view changes

---

## 🛠️ Advanced Scenarios

### Custom Tag Naming

```yaml
jobs:
  release:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-release.yml@v1
    with:
      tag_name: "release-${{ github.run_number }}"
    permissions:
      contents: write
```

### Conditional Release Types

```yaml
jobs:
  release:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-release.yml@v1
    with:
      draft: ${{ github.event_name == 'workflow_dispatch' }}
      prerelease: ${{ contains(github.ref_name, '-') }}
    permissions:
      contents: write
```

---

## 🔗 Related Workflows

- **[ESP32 Releases](https://github.com/hardfoc/hf-espidf-ci-tools)** - Use `ru-release-with-artifacts.yml` for firmware releases
- **[Documentation](ru-docs-publish.md)** - Often combined with release workflows
- **[C/C++ Linting](ru-cpp-lint.md)** - Quality checks before releases

---

## 📚 Examples in Production

This workflow is used by:
- **HardFOC Driver Libraries** - Automated releases on version tags
- **ESP32 Projects** - Combined with build artifacts for firmware releases
- **Documentation Sites** - Release coordination with documentation updates

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Permission denied** | Add `permissions: contents: write` to calling workflow |
| **Tag not found** | Ensure workflow triggers on correct tag patterns |
| **Empty release notes** | Check that PRs use proper titles and descriptions |
| **Duplicate releases** | Verify tag uniqueness and workflow triggers |

### Debug Tips

1. **Check permissions** in the calling repository's workflow
2. **Verify tag format** matches your trigger patterns
3. **Review repository settings** for release permissions
4. **Test with draft releases** first

---

**📖 [← Back to Documentation Index](index.md)**