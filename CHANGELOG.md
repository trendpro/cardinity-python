# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-06-30

### Added
- New features and improvements

### Changed
- Updated documentation configs for pypi and readthedocs

### Fixed
- Bug fixes and stability improvements

## [1.0.1] - 2025-06-29

### Changed
- Updated documentations

### Fixed
- Bug fixes and stability improvements

## [1.0.0-rc4] - 2025-06-20

### Added
- New features and improvements

### Changed
- Updated dependencies and improvements

### Fixed
- Bug fixes and stability improvements

## [1.0.0-rc3] - 2025-06-20

### Added
- New features and improvements

### Changed
- Updated dependencies and improvements

### Fixed
- Bug fixes and stability improvements

## [1.0.0-rc2] - 2025-06-20

### Added
- Prepping for release

### Changed
- Updated dependencies and improvements

### Fixed
- Bug fixes and stability improvements

## [1.0.0-rc1] - 2025-06-20

### Added
- Prepping for release

### Changed
- Updated dependencies and improvements

### Fixed
- Bug fixes and stability improvements

## [Unreleased]

### Added
- Automated PyPI publishing with GitHub Actions
- Direct-to-production publishing pipeline
- Pre-release testing workflow
- Release preparation script
- Comprehensive release documentation
- GitHub issue and PR templates

### Changed
- Enhanced CI/CD pipeline with security checks
- Improved package validation process
- Streamlined release process for direct PyPI publishing

## [1.0.0] - 2024-01-15

### Added
- Initial release of Cardinity Python SDK
- Complete feature parity with Node.js SDK
- Support for Python 3.8+
- OAuth 1.0 HMAC-SHA1 authentication
- All Cardinity API operations:
  - Payment creation and processing
  - 3D Secure v1 and v2 authentication
  - Recurring payments
  - Refunds and settlements
  - Payment voids
  - Chargeback retrieval
  - Payment links with expiration handling
- Comprehensive validation system with constraints
- HTTP client with retry logic and error handling
- Type hints and full MyPy compatibility
- 171 unit tests with 92% coverage
- Complete Sphinx documentation
- Working examples for all operations

### Security
- Secure OAuth 1.0 signature generation
- Proper credential handling without leakage
- Input validation and sanitization 
