---
layout: default
title: "🚀 CI Workflows & Design Philosophy"
description: "Understanding our comprehensive CI testing approach and design decisions"
nav_order: 6
---

# 🚀 CI Workflows & Design Philosophy

**Understanding Our Comprehensive Testing & Validation Approach**

---

## 📋 Overview

This repository uses a **dual-workflow architecture** that separates **reusable tools** from **comprehensive testing**. This design ensures our workflows are thoroughly validated while providing clean, reliable tools for external use.

### **🎯 Architecture Philosophy**

```
🔧 REUSABLE WORKFLOWS (ru-*.yml)     🚀 CI WORKFLOWS (ci-*.yml)
├── ru-cpp-lint.yml                 ├── ci-cpp-lint.yml
├── ru-cpp-analysis.yml             ├── ci-cpp-analysis.yml
├── ru-docs-publish.yml             ├── ci-docs-publish.yml
├── ru-docs-linkcheck.yml           ├── ci-docs-linkcheck.yml
└── ru-yaml-lint.yml                └── ci-yaml-lint.yml
```

**🔧 Reusable Workflows** = Clean, documented tools for other repositories
**🚀 CI Workflows** = Comprehensive testing that validates every feature

---

## 🔧 Reusable Workflows (Production Tools)

These are the **production-ready tools** that external repositories should use:

### **🔧 ru-cpp-lint.yml** - C++ Linting Tools
- **Purpose:** Provides clang-format and clang-tidy linting for any C++ project
- **Features:** Configurable versions, custom rules, extensive file pattern matching
- **Documentation:** [→ C++ Linting Guide](ru-cpp-lint.md)

### **🔍 ru-cpp-analysis.yml** - C++ Static Analysis
- **Purpose:** Provides cppcheck static analysis for security and bug detection
- **Features:** Configurable strictness, multiple C++ standards, Docker-based analysis
- **Documentation:** [→ C++ Analysis Guide](ru-cpp-analysis.md)

### **📚 ru-docs-publish.yml** - Documentation Publisher
- **Purpose:** Comprehensive documentation building and GitHub Pages deployment
- **Features:** Doxygen, Jekyll, versioning, link checking, multi-format support
- **Documentation:** [→ Docs Publisher Guide](ru-docs-publish.md)

### **🔗 ru-docs-linkcheck.yml** - Documentation Link Check
- **Purpose:** Validates all links in documentation using Lychee
- **Features:** External link checking, anchor validation, custom configurations
- **Documentation:** [→ Link Check Guide](ru-docs-linkcheck.md)

### **📝 ru-yaml-lint.yml** - YAML Linting Tools
- **Purpose:** Validates YAML files using yamllint with extensive configuration
- **Features:** Custom rules, multiple file patterns, strict/permissive modes
- **Documentation:** [→ YAML Linting Guide](ru-yaml-lint.md)

---

## 🚀 CI Workflows (Comprehensive Testing)

These workflows **test and validate** our reusable workflows by exercising **all their features** against real code:

### **🔧 ci-cpp-lint.yml** - C++ Lint Testing
```yaml
# Tests ru-cpp-lint.yml with maximum configuration
- clang_version: "20"           # Latest version
- extensions: "c,cpp,cc,cxx,h,hpp"  # All C++ extensions
- files_changed_only: false     # Test full analysis
- lines_changed_only: false     # Test comprehensive checking
- step_summary: true           # Test reporting features
```
**→ Validates:** All clang-format/clang-tidy features against real C++ code in `cpp-ci-test/`

### **🔍 ci-cpp-analysis.yml** - C++ Analysis Testing
```yaml
# Tests ru-cpp-analysis.yml with comprehensive settings
- paths: "cpp-ci-test/src cpp-ci-test/include"  # Real code paths
- std: "c++17"                 # Modern C++ standard
- strict: false               # Test permissive mode for CI
```
**→ Validates:** Cppcheck analysis capabilities against actual C++ codebase

### **📚 ci-docs-publish.yml** - Docs Publishing Testing
```yaml
# Tests ru-docs-publish.yml with full feature set
- doxygen_config: "_config/Doxyfile"    # Real Doxygen setup
- jekyll_enabled: true                  # Full Jekyll integration
- deploy_pages: true                    # Actual GitHub Pages deployment
- run_link_check: true                  # Integrated link validation
```
**→ Validates:** Complete documentation pipeline including this repository's live docs

### **🔗 ci-docs-linkcheck.yml** - Link Check Testing
```yaml
# Tests ru-docs-linkcheck.yml with maximum features
- check_external_links: true    # Test external link validation
- check_anchors: true          # Test anchor link validation
- follow_redirects: true       # Test redirect handling
- timeout: 30                  # Test timeout configurations
```
**→ Validates:** Link checking against all documentation in this repository

### **📝 ci-yaml-lint.yml** - YAML Lint Testing
```yaml
# Tests ru-yaml-lint.yml against repository YAML files
- paths: '**/*.yml,**/*.yaml'   # All YAML files in repo
- strict_mode: false           # Test permissive validation
```
**→ Validates:** YAML linting against all workflow files in `.github/workflows/`

---

## 🎯 Design Decisions & Benefits

### **✅ Why This Architecture?**

1. **🔒 Quality Assurance**
   - Every reusable workflow is continuously tested with real-world scenarios
   - CI workflows catch regressions and validate new features
   - External users get battle-tested, reliable tools

2. **📋 Documentation by Example**
   - CI workflows serve as **live documentation** showing all features
   - No need for separate example files - the CI IS the example
   - Always up-to-date examples that actually run

3. **🚀 Continuous Validation**
   - Every push tests all workflows against real code
   - Ensures compatibility across different configurations
   - Validates integration between different tools

4. **🎯 Clear Separation of Concerns**
   - `ru-*.yml` = Clean, focused, reusable tools
   - `ci-*.yml` = Comprehensive testing and validation
   - No confusion about what external users should use

### **🔄 Development Workflow**

```
1. Modify reusable workflow (ru-*.yml)
2. Update corresponding CI test (ci-*.yml)
3. CI automatically validates changes
4. Documentation shows working examples
5. External users get reliable, tested tools
```

---

## 📚 Related Guides

- **[Jekyll Integration Guide](jekyll-guide.md)** - Advanced Jekyll configuration for documentation sites
- **[Versioning Guide](versioning-guide.md)** - Multi-version documentation strategies
- **[All Reusable Workflows](workflows.md)** - Complete workflow documentation index

---

## 🤝 For External Users

**Use the reusable workflows (`ru-*.yml`)** - they're production-ready, well-documented, and continuously tested.

**Reference the CI workflows (`ci-*.yml`)** - they show you exactly how to configure and use every feature.

**Never copy example files** - use the live CI workflows as your examples since they actually run and validate!

---

*This design ensures you always get reliable, tested, and well-documented workflows for your projects.* ✨
