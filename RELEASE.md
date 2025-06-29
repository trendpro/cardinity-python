# Release Process Documentation

This document outlines the complete release process for cardinity-python, including automated PyPI publishing via GitHub Actions.

## Overview

The release process is fully automated using GitHub Actions with direct publishing to production PyPI after comprehensive validation and testing.

## Prerequisites

### 1. Repository Setup

Ensure your repository has the following secrets configured in GitHub:

#### GitHub Repository Secrets

Navigate to your repository → Settings → Secrets and variables → Actions, and add:

- `PYPI_API_TOKEN`: Production PyPI API token with project scope

#### GitHub Environments

Set up the following environment in your repository (Settings → Environments):

**pypi**
- Add protection rules (recommended: require approval for production)
- Add `PYPI_API_TOKEN` secret

### 2. PyPI Account Setup

#### Create PyPI Account
**Production PyPI**: https://pypi.org/account/register/

#### Generate API Token
1. Go to Account Settings → API tokens
2. Create a new token with project scope
3. Copy the token (you won't see it again)
4. Add to GitHub secrets

## Release Types

### 1. Pre-release (Testing)
- Tags: `v1.0.0-rc1`, `v1.0.0-beta1`, `v1.0.0-alpha1`
- Triggers: Pre-release workflow
- Publishes: Nothing (dry-run only)
- Purpose: Testing and validation

### 2. Production Release
- Tags: `v1.0.0`, `v1.2.3`
- Triggers: Full publish workflow
- Publishes: Production PyPI
- Creates: GitHub release

## Step-by-Step Release Process

### Step 1: Prepare Release

Use the automated release preparation script:

```bash
# Navigate to project directory
cd cardinity-python

# Prepare release (this will run tests, update versions, etc.)
python scripts/prepare-release.py 1.2.0

# Or skip certain steps if needed
python scripts/prepare-release.py 1.2.0 --skip-tests --skip-build
```

The script will:
- Validate git state (clean working directory, up-to-date with remote)
- Run comprehensive tests (linting, type checking, pytest)
- Update version in `pyproject.toml` and `cardinity/__init__.py`
- Update `CHANGELOG.md` with new version section
- Build and validate the package

### Step 2: Review and Commit Changes

1. **Review the changes made by the script:**
   ```bash
   git diff
   ```

2. **Edit CHANGELOG.md to add specific changes:**
   ```markdown
   ## [1.2.0] - 2024-01-15
   
   ### Added
   - New payment link expiration handling
   - Enhanced error messages for validation
   
   ### Changed
   - Updated dependencies to latest versions
   - Improved type hints coverage
   
   ### Fixed
   - Fixed issue with 3DS v2 authentication
   - Resolved memory leak in HTTP client
   ```

3. **Commit the changes:**
   ```bash
   git add .
   git commit -m "Prepare release v1.2.0"
   ```

### Step 3: Create and Push Release Tag

```bash
# Create the release tag
git tag v1.2.0

# Push the commit and tag
git push origin main
git push origin v1.2.0
```

### Step 4: Monitor Automated Release

The GitHub Actions workflow will automatically:

1. **Run comprehensive tests** on Python 3.8-3.12
2. **Build the package** and verify contents
3. **Publish to production PyPI**
4. **Test installation** from PyPI
5. **Create GitHub release** with changelog and artifacts

Monitor the workflow at: `https://github.com/trendpro/cardinity-python/actions`

### Step 5: Verify Release

1. **Check PyPI publication:**
   ```bash
   # Install from PyPI
   pip install cardinity-python==1.2.0
   
   # Verify installation
   python -c "import cardinity; print(cardinity.__version__)"
   ```

2. **Check GitHub release:**
   - Visit: `https://github.com/trendpro/cardinity-python/releases`
   - Verify release notes and attached files

## Pre-release Testing

For testing the release process without publishing to production:

### 1. Create Pre-release Tag
```bash
# Create pre-release tag
git tag v1.2.0-rc1
git push origin v1.2.0-rc1
```

### 2. Manual Testing Only
```bash
# Run pre-release workflow manually
# Go to: Actions → Pre-Release Testing → Run workflow
```

This will:
- Run all tests and validations
- Build the package
- Simulate the upload process
- Verify package contents
- Run security checks

## Manual Release (Emergency)

If automated release fails, you can manually release:

### 1. Prepare Package
```bash
# Clean and build
rm -rf dist/
uv build

# Verify contents
ls -la dist/
python -m zipfile -l dist/*.whl
```

### 2. Upload to Production PyPI
```bash
# Upload to production PyPI
uv publish --token $PYPI_API_TOKEN

# Test installation
pip install cardinity-python==1.2.0
```

## Troubleshooting

### Common Issues

1. **Version Mismatch**
   - Ensure version is updated in both `pyproject.toml` and `cardinity/__init__.py`
   - Use the preparation script to avoid manual errors

2. **Authentication Errors**
   - Verify API tokens are correctly set in GitHub secrets
   - Check token permissions and expiration

3. **Package Build Fails**
   - Run `uv build` locally to debug
   - Check for missing files or incorrect paths

4. **Tests Fail**
   - Run full test suite locally: `uv run pytest --cov`
   - Fix any failing tests before releasing

5. **Upload Fails**
   - Check if version already exists on PyPI
   - Verify package name and metadata

### Workflow Debugging

1. **Check Action Logs**
   - Go to Actions tab in GitHub
   - Click on failed workflow
   - Review step-by-step logs

2. **Test Locally**
   - Run the same commands from the workflow locally
   - Use the pre-release workflow for testing

3. **Verify Secrets**
   - Ensure secrets are correctly set in repository settings
   - Test tokens work by running manual uploads

## Version Management

### Semantic Versioning

Follow semantic versioning (semver.org):
- `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
- `MAJOR.MINOR.PATCH-PRERELEASE` (e.g., `1.2.3-rc1`)

### Version Increment Guidelines

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)
- **PRERELEASE**: Testing versions (`-alpha`, `-beta`, `-rc`)

## Security Considerations

1. **API Tokens**
   - Use project-scoped tokens when possible
   - Rotate tokens regularly
   - Never commit tokens to repository

2. **Release Validation**
   - Always validate packages thoroughly before production
   - Verify package contents before production
   - Monitor for security vulnerabilities

3. **Access Control**
   - Use GitHub environment protection rules
   - Require approval for production releases
   - Limit who can create releases

## Documentation

### Building Documentation Locally

The project uses Sphinx for documentation generation with the Read the Docs theme.

#### Quick Start
```bash
# Build documentation
make docs

# Serve documentation locally at http://localhost:8000
make docs-serve

# View in browser
open http://localhost:8000
```

#### Alternative Methods
```bash
# Direct sphinx-build command
uv run sphinx-build docs docs/_build

# Or navigate to docs directory
cd docs && uv run make html

# Manual serving
cd docs/_build/html && python -m http.server 8000
```

#### Documentation Commands
- `make docs` - Build HTML documentation
- `make docs-serve` - Serve documentation locally
- `make docs-clean` - Clean documentation build artifacts

#### Documentation Dependencies
Documentation dependencies are included in the `dev` extra:
```bash
# Install with documentation dependencies
uv sync --extra dev
```

### Read the Docs Integration

The project is configured for automatic documentation building on Read the Docs:

#### Configuration Files
- `.readthedocs.yaml` - Read the Docs configuration
- `docs/conf.py` - Sphinx configuration
- `pyproject.toml` - Python dependencies (dev extras)

#### Automatic Builds
- **Triggered by**: Git pushes to main branch and tags
- **Build environment**: Ubuntu 22.04, Python 3.11  
- **Output formats**: HTML, PDF, ePub
- **URL**: https://cardinity-python.readthedocs.io/

#### Read the Docs Features
- Automatic version management
- Multi-format output (HTML, PDF, ePub)
- Search functionality
- Version switching
- GitHub integration

### Documentation in Release Process

Documentation is automatically updated during releases:

#### Pre-Release Documentation Check
```bash
# Build and verify documentation
make docs

# Check for warnings or errors
# Documentation should build without warnings

# Review generated documentation
make docs-serve
```

#### Release Documentation Steps
1. **Version Update**: Documentation version is automatically updated from `pyproject.toml`
2. **API Changes**: Ensure any API changes are documented
3. **Examples**: Update examples if new features are added
4. **Changelog**: Update CHANGELOG.md with documentation changes

#### Verifying Documentation

After each release, verify:
1. **Read the Docs Build**: Check https://readthedocs.org/projects/cardinity-python/
2. **Version Display**: Ensure new version appears in documentation
3. **Links**: Verify internal and external links work
4. **Examples**: Test code examples in documentation
5. **API Reference**: Check auto-generated API documentation

#### Documentation Structure
```
docs/
├── _build/          # Generated documentation (local)
├── _static/         # Static files (CSS, images)
├── _templates/      # Custom templates
├── api.rst          # API reference
├── authentication.rst
├── conf.py          # Sphinx configuration
├── examples/
├── index.rst        # Main documentation page
├── installation.rst
├── migration.rst
└── quickstart.rst
```

#### Troubleshooting Documentation

Common documentation issues:

1. **Build Warnings**
   ```bash
   # Check for and fix warnings
   make docs
   # Review output for warnings
   ```

2. **Missing Dependencies**
   ```bash
   # Install documentation dependencies
   uv sync --extra dev
   ```

3. **Read the Docs Build Failures**
   - Check `.readthedocs.yaml` configuration
   - Verify Python version compatibility
   - Check dependency specification in `pyproject.toml`

4. **API Documentation Issues**
   - Ensure modules are importable
   - Check docstring formatting
   - Verify Sphinx autodoc configuration

## Post-Release Tasks

1. **Update Documentation**
   - Verify Read the Docs build completed successfully
   - Check documentation reflects new version
   - Update API documentation if needed
   - Update example code with new features
   - Review and update any outdated documentation

2. **Communicate Release**
   - Announce on relevant channels
   - Update project README if needed
   - Close related GitHub issues
   - Update documentation links if needed

3. **Monitor**
   - Watch for installation issues
   - Monitor PyPI download statistics
   - Monitor Read the Docs build status
   - Address any reported issues promptly

## Rollback Procedure

If a release has critical issues:

1. **Immediate**: Yank the problematic version from PyPI
   ```bash
   # This doesn't delete but prevents new installations
   uv publish --skip-existing --verbose
   ```

2. **Follow-up**: Release a patch version with fixes
   ```bash
   python scripts/prepare-release.py 1.2.1
   ```

3. **Communication**: Notify users of the issue and fix
