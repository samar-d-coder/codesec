# CodeSec CLI

A powerful terminal-based tool that combines codebase exploration with privacy and security analysis.

## Features

- 🔍 **Code Exploration**

  - File tree with keyboard navigation
  - Fuzzy search for files and functions
  - Syntax-highlighted code viewer
  - Interactive ASCII call graph visualization
- 🔒 **Security Analysis**

  - Detection of hard-coded credentials (AWS keys, API tokens)
  - Browser credential file scanning
  - Suspicious domain detection in JS files
  - Plaintext storage scanning
- 📊 **Reporting**

  - Interactive TUI summary panel
  - Exportable audit reports (JSON/Markdown)
  - Severity-based issue categorization

## Installation

CodeSec CLI requires Python 3.10 or later.


### From Source

```bash
git clone https://github.com/samar-d-coder/codesec.git
cd codesec
pip install -e .
```

## Usage

Start the TUI application:

```bash
codesec .
```

### Keyboard Shortcuts

- `↑`/`↓`: Navigate file tree
- `Enter`: Select file/directory
- `Tab`: Switch between panels
- `Q`: Quit

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/samar-d-coder/codesec.git
   cd codesec
   ```
2. Create and activate a virtual environment:

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests:

   ```bash
   pytest tests/
   ```

## Screenshots

![Main Interface](docs/screenshots/main.png)
*Main interface showing file tree, code viewer, and security panel*

![Security Scan](docs/screenshots/run.png)
*Security scan results with highlighted issues*

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.


## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

## Acknowledgments

- [Textual](https://github.com/Textualize/textual) - TUI framework
- [Rich](https://github.com/Textualize/rich) - Terminal formatting
- [tree-sitter](https://github.com/tree-sitter/py-tree-sitter) - Code parsing
