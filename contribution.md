# Contributing to CodeSec CLI

First off, thank you for considering contributing to CodeSec CLI! It's people like you that make CodeSec CLI such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for CodeSec CLI.

#### Before Submitting A Bug Report

* Check the [issues](https://github.com/samar-d-coder/codesec/issues) to see if the problem has already been reported.
* Update to the latest version of CodeSec CLI to see if the problem persists.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as GitHub issues. Create an issue and provide the following information:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if applicable

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for CodeSec CLI.

#### Before Submitting An Enhancement Suggestion

* Check if there's already a feature that provides your suggested functionality.
* Check if the suggestion has already been made in the issues.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide the following information:

* Use a clear and descriptive title
* Provide a detailed description of the suggested enhancement
* Provide specific examples to demonstrate the proposal
* Describe the current behavior and explain the behavior you'd like to see instead
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Include screenshots in your pull request whenever possible
* Follow the Python code style
* Include tests for new features
* Document new code
* End all files with a newline

## Development Process

1. Fork the repository
2. Create a new branch for your feature/fix
3. Write your code
4. Write tests for your code
5. Run the test suite
6. Push your branch and submit a pull request

### Development Setup

1. Clone your fork
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests:
   ```bash
   pytest tests/
   ```

### Code Style

* Follow PEP 8
* Use type hints
* Write docstrings for functions and classes
* Keep functions focused and modular
* Comment complex logic

## Project Structure

```
codesec-cli/
│
├── codesec/              # Main package
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── scanner.py       # Security scanning
│   ├── explorer.py      # Code exploration
│   └── reports.py       # Report generation
│
├── tests/               # Test suite
│   └── test_codesec.py
│
├── docs/                # Documentation
│   └── screenshots/     # UI screenshots
│
└── examples/            # Example code
```

## Questions?

Feel free to open an issue with your question or contact the maintainers directly.