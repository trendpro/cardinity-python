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

## Post-Release Tasks

1. **Update Documentation**
   - Update API documentation if needed
   - Update example code with new features

2. **Communicate Release**
   - Announce on relevant channels
   - Update project README if needed
   - Close related GitHub issues

3. **Monitor**
   - Watch for installation issues
   - Monitor PyPI download statistics
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
