#!/usr/bin/env python3
"""
Release preparation script for cardinity-python.

This script helps prepare a new release by:
1. Validating the current state
2. Updating version numbers consistently
3. Updating changelog
4. Running final checks
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import List

import tomllib


def run_command(
    cmd: List[str], capture_output: bool = True
) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=capture_output, text=True)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result


def validate_version_format(version: str) -> bool:
    """Validate that version follows semantic versioning."""
    pattern = r"^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*))?$"
    return bool(re.match(pattern, version))


def get_current_version() -> str:
    """Get current version from pyproject.toml."""
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


def update_pyproject_version(new_version: str):
    """Update version in pyproject.toml."""
    with open("pyproject.toml") as f:
        content = f.read()

    pattern = r'version = "[^"]+"'
    replacement = f'version = "{new_version}"'

    new_content = re.sub(pattern, replacement, content)

    with open("pyproject.toml", "w") as f:
        f.write(new_content)

    print(f"Updated pyproject.toml version to {new_version}")


def update_init_version(new_version: str):
    """Update version in cardinity/__init__.py."""
    init_file = Path("cardinity/__init__.py")

    with open(init_file) as f:
        content = f.read()

    pattern = r'__version__ = "[^"]+"'
    replacement = f'__version__ = "{new_version}"'

    new_content = re.sub(pattern, replacement, content)

    with open(init_file, "w") as f:
        f.write(new_content)

    print(f"Updated cardinity/__init__.py version to {new_version}")


def update_changelog(version: str):
    """Update CHANGELOG.md with new version section."""
    changelog_file = Path("CHANGELOG.md")

    if not changelog_file.exists():
        print("CHANGELOG.md not found, creating one...")
        with open(changelog_file, "w") as f:
            f.write(f"""# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [{version}] - 2024-01-01

### Added
- Initial release of cardinity-python SDK
- Complete feature parity with Node.js SDK
- Support for all Cardinity API operations

""")
        return

    with open(changelog_file) as f:
        content = f.read()

    # Check if version already exists
    if f"## [{version}]" in content:
        print(f"Version {version} already exists in CHANGELOG.md")
        return

    # Find the first occurrence of "## [" and insert new version before it
    lines = content.split("\n")
    new_lines = []
    inserted = False

    for line in lines:
        if line.startswith("## [") and not inserted:
            new_lines.append(
                f"## [{version}] - {subprocess.check_output(['date', '+%Y-%m-%d']).decode().strip()}"
            )
            new_lines.append("")
            new_lines.append("### Added")
            new_lines.append("- New features and improvements")
            new_lines.append("")
            new_lines.append("### Changed")
            new_lines.append("- Updated dependencies and improvements")
            new_lines.append("")
            new_lines.append("### Fixed")
            new_lines.append("- Bug fixes and stability improvements")
            new_lines.append("")
            inserted = True
        new_lines.append(line)

    with open(changelog_file, "w") as f:
        f.write("\n".join(new_lines))

    print(f"Added version {version} section to CHANGELOG.md")
    print("Please edit CHANGELOG.md to add specific changes for this release")


def run_tests():
    """Run comprehensive tests."""
    print("Running comprehensive tests...")

    # Linting
    run_command(["uv", "run", "ruff", "check", "."])
    run_command(["uv", "run", "ruff", "format", "--check", "."])

    # Type checking
    run_command(["uv", "run", "mypy", "cardinity/"])

    # Tests with coverage
    run_command(["uv", "run", "pytest", "--cov", "--cov-fail-under=85"])

    print("✓ All tests passed!")


def build_package():
    """Build the package and verify contents."""
    print("Building package...")

    # Clean previous builds
    run_command(["rm", "-rf", "dist/"])

    # Build package
    run_command(["uv", "build"])

    # List built files
    result = run_command(["ls", "-la", "dist/"])
    print("Built files:")
    print(result.stdout)

    print("✓ Package built successfully!")


def validate_git_state():
    """Validate git repository state."""
    print("Validating git state...")

    # Check if we're on main branch
    result = run_command(["git", "branch", "--show-current"])
    current_branch = result.stdout.strip()

    if current_branch != "main":
        print(f"Warning: Currently on branch '{current_branch}', not 'main'")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != "y":
            sys.exit(1)

    # Check if working directory is clean
    result = run_command(["git", "status", "--porcelain"])
    if result.stdout.strip():
        print("Working directory is not clean. Please commit or stash changes.")
        print("Uncommitted changes:")
        print(result.stdout)
        sys.exit(1)

    # Check if we're up to date with remote
    run_command(["git", "fetch"])
    result = run_command(["git", "log", "HEAD..origin/main", "--oneline"])
    if result.stdout.strip():
        print("Local branch is behind remote. Please pull latest changes.")
        sys.exit(1)

    print("✓ Git state is clean and up to date!")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Prepare a new release")
    parser.add_argument("version", help="New version number (e.g., 1.2.0)")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument(
        "--skip-build", action="store_true", help="Skip building package"
    )
    parser.add_argument(
        "--skip-git-check", action="store_true", help="Skip git validation"
    )

    args = parser.parse_args()

    new_version = args.version

    # Validate version format
    if not validate_version_format(new_version):
        print(f"Invalid version format: {new_version}")
        print("Version should follow semantic versioning (e.g., 1.2.0, 1.2.0-rc1)")
        sys.exit(1)

    # Get current version
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    print(f"New version: {new_version}")

    if current_version == new_version:
        print("New version is the same as current version")
        sys.exit(1)

    # Validate git state
    if not args.skip_git_check:
        validate_git_state()

    # Run tests
    if not args.skip_tests:
        run_tests()

    # Update version numbers
    update_pyproject_version(new_version)
    update_init_version(new_version)

    # Update changelog
    update_changelog(new_version)

    # Build package
    if not args.skip_build:
        build_package()

    print(f"\n✅ Release preparation complete for version {new_version}!")
    print("\nNext steps:")
    print("1. Review and edit CHANGELOG.md with specific changes")
    print("2. Commit the version changes:")
    print("   git add .")
    print(f"   git commit -m 'Prepare release v{new_version}'")
    print("3. Create and push the version tag:")
    print(f"   git tag v{new_version}")
    print("   git push origin main")
    print(f"   git push origin v{new_version}")
    print("4. The GitHub Actions workflow will automatically:")
    print("   - Run tests on all supported Python versions")
    print("   - Build the package")
    print("   - Publish to TestPyPI")
    print("   - Publish to PyPI")
    print("   - Create a GitHub release")


if __name__ == "__main__":
    main()
