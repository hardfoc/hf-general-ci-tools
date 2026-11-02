# Contributing to hf-general-ci-tools

Thank you for your interest in contributing to hf-general-ci-tools! This project provides a comprehensive collection of reusable GitHub Actions workflows for CI/CD automation, featuring a dual-architecture system with production-ready reusable workflows and comprehensive CI testing workflows. We welcome contributions from the community!

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Types of Contributions](#types-of-contributions)
- [Development Workflow](#development-workflow)
- [Workflow Development Guidelines](#workflow-development-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)
- [Questions and Support](#questions-and-support)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Git
- GitHub account
- Basic understanding of GitHub Actions workflows
- YAML syntax knowledge
- Familiarity with CI/CD concepts
- Understanding of the project's dual-workflow architecture:
  - **Reusable workflows** (`ru-*.yml`) - Production-ready tools for other repositories
  - **CI workflows** (`ci-*.yml`) - Comprehensive testing workflows that validate the reusable ones

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/hf-general-ci-tools.git
   cd hf-general-ci-tools
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/hardfoc/hf-general-ci-tools.git
   ```
4. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Types of Contributions

We welcome several types of contributions:

### 🐛 Bug Reports
- Report issues with existing workflows
- Include detailed reproduction steps
- Provide environment information

### ✨ Feature Requests
- Suggest new workflow capabilities
- Propose improvements to existing workflows
- Request additional configuration options

### 🔧 Workflow Improvements
- Fix bugs in existing reusable workflows (`ru-*.yml`)
- Enhance CI testing workflows (`ci-*.yml`) 
- Add new workflow capabilities (C++ analysis, documentation generation, etc.)
- Optimize workflow performance and resource usage
- Improve error handling and user experience
- Update workflow inputs/outputs to match current tool versions

### 📚 Documentation
- Update workflow documentation (`docs/ru-*.md`) to match actual implementations
- Improve Jekyll documentation site configuration
- Add real-world usage examples and tutorials
- Fix typos and clarify complex instructions
- Ensure 1:1 mapping between workflows and documentation files
- Update versioning guides and Jekyll integration docs

### 🧪 Testing
- Test workflows in different environments
- Report compatibility issues with tool versions
- Improve CI workflow coverage
- Validate tool CLI argument compatibility

### 🔧 Available Workflow Categories

This repository currently supports:

- **C++ Development**: `ru-cpp-lint.yml` and `ru-cpp-analysis.yml` for code quality
- **Documentation**: `ru-docs-publish.yml` and `ru-docs-linkcheck.yml` for Jekyll/Doxygen sites  
- **YAML Validation**: `ru-yaml-lint.yml` for configuration file quality
- **Future Categories**: Python, Node.js, Docker, or other language ecosystems welcome!

## Development Workflow

### 1. Choose an Issue

- Look for issues labeled `good first issue` for beginners
- Check `help wanted` for more complex tasks
- Comment on the issue to indicate you're working on it

### 2. Make Your Changes

- Follow the [Workflow Development Guidelines](#workflow-development-guidelines)
- Update documentation as needed
- Test your changes thoroughly

### 3. Test Your Changes

- Test workflows in a test repository
- Verify all inputs and outputs work correctly
- Check that error handling works as expected

### 4. Submit a Pull Request

- Follow the [Pull Request Process](#pull-request-process)
- Ensure all checks pass
- Request review from maintainers

## Workflow Development Guidelines

### General Principles

- **Reusability**: Workflows should be designed for use across different repositories
- **Configurability**: Provide sensible defaults but allow extensive customization
- **Reliability**: Include proper error handling and validation
- **Performance**: Optimize for speed and resource usage
- **Security**: Follow GitHub Actions security best practices

### Workflow Architecture

This project uses a **dual-workflow architecture**:

#### Reusable Workflows (`ru-*.yml`)
Production-ready workflows that other repositories can call:

```yaml
---
name: 🔧 [RU] Workflow Name

on:
  workflow_call:
    inputs:
      input_name:
        description: 'Clear description of what this input does'
        required: false
        type: string
        default: 'sensible_default'
    outputs:
      output_name:
        description: 'Description of output'
        value: ${{ jobs.job-name.outputs.result }}

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - name: Step name
        # Implementation
```

#### CI Testing Workflows (`ci-*.yml`)
Comprehensive testing workflows that validate the reusable ones:

```yaml
---
name: 🔧 Workflow Name CI

on:
  push:
    branches: [main, 'release/*']
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  test-workflow:
    name: Test Workflow Name
    uses: ./.github/workflows/ru-workflow-name.yml
    with:
      # Test all possible input combinations
      input_name: "comprehensive_test_value"
```

### Input Guidelines

- **Use descriptive names**: `checkout_recursive` instead of `recursive`
- **Provide comprehensive descriptions**: Explain what each input does and when to use it
- **Set sensible defaults**: Make workflows work out-of-the-box (e.g., `paths: 'docs/** *.md'`)
- **Validate tool compatibility**: Ensure parameter names match actual tool versions (e.g., Lychee `max_retries`)
- **Use appropriate types**: `string`, `boolean` (avoid `number` for better YAML compatibility)
- **Include usage notes**: Add helpful context like `(Note: requires tool version X.Y)`

### Output Guidelines

- **Define meaningful outputs**: Only include outputs that other workflows might need
- **Use consistent naming**: Follow a clear naming convention
- **Document outputs**: Explain what each output contains

### Error Handling

- **Validate inputs early**: Check for required parameters and valid values
- **Provide clear error messages**: Help users understand what went wrong
- **Use appropriate exit codes**: Follow standard conventions
- **Include troubleshooting hints**: Suggest common solutions

### Security Considerations

- **Minimize permissions**: Only request necessary permissions
- **Use secrets appropriately**: Mark sensitive inputs as secrets
- **Avoid hardcoded values**: Use inputs and environment variables
- **Follow principle of least privilege**: Limit access to what's needed

## Documentation Guidelines

### Workflow Documentation

Each reusable workflow must have corresponding documentation in `docs/ru-*.md`:

- **Perfect 1:1 mapping**: Every `ru-*.yml` has a `ru-*.md` documentation file
- **Live CI Example**: Reference to the `ci-*.yml` that demonstrates all features
- **Accurate inputs table**: All parameters with correct defaults and descriptions
- **Real usage examples**: Working code snippets that users can copy-paste
- **Tool-specific notes**: Version requirements and compatibility information
- **Jekyll integration**: Proper front matter for the documentation site

### Documentation Structure

```markdown
# Workflow Name

Brief description of the workflow.

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| input1 | Description | Yes | value |

## Outputs

| Output | Description |
|--------|-------------|
| output1 | Description |

## Examples

### Basic Usage
```yaml
# Example here
```

### Advanced Usage
```yaml
# Example here
```

## Prerequisites

- List prerequisites

## Troubleshooting

### Common Issues

- Issue 1: Solution
- Issue 2: Solution
```

### Quality Standards

This repository maintains high quality standards:

#### YAML Quality
- **yamllint compliance**: All workflows must pass `yamllint -c _config/.yamllint`
- **No trailing whitespace**: Use proper line endings
- **Consistent formatting**: Follow established patterns in existing workflows

#### Documentation Quality  
- **No broken links**: All cross-references must work
- **Markdown formatting**: Clean structure with proper headers
- **Accurate examples**: All code examples must be functional

#### Tool Integration
- **Version compatibility**: CLI arguments must match actual tool versions
- **Parameter validation**: Ensure all inputs work as documented
- **Error handling**: Provide helpful error messages

#### Architecture Compliance
- **Dual workflow system**: Every `ru-*.yml` needs a `ci-*.yml`
- **Naming conventions**: Follow `ru-` and `ci-` prefixes consistently
- **Documentation mapping**: Maintain perfect workflow-to-docs alignment

## Testing Guidelines

### Our Testing Architecture

This project uses **comprehensive CI workflows** to test every reusable workflow:

1. **Every reusable workflow** (`ru-*.yml`) has a corresponding CI test (`ci-*.yml`)
2. **CI workflows test maximum features** - They use comprehensive input combinations
3. **Live validation** - CI workflows run against this repository's actual content
4. **Quality gates** - All workflows must pass yamllint and documentation accuracy checks

### Testing Your Workflows

1. **Create both workflows**: Always create `ru-*.yml` AND `ci-*.yml` together
2. **Test in the CI workflow**: Use the `ci-*.yml` to validate your `ru-*.yml`
3. **Verify against real content**: Test with this repository's actual files
4. **Check tool compatibility**: Ensure CLI arguments match tool versions (e.g., Lychee, yamllint)
5. **Validate documentation sync**: Ensure `docs/ru-*.md` matches the workflow parameters

### Test Cases to Consider

- **Valid inputs**: Ensure workflows work with correct inputs
- **Invalid inputs**: Test error handling with bad inputs
- **Edge cases**: Test with empty inputs, very large inputs, etc.
- **Different environments**: Test on different operating systems
- **Integration**: Test workflows work together

### Testing Checklist

- [ ] **Reusable workflow** (`ru-*.yml`) runs successfully with valid inputs
- [ ] **CI workflow** (`ci-*.yml`) comprehensively tests the reusable workflow
- [ ] **Documentation** (`docs/ru-*.md`) accurately describes all inputs/outputs
- [ ] **Tool compatibility** verified (CLI arguments match current tool versions)
- [ ] **YAML linting** passes using `_config/.yamllint`
- [ ] **Error messages** are clear and helpful for end users
- [ ] **Live CI Example** reference works in documentation
- [ ] **Navigation flow** maintains proper cross-references

## Pull Request Process

### Before Submitting

- [ ] Test your changes thoroughly
- [ ] Update documentation if needed
- [ ] Follow the coding guidelines
- [ ] Ensure all checks pass
- [ ] Write a clear description

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] Tested locally
- [ ] Tested in test repository
- [ ] All existing tests pass
- [ ] New tests added (if applicable)

## Documentation
- [ ] Documentation updated
- [ ] Examples added/updated
- [ ] README updated (if needed)

## Checklist
- [ ] Code follows project guidelines
- [ ] Self-review completed
- [ ] No breaking changes (or clearly documented)
- [ ] Ready for review
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in different environments
4. **Documentation review** for completeness
5. **Approval** from at least one maintainer

### After Approval

- **Squash and merge** (preferred) or **merge commit**
- **Delete feature branch** after merge
- **Update version tags** if applicable

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Update version** in workflow files
2. **Update CHANGELOG.md** with changes
3. **Create release tag** (e.g., `v1.2.3`)
4. **Publish release** on GitHub
5. **Update documentation** if needed

## Questions and Support

### Getting Help

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Pull Request Comments**: For specific code-related questions

### Communication Guidelines

- **Be respectful**: Treat everyone with respect
- **Be constructive**: Provide helpful feedback
- **Be patient**: Maintainers are volunteers
- **Be clear**: Explain your questions and suggestions clearly

### Resources

#### General Resources
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [YAML Syntax Guide](https://yaml.org/spec/1.2/spec.html)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

#### Project-Specific Resources
- [Jekyll Documentation](https://jekyllrb.com/docs/) - For documentation site features
- [Lychee Link Checker](https://github.com/lycheeverse/lychee) - Current CLI options and compatibility
- [yamllint Documentation](https://yamllint.readthedocs.io/) - YAML linting rules and configuration
- [GitHub Pages](https://docs.github.com/en/pages) - For documentation deployment
- [Doxygen Manual](https://www.doxygen.nl/manual/) - For C++ documentation generation

## 🙏 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same [GNU General Public License v3.0](LICENSE) that covers the project.

---

Thank you for contributing to hf-general-ci-tools! Your contributions help make CI/CD more accessible and efficient for everyone. 🚀
