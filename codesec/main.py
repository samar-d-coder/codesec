import sys
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DirectoryTree, Static
from textual.containers import Horizontal, Vertical
from rich.syntax import Syntax
from .scanner import SecurityScanner
from .reports import ReportGenerator


class CodeView(Static):
    """A widget to display code with syntax highlighting."""
    def __init__(self) -> None:
        super().__init__("")
        self.code = ""

    def update_code(self, path: Path) -> None:
        """Update the displayed code."""
        try:
            syntax = Syntax.from_path(
                path,
                line_numbers=True,
                word_wrap=True,
                indent_guides=True,
                theme="monokai"
            )
            self.update(syntax)
        except Exception as e:
            self.update(f"Error loading file: {e}")


class SecurityPanel(Static):
    """Display security scan results."""
    def __init__(self) -> None:
        super().__init__("")
        self.scanner = SecurityScanner()

    def scan_file(self, path: Path) -> None:
        """Scan a file and display results."""
        issues = self.scanner.scan_file(path)
        if issues:
            self.update("\n".join(f"⚠️ {issue['message']}" for issue in issues))
        else:
            self.update("✅ No security issues found")


class CodeSecApp(App):
    """Main CodeSec CLI application."""
    BINDINGS = [("q", "quit", "Quit"), ("r", "refresh_scan", "Refresh Security Scan")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield DirectoryTree(".", id="tree")
            with Vertical():
                yield CodeView()
                yield SecurityPanel()
        yield Footer()

    def __init__(self):
        super().__init__()
        self.scanner = SecurityScanner()
        self.suspicious_files = set()

    def on_mount(self) -> None:
        """Scan everything on app start."""
        self.scan_workspace()

    def scan_workspace(self) -> None:
        """Scan the entire workspace recursively."""
        tree = self.query_one("#tree", DirectoryTree)
        security_panel = self.query_one(SecurityPanel)

        self.suspicious_files.clear()
        root_path = Path.cwd()

        for path in root_path.rglob("*"):
            if path.is_file():
                try:
                    issues = self.scanner.scan_file(path)
                    if issues:
                        self.suspicious_files.add(str(path))
                except Exception as e:
                    print(f"Error scanning {path}: {e}", file=sys.stderr)

        # Display results
        if self.suspicious_files:
            msg = f"⚠️ Found {len(self.suspicious_files)} files with potential security issues:\n" + \
                  "\n".join(f"- {Path(f).name}" for f in self.suspicious_files)
            security_panel.update(msg)
            self.notify(f"Security scan complete: {len(self.suspicious_files)} vulnerable files found!", severity="warning")
        else:
            security_panel.update("✅ No security issues found in workspace")
            self.notify("Security scan complete: No security issues found!", severity="info")

    def action_refresh_scan(self) -> None:
        """Manually refresh scan."""
        self.scan_workspace()

    def on_directory_tree_file_selected(self, event):
        """When a file is selected from the tree, show code and scan that file."""
        path = Path(event.path)
        code_view = self.query_one(CodeView)
        security_panel = self.query_one(SecurityPanel)
        code_view.update_code(path)
        security_panel.scan_file(path)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="CodeSec CLI - Security and Privacy Analyzer")
    parser.add_argument("path", nargs="?", help="Path to analyze", type=Path, default=Path.cwd())
    parser.add_argument("--report", help="Generate report file", type=Path)

    args = parser.parse_args()

    if args.report:
        # Run report mode
        scanner = SecurityScanner()
        report_gen = ReportGenerator()
        issues = scanner.scan_file(args.path)
        report_gen.generate_markdown({"issues": issues}, args.report)
    else:
        # Launch TUI
        app = CodeSecApp()
        app.run()


if __name__ == "__main__":
    main()
