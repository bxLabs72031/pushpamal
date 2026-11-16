# Changelog

All notable changes to PushpAmal will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-11-14
### Added
- Initial release with version 0.1.0
- Bootstrap compiler verification (14/14 test suite passing)
- 7 example programs (quine, sieve, matrix, factorial, numbers, prime, stress_ub)
- REPL with 7 commands (.run, .clear, .help, .exit, .history, .undo, .graphic)
- Debugger with step-through execution, registers, memory inspection
- Standard library: Math, IO, String, Dict modules
- Comprehensive tutorial documentation (10 sections, PUSHAMAL_TUTORIAL.md)
- Packaging files: setup.py, pyproject.toml, MANIFEST.in, README, LICENSE, badge.svg
- PyPI packaging workarounds documented (setuptools/Python 3.12 compatibility)

### Changed
- pyproject.toml updated with setuptools version range for Python 3.12 compatibility
- PROJECT STRUCTURE reorganized for clarity

### Deprecated
- None

### Fixed
- PyPI packaging setuptools/Python 3.12 compatibility issue
- Bootstrap compiler test verification

### Security
- None

## [0.0.1] - 2026-11-13
### Added
- Initial project setup
- Core language with 80+ opcodes
- PushpAmal assembly and VM execution
- First release at version 0.0.1