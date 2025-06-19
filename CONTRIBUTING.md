# Contributing to Cardinity Python SDK

We welcome contributions to the Cardinity Python SDK! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct. Please treat all contributors with respect and create a welcoming environment for everyone.

## Getting Started

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cardinity/cardinity-python.git
   cd cardinity-python
   ```

2. **Install Python 3.8+:**
   - Make sure you have Python 3.8 or later installed
   - We recommend using `pyenv` for Python version management

3. **Install uv (recommended) or use pip:**
   ```bash
   # Using uv (faster, recommended)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv sync --all-extras

   # Or using pip
   pip install -e .[dev,test,docs]
   ```

4. **Set up pre-commit hooks:**
   ```bash
   uv run pre-commit install
   ```

### Project Structure

```
cardinity-python/
├── cardinity/           # Main SDK package
│   ├── __init__.py     # Public API exports
│   ├── auth.py         # OAuth authentication
│   ├── client.py       # HTTP client
│   ├── exceptions.py   # Custom exceptions
│   ├── sdk.py          # Main SDK class
│   ├── models/         # Data models
│   ├── validation/     # Input validation
│   └── utils/          # Utility functions
├── examples/           # Usage examples
├── docs/               # Sphinx documentation
├── tests/              # Test suite
│   ├── fixtures/       # Test data
│   ├── integration/    # Integration tests
│   └── unit/           # Unit tests
├── pyproject.toml      # Project configuration
└── README.md
```

## Development Workflow

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clear, readable code
   - Follow existing code style and patterns
   - Add docstrings to public methods
   - Update type hints as needed

3. **Add tests:**
   - Write unit tests for new functionality
   - Add integration tests if applicable
   - Ensure all tests pass: `uv run pytest`

4. **Update documentation:**
   - Add docstrings to new public APIs
   - Update examples if needed
   - Build docs to verify: `uv run sphinx-build docs docs/_build`

5. **Run quality checks:**
   ```bash
   # Run all tests
   uv run pytest

   # Run type checking
   uv run mypy cardinity

   # Run linting
   uv run ruff check .

   # Run formatting
   uv run black .
   ```

### Submitting Changes

1. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

2. **Use conventional commit format:**
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring
   - `chore:` for maintenance tasks

3. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request:**
   - Use a clear, descriptive title
   - Explain what the change does and why
   - Link to any relevant issues
   - Ensure CI passes

## Testing Guidelines

### Test Types

1. **Unit Tests** (`tests/unit/`)
   - Test individual functions and classes
   - Mock external dependencies
   - Fast execution
   - High coverage

2. **Integration Tests** (`tests/integration/`)
   - Test real API interactions
   - Use test credentials
   - Validate complete workflows
   - May be slower

3. **Performance Tests** (`tests/unit/test_performance.py`)
   - Test SDK performance metrics
   - Memory usage validation
   - Concurrent request handling

### Writing Tests

```python
import pytest
from cardinity import Cardinity, APIError

def test_payment_creation():
    """Test payment creation with valid data."""
    client = Cardinity(
        consumer_key="test_key",
        consumer_secret="test_secret"
    )
    
    # Test implementation
    assert result is not None

def test_payment_creation_error():
    """Test payment creation with invalid data."""
    with pytest.raises(APIError):
        # Test error scenario
        pass
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_client.py

# Run with coverage
uv run pytest --cov=cardinity

# Run integration tests only
uv run pytest -m integration

# Run performance tests
uv run pytest -m performance
```

## Code Style Guidelines

### Python Style

- Follow PEP 8 conventions
- Use `black` for code formatting
- Use `ruff` for linting
- Maximum line length: 88 characters
- Use type hints for all public APIs

### Naming Conventions

- **Classes:** `PascalCase` (e.g., `PaymentModel`)
- **Functions/Methods:** `snake_case` (e.g., `create_payment`)
- **Variables:** `snake_case` (e.g., `payment_id`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `API_BASE_URL`)
- **Private members:** Leading underscore (e.g., `_internal_method`)

### Documentation

- All public classes and methods must have docstrings
- Use Google-style docstrings
- Include type information in docstrings
- Provide examples for complex APIs

```python
def create_payment(
    self,
    amount: str,
    currency: str,
    description: str,
    **kwargs
) -> Dict[str, Any]:
    """Create a new payment.
    
    Args:
        amount: Payment amount as decimal string (e.g., "10.00")
        currency: Three-letter currency code (e.g., "EUR")
        description: Payment description
        **kwargs: Additional payment parameters
        
    Returns:
        Dictionary containing payment data
        
    Raises:
        ValidationError: If input parameters are invalid
        APIError: If API request fails
        
    Example:
        >>> client = Cardinity(consumer_key="key", consumer_secret="secret")
        >>> payment = client.create_payment(
        ...     amount="10.00",
        ...     currency="EUR",
        ...     description="Test payment"
        ... )
    """
```

## API Design Guidelines

### Method Naming

- Use descriptive, action-oriented names
- Follow the pattern: `verb_noun` (e.g., `create_payment`, `get_refund`)
- Be consistent with naming patterns

### Parameter Design

- Use keyword arguments for optional parameters
- Provide sensible defaults where possible
- Validate input parameters early
- Use type hints consistently

### Error Handling

- Create specific exception types for different error categories
- Provide clear error messages
- Include relevant context in exceptions
- Document all exceptions that methods can raise

### Return Values

- Return dictionaries for API responses
- Be consistent with return types
- Document return value structure
- Include examples in docstrings

## Documentation

### Building Documentation

```bash
# Install documentation dependencies
uv sync --extra docs

# Build documentation
uv run sphinx-build docs docs/_build

# Serve documentation locally
uv run python -m http.server 8000 --directory docs/_build
```

### Documentation Structure

- **Installation:** Setup and installation instructions
- **Quick Start:** Basic usage examples
- **API Reference:** Complete API documentation
- **Examples:** Comprehensive usage examples
- **Migration Guide:** Node.js to Python migration
- **Contributing:** This document

## Release Process

### Version Management

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Update version in `pyproject.toml`
- Create git tags for releases
- Maintain CHANGELOG.md

### Release Checklist

1. **Pre-release:**
   - [ ] All tests pass
   - [ ] Documentation is up to date
   - [ ] Version number updated
   - [ ] CHANGELOG.md updated

2. **Release:**
   - [ ] Create git tag
   - [ ] Build package: `uv build`
   - [ ] Upload to PyPI: `uv publish`
   - [ ] Create GitHub release

3. **Post-release:**
   - [ ] Update documentation
   - [ ] Announce release
   - [ ] Update examples

## Issue and PR Templates

### Bug Reports

When reporting bugs, please include:

- Python version
- SDK version
- Minimal code example
- Expected vs actual behavior
- Error messages and stack traces

### Feature Requests

When requesting features, please include:

- Clear description of the feature
- Use case and motivation
- Proposed API design (if applicable)
- Backward compatibility considerations

### Pull Request Guidelines

- Link to relevant issue(s)
- Describe changes made
- Include test coverage
- Update documentation as needed
- Ensure CI passes

## Getting Help

- **Issues:** Use GitHub issues for bugs and feature requests
- **Discussions:** Use GitHub discussions for questions
- **Email:** Contact support at support@cardinity.com

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- GitHub contributors list
- Documentation acknowledgments (for major contributions)

Thank you for contributing to the Cardinity Python SDK! 
