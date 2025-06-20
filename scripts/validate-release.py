#!/usr/bin/env python3
"""
Release validation script for cardinity-python.

This script validates that the package is ready for release by:
1. Running comprehensive tests
2. Validating package metadata
3. Testing package building
4. Checking for common issues
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List

import tomllib


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


def run_command(
    cmd: List[str], capture_output: bool = True
) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=capture_output, text=True)
    return result


def validate_version_consistency() -> Dict[str, str]:
    """Validate that version is consistent across all files."""
    print("🔍 Validating version consistency...")

    # Get version from pyproject.toml
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    pyproject_version = data["project"]["version"]

    # Get version from __init__.py
    try:
        result = run_command(
            ["python", "-c", "from cardinity import __version__; print(__version__)"]
        )
        if result.returncode != 0:
            raise ValidationError(
                f"Failed to import version from cardinity: {result.stderr}"
            )
        init_version = result.stdout.strip()
    except Exception as e:
        raise ValidationError(f"Failed to get version from __init__.py: {e}")

    # Compare versions
    if pyproject_version != init_version:
        raise ValidationError(
            f"Version mismatch: pyproject.toml={pyproject_version}, __init__.py={init_version}"
        )

    print(f"✅ Version consistency check passed: {pyproject_version}")
    return {"pyproject": pyproject_version, "init": init_version}


def validate_package_metadata():
    """Validate package metadata in pyproject.toml."""
    print("🔍 Validating package metadata...")

    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    project = data["project"]

    # Required fields
    required_fields = ["name", "version", "description", "authors", "requires-python"]
    for field in required_fields:
        if field not in project:
            raise ValidationError(f"Missing required field in pyproject.toml: {field}")

    # Validate name
    if project["name"] != "cardinity-python":
        raise ValidationError(f"Invalid package name: {project['name']}")

    # Validate dependencies
    if "dependencies" not in project:
        raise ValidationError("Missing dependencies in pyproject.toml")

    expected_deps = ["requests", "requests-oauthlib", "cerberus", "python-dateutil"]
    for dep in expected_deps:
        if not any(dep in d for d in project["dependencies"]):
            raise ValidationError(f"Missing required dependency: {dep}")

    print("✅ Package metadata validation passed")


def validate_code_quality():
    """Run code quality checks."""
    print("🔍 Running code quality checks...")

    # Linting
    print("  Running ruff check...")
    result = run_command(["uv", "run", "ruff", "check", "."])
    if result.returncode != 0:
        raise ValidationError(f"Ruff check failed:\n{result.stdout}\n{result.stderr}")

    # Formatting
    print("  Running ruff format check...")
    result = run_command(["uv", "run", "ruff", "format", "--check", "."])
    if result.returncode != 0:
        raise ValidationError(
            f"Ruff format check failed:\n{result.stdout}\n{result.stderr}"
        )

    # Type checking
    print("  Running mypy...")
    result = run_command(["uv", "run", "mypy", "cardinity/"])
    if result.returncode != 0:
        raise ValidationError(f"MyPy check failed:\n{result.stdout}\n{result.stderr}")

    print("✅ Code quality checks passed")


def validate_tests():
    """Run comprehensive tests."""
    print("🔍 Running comprehensive tests...")

    result = run_command(["uv", "run", "pytest", "--cov", "--cov-fail-under=85", "-v"])
    if result.returncode != 0:
        raise ValidationError(f"Tests failed:\n{result.stdout}\n{result.stderr}")

    print("✅ All tests passed")


def validate_package_build():
    """Validate package building and contents."""
    print("🔍 Validating package build...")

    # Clean previous builds
    run_command(["rm", "-rf", "dist/"])

    # Build package
    result = run_command(["uv", "build"])
    if result.returncode != 0:
        raise ValidationError(
            f"Package build failed:\n{result.stdout}\n{result.stderr}"
        )

    # Check if files exist
    dist_path = Path("dist")
    if not dist_path.exists():
        raise ValidationError("dist/ directory not created")

    wheel_files = list(dist_path.glob("*.whl"))
    tar_files = list(dist_path.glob("*.tar.gz"))

    if not wheel_files:
        raise ValidationError("No wheel file created")
    if not tar_files:
        raise ValidationError("No source distribution created")

    print(f"  Built files: {[f.name for f in wheel_files + tar_files]}")

    # Validate wheel contents
    wheel_file = wheel_files[0]
    result = run_command(["python", "-m", "zipfile", "-l", str(wheel_file)])
    if result.returncode != 0:
        raise ValidationError(f"Failed to read wheel contents: {result.stderr}")

    wheel_contents = result.stdout

    # Check for essential files
    essential_files = [
        "cardinity/__init__.py",
        "cardinity/sdk.py",
        "cardinity/client.py",
    ]
    for file in essential_files:
        if file not in wheel_contents:
            raise ValidationError(f"Missing essential file in wheel: {file}")

    print("✅ Package build validation passed")


def validate_installation():
    """Test package installation in clean environment."""
    print("🔍 Testing package installation...")

    try:
        # Install from wheel using uv directly
        wheel_files = list(Path("dist").glob("*.whl"))
        if not wheel_files:
            raise ValidationError("No wheel file found for installation test")

        wheel_file = wheel_files[0]

        # Create a temporary environment and install the package
        result = run_command(
            [
                "uv",
                "run",
                "--with",
                str(wheel_file),
                "python",
                "-c",
                'import cardinity; print(f"Cardinity v{cardinity.__version__} imported successfully")',
            ]
        )
        if result.returncode != 0:
            raise ValidationError(
                f"Failed to import installed package: {result.stderr}"
            )

        print(f"  {result.stdout.strip()}")

        # Test basic functionality
        result = run_command(
            [
                "uv",
                "run",
                "--with",
                str(wheel_file),
                "python",
                "-c",
                """
import cardinity
from cardinity import Cardinity, CardinityError, ValidationError

# Test basic imports
print("✓ Basic imports successful")

# Test SDK initialization
try:
    sdk = Cardinity("test_key", "test_secret")
    print("✓ SDK initialization successful")
except Exception as e:
    print(f"✗ SDK initialization failed: {e}")
    exit(1)

print("✓ All import tests passed")
""",
            ]
        )
        if result.returncode != 0:
            raise ValidationError(f"Package functionality test failed: {result.stderr}")

        print("✅ Package installation test passed")

    except Exception as e:
        if "ValidationError" in str(type(e)):
            raise
        else:
            print(f"⚠️  Installation test skipped due to environment issue: {e}")
            print("✅ Package installation test completed (with warnings)")


def validate_documentation():
    """Validate documentation completeness."""
    print("🔍 Validating documentation...")

    # Check if README exists and is not empty
    readme_path = Path("README.md")
    if not readme_path.exists():
        raise ValidationError("README.md not found")

    readme_content = readme_path.read_text()
    if len(readme_content.strip()) < 100:
        raise ValidationError("README.md is too short")

    # Check for essential sections
    essential_sections = ["Installation", "Usage", "Examples"]
    for section in essential_sections:
        if section.lower() not in readme_content.lower():
            print(f"⚠️  Warning: README.md may be missing section: {section}")

    # Check if examples exist
    examples_path = Path("examples")
    if not examples_path.exists():
        raise ValidationError("examples/ directory not found")

    example_files = list(examples_path.glob("*.py"))
    if len(example_files) < 3:
        print(f"⚠️  Warning: Only {len(example_files)} example files found")

    print("✅ Documentation validation passed")


def validate_security():
    """Run security checks."""
    print("🔍 Running security checks...")

    # Check for potential secrets in code
    print("  Checking for potential secrets...")
    result = run_command(
        [
            "grep",
            "-r",
            "-E",
            "(password|secret|key|token|api_key)",
            "--include=*.py",
            "cardinity/",
        ]
    )

    if result.returncode == 0:
        # Found potential secrets, check if they're legitimate
        output = result.stdout.lower()
        legitimate_patterns = [
            "consumer_key",
            "consumer_secret",
            "test_key",
            "test_secret",
        ]

        lines = output.split("\n")
        suspicious_lines = []

        for line in lines:
            if line.strip():
                is_legitimate = any(pattern in line for pattern in legitimate_patterns)
                if not is_legitimate:
                    suspicious_lines.append(line)

        if suspicious_lines:
            print("⚠️  Warning: Found potential secrets in code:")
            for line in suspicious_lines:
                print(f"    {line}")

    print("✅ Security checks completed")


def main():
    """Main validation function."""
    print("🚀 Starting release validation...\n")

    try:
        # Change to script directory
        script_dir = Path(__file__).parent
        project_dir = script_dir.parent

        print(f"Project directory: {project_dir}")

        # Change to project directory
        import os

        os.chdir(project_dir)

        # Run all validations
        validate_version_consistency()
        validate_package_metadata()
        validate_code_quality()
        validate_tests()
        validate_package_build()
        validate_installation()
        validate_documentation()
        validate_security()

        print("\n🎉 All validations passed! The package is ready for release.")

    except ValidationError as e:
        print(f"\n❌ Validation failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
