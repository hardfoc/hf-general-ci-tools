---
layout: default
title: "📖 Documentation"
description: "Complete documentation for hf-general-ci-tools workflows"
nav_order: 2
permalink: /docs/
---

# hf-general-ci-tools

**A collection of reusable GitHub Actions workflows for general CI/CD tasks**

---

## 🔄 Reusable Workflows

**These workflows are designed to be used by other repositories:**

| Workflow | Description | Quick Start |
|----------|-------------|-------------|
| **[🔧 C++ Linting](ru-cpp-lint.md)** | Reusable C++ code quality checks using clang-format and clang-tidy | [→ Lint Guide](ru-cpp-lint.md) |
| **[🔍 C++ Analysis](ru-cpp-analysis.md)** | Reusable C++ security analysis using cppcheck | [→ Analysis Guide](ru-cpp-analysis.md) |
| **[📚 Docs Publisher](ru-docs-publish.md)** | Reusable documentation generation and GitHub Pages deployment | [→ Docs Guide](ru-docs-publish.md) |
| **[🔗 Link Checker](ru-docs-linkcheck.md)** | Reusable documentation link validation using Lychee | [→ Link Check Guide](ru-docs-linkcheck.md) |
| **[📝 YAML Linting](ru-yaml-lint.md)** | Reusable YAML file validation and formatting | [→ YAML Guide](ru-yaml-lint.md) |
| **[� Release Management](ru-release.md)** | Reusable GitHub release creation with auto-generated notes | [→ Release Guide](ru-release.md) |
| **[�📖 Versioning](versioning-guide.md)** | Multi-version documentation with Doxygen and Jekyll | [→ Versioning Guide](versioning-guide.md) |

## 🏠 Repository-Specific Workflows

**These workflows are used internally by this repository:**

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| **[Publish Documentation](https://github.com/hardfoc/hf-general-ci-tools/blob/main/.github/workflows/ci-docs-publish.yml)** | Builds and deploys this repo's documentation site | Push to main, PRs |
| **[YAML Lint](https://github.com/hardfoc/hf-general-ci-tools/blob/main/.github/workflows/ci-yaml-lint.yml)** | Validates YAML syntax in this repository | Push, PRs |

## 📚 Documentation Structure

### **🔧 Reusable Workflows** (Production Tools)
- **[🔧 C++ Linting Tools](ru-cpp-lint.md)** - Clang-format and clang-tidy for any C++ project
- **[🔍 C++ Static Analysis](ru-cpp-analysis.md)** - Cppcheck security analysis with flexible configuration
- **[📚 Documentation Publisher](ru-docs-publish.md)** - Complete docs pipeline with Doxygen, Jekyll, and GitHub Pages
- **[🔗 Documentation Link Check](ru-docs-linkcheck.md)** - Comprehensive link validation using Lychee
- **[📝 YAML Linting Tools](ru-yaml-lint.md)** - Flexible YAML validation and formatting
- **[� Markdown Linting Tools](ru-markdown-lint.md)** - Markdown file validation with auto-fix capabilities
- **[�📦 Release Management](ru-release.md)** - Automated GitHub release creation with professional release notes

### **🚀 Design & Implementation**
- **[🚀 CI Workflows & Design Philosophy](ci-workflows.md)** - Understanding our testing approach and architecture decisions
- **[📖 Versioning Guide](versioning-guide.md)** - Multi-version documentation strategies with Doxygen and Jekyll
- **[🎨 Jekyll Integration Guide](jekyll-guide.md)** - Advanced Jekyll configuration for documentation sites

## 🎯 Quick Start

### 1. Choose Your Reusable Workflow

Select the appropriate **reusable workflow** for your needs:

```yaml
# For C/C++ projects
uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-lint.yml@v1

# For documentation
uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1

# For link checking
uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1

# For YAML validation
uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-yaml-lint.yml@v1

# For Markdown validation
uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1

# For releases
uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-release.yml@v1
```

> **Note:** These are **reusable workflows** designed to be called from other repositories.
> The repository-specific workflows (like `ci-docs-publish.yml`) are only used internally by this repository.

### 2. Configure Your Workflow

Each workflow supports extensive configuration options. See the individual workflow documentation for details.

### 3. Deploy

The workflows will automatically run on your specified triggers and provide detailed feedback.

## 🔧 Features

- **🔄 Reusable** - Drop-in workflows for common CI tasks
- **⚙️ Configurable** - Extensive input parameters for customization
- **📚 Well Documented** - Comprehensive guides and examples
- **🛡️ Secure** - Follows GitHub Actions security best practices
- **🚀 Fast** - Optimized for performance and reliability

## 📋 Workflow Types

### 🔄 Reusable Workflows
These workflows are designed to be **called from other repositories** using the `uses` keyword:

```yaml
jobs:
  my-job:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    with:
      jekyll_enabled: true
      deploy_pages: true
```

### 🏠 Repository-Specific Workflows
These workflows are **only used internally** by this repository:

- **`ci-docs-publish.yml`** - Builds and deploys this repo's documentation site
- **`ci-yaml-lint.yml`** - Validates YAML syntax in this repository

> **For other repositories:** Only use the **reusable workflows** listed in the "Reusable Workflows" section above.

## 📖 Usage Examples

### Basic C/C++ Linting

```yaml
name: Code Quality
on: [push, pull_request]
jobs:
  lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-lint.yml@v1
    with:
      source_dirs: "src/"
      include_patterns: "*.cpp,*.hpp,*.c,*.h"
```

### Documentation Generation

```yaml
name: Documentation
on: [push]
jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    with:
      jekyll_enabled: true
      run_link_check: true
      deploy_pages: true
```

### Link Validation

```yaml
name: Link Check
on: [push, pull_request]
jobs:
  links:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    with:
      paths: "docs/** *.md"
      verbose: true
```

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](https://github.com/hardfoc/hf-general-ci-tools/blob/main/CONTRIBUTING.md)
for details.

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/hardfoc/hf-general-ci-tools/blob/main/LICENSE)
file for details.

## 🙏 Acknowledgments

- GitHub Actions team for the excellent CI/CD platform
- The open source community for inspiration and feedback
- All contributors who help improve these workflows

---

[Next: Reusable Workflows →](workflows.md)

**Made with ❤️ by [N3b3x](https://github.com/n3b3x)**

[GitHub](https://github.com/hardfoc/hf-general-ci-tools) • [Issues](https://github.com/hardfoc/hf-general-ci-tools/issues)
