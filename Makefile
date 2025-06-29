# Cardinity Python SDK Makefile
# Provides convenient commands for development and release

.PHONY: help install test lint format type-check build clean validate-release prepare-release
.DEFAULT_GOAL := help

# Colors for pretty output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Cardinity Python SDK - Available Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	@echo "$(GREEN)Installing dependencies...$(NC)"
	uv sync --dev

install-prod: ## Install production dependencies only
	@echo "$(GREEN)Installing production dependencies...$(NC)"
	uv sync

test: ## Run tests
	@echo "$(GREEN)Running tests...$(NC)"
	uv run pytest

test-cov: ## Run tests with coverage
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	uv run pytest --cov --cov-report=term-missing

test-cov-html: ## Run tests with HTML coverage report
	@echo "$(GREEN)Running tests with HTML coverage report...$(NC)"
	uv run pytest --cov --cov-report=html
	@echo "$(GREEN)Coverage report available at htmlcov/index.html$(NC)"

lint: ## Run linting
	@echo "$(GREEN)Running linting...$(NC)"
	uv run ruff check .

lint-fix: ## Run linting with auto-fix
	@echo "$(GREEN)Running linting with auto-fix...$(NC)"
	uv run ruff check . --fix

format: ## Format code
	@echo "$(GREEN)Formatting code...$(NC)"
	uv run ruff format .

format-check: ## Check code formatting
	@echo "$(GREEN)Checking code formatting...$(NC)"
	uv run ruff format --check .

type-check: ## Run type checking
	@echo "$(GREEN)Running type checking...$(NC)"
	uv run mypy cardinity/

quality: lint format-check type-check ## Run all code quality checks
	@echo "$(GREEN)All code quality checks completed!$(NC)"

build: ## Build package
	@echo "$(GREEN)Building package...$(NC)"
	uv build

build-clean: clean build ## Clean and build package
	@echo "$(GREEN)Package built successfully!$(NC)"

clean: ## Clean build artifacts
	@echo "$(GREEN)Cleaning build artifacts...$(NC)"
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

validate-release: ## Validate package is ready for release
	@echo "$(GREEN)Validating release readiness...$(NC)"
	python scripts/validate-release.py

prepare-release: ## Prepare a new release (usage: make prepare-release VERSION=1.2.0)
	@if [ -z "$(VERSION)" ]; then \
		echo "$(RED)Error: VERSION is required. Usage: make prepare-release VERSION=1.2.0$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Preparing release $(VERSION)...$(NC)"
	python scripts/prepare-release.py $(VERSION)

docs: ## Build documentation
	@echo "$(GREEN)Building documentation...$(NC)"
	uv run sphinx-build docs docs/_build

docs-serve: docs ## Serve documentation locally
	@echo "$(GREEN)Serving documentation at http://localhost:8000$(NC)"
	@echo "$(GREEN)Open http://localhost:8000 in your browser$(NC)"
	cd docs/_build && python -m http.server 8000

docs-clean: ## Clean documentation build
	@echo "$(GREEN)Cleaning documentation...$(NC)"
	rm -rf docs/_build

examples: ## Run all examples
	@echo "$(GREEN)Running examples...$(NC)"
	@for example in examples/*.py; do \
		echo "Running $$example..."; \
		uv run python "$$example" || true; \
	done

security: ## Run security checks
	@echo "$(GREEN)Running security checks...$(NC)"
	uv run safety check --json || true

performance: ## Run performance tests
	@echo "$(GREEN)Running performance tests...$(NC)"
	uv run pytest tests/unit/test_performance.py -v

# Development workflow commands
dev-setup: install ## Complete development setup
	@echo "$(GREEN)Development environment setup complete!$(NC)"

dev-test: quality test-cov ## Run full development test suite
	@echo "$(GREEN)All development tests completed!$(NC)"

# Release workflow commands
pre-release-test: quality test-cov validate-release build ## Run pre-release validation
	@echo "$(GREEN)Pre-release validation completed successfully!$(NC)"

# CI/CD simulation commands
ci-test: ## Simulate CI testing
	@echo "$(GREEN)Simulating CI testing...$(NC)"
	@echo "Testing on Python $(shell python --version)"
	$(MAKE) quality
	$(MAKE) test-cov
	$(MAKE) build

# Quick development commands
quick-test: ## Quick test run (no coverage)
	@echo "$(GREEN)Running quick tests...$(NC)"
	uv run pytest -x --tb=short

quick-check: ## Quick quality check
	@echo "$(GREEN)Running quick checks...$(NC)"
	uv run ruff check .
	uv run mypy cardinity/

# Package inspection commands
inspect-wheel: build ## Inspect built wheel contents
	@echo "$(GREEN)Inspecting wheel contents...$(NC)"
	@if [ -f dist/*.whl ]; then \
		uv run python -m zipfile -l dist/*.whl; \
	else \
		echo "$(RED)No wheel file found. Run 'make build' first.$(NC)"; \
	fi

inspect-metadata: ## Inspect package metadata
	@echo "$(GREEN)Package metadata:$(NC)"
	@uv run python -c "import tomllib; f=open('pyproject.toml','rb'); data=tomllib.load(f); print(f'Name: {data[\"project\"][\"name\"]}'); print(f'Version: {data[\"project\"][\"version\"]}'); print(f'Description: {data[\"project\"][\"description\"]}');"

# Version management
version: ## Show current version
	@echo "$(GREEN)Current version:$(NC)"
	@uv run python -c "from cardinity import __version__; print(__version__)"

version-check: ## Check version consistency
	@echo "$(GREEN)Checking version consistency...$(NC)"
	@PYPROJECT_VERSION=$$(uv run python -c "import tomllib; f=open('pyproject.toml','rb'); data=tomllib.load(f); print(data['project']['version'])"); \
	INIT_VERSION=$$(uv run python -c "from cardinity import __version__; print(__version__)"); \
	if [ "$$PYPROJECT_VERSION" = "$$INIT_VERSION" ]; then \
		echo "$(GREEN)✓ Versions match: $$PYPROJECT_VERSION$(NC)"; \
	else \
		echo "$(RED)✗ Version mismatch: pyproject.toml=$$PYPROJECT_VERSION, __init__.py=$$INIT_VERSION$(NC)"; \
		exit 1; \
	fi

# Utility commands
list-deps: ## List all dependencies
	@echo "$(GREEN)Dependencies:$(NC)"
	@uv tree

update-deps: ## Update dependencies
	@echo "$(GREEN)Updating dependencies...$(NC)"
	uv sync --upgrade

size: ## Show package size information
	@echo "$(GREEN)Package size information:$(NC)"
	@if [ -d "dist" ]; then \
		du -sh dist/*; \
	else \
		echo "$(YELLOW)No dist/ directory found. Run 'make build' first.$(NC)"; \
	fi
	@echo "$(GREEN)Source code size:$(NC)"
	@du -sh cardinity/
