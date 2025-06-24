import sys
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DirectoryTree, Static
from textual.containers import Horizontal, Vertical
from rich.syntax import Syntax
from .scanner import SecurityScanner
from .reports import ReportGenerator
from textual.widgets import ListView, ListItem
from textual.message import Message


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
    class IssueSelected(Message):
        def __init__(self, file_path: str):
            self.file_path = file_path
            super().__init__()

    def __init__(self) -> None:
        super().__init__("")
        self.scanner = SecurityScanner()
        self.list_view = ListView()

    def compose(self):
        yield self.list_view

    def update_issues(self, issues_by_file):
        self.list_view.clear()
        if issues_by_file:
            for file_path, issues in issues_by_file.items():
                for issue in issues:
                    item = ListItem(Static(f"⚠️ {Path(file_path).name}: {issue['message']}"))
                    item.issue_path = file_path
                    self.list_view.append(item)
        else:
            self.list_view.append(ListItem(Static("✅ No security issues found in workspace")))

    def on_list_view_selected(self, event):
        selected = event.item
        if hasattr(selected, 'issue_path'):
            self.post_message(self.IssueSelected(selected.issue_path))


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
        issues_by_file = {}
        root_path = Path.cwd()

        for path in root_path.rglob("*"):
            if path.is_file():
                try:
                    issues = self.scanner.scan_file(path)
                    if issues:
                        self.suspicious_files.add(str(path))
                        issues_by_file[str(path)] = issues
                except Exception as e:
                    print(f"Error scanning {path}: {e}", file=sys.stderr)

        # Display results
        security_panel.update_issues(issues_by_file)
        if self.suspicious_files:
            self.notify(f"Security scan complete: {len(self.suspicious_files)} vulnerable files found!", severity="warning")
        else:
            self.notify("Security scan complete: No security issues found!", severity="information")
    
    def on_security_panel_issue_selected(self, message: SecurityPanel.IssueSelected) -> None:
        """Handle when a security issue is selected from the panel."""
        file_path = Path(message.file_path)
        tree = self.query_one("#tree", DirectoryTree)
        code_view = self.query_one(CodeView)
        
        
        code_view.update_code(file_path)
        
        
        try:
            
            tree.select_node(file_path)
        except Exception:
            
            tree.focus()
        
        
        tree_structure = self.format_file_path_as_tree(file_path)
        self.notify(f"File Location:\n{tree_structure}", severity="information")

    def format_file_path_as_tree(self, file_path: Path) -> str:
        """Format file path as a tree structure for notification display."""
        cwd = Path.cwd()
        
        try:
            rel_path = file_path.relative_to(cwd)
            parts = rel_path.parts
        except ValueError:
            parts = file_path.parts
        
        if len(parts) == 1:
            return f"📁 ./{parts[0]}"
        
        
        tree_parts = []
        for i, part in enumerate(parts):
            if i == 0:
                
                tree_parts.append(f"📁 ./{part}")
            elif i == len(parts) - 1:
                
                indent = "  " * i
                tree_parts.append(f"{indent}└── 📄 {part}")
            else:
                
                indent = "  " * i
                tree_parts.append(f"{indent}├── 📁 {part}")
        
        return "\n".join(tree_parts)
    
    def action_refresh_scan(self) -> None:
        """Manually refresh scan."""
        self.scan_workspace()

    def on_directory_tree_file_selected(self, event):
        """When a file is selected from the tree, show code and scan that file."""
        path = Path(event.path)
        code_view = self.query_one(CodeView)
        security_panel = self.query_one(SecurityPanel)
        code_view.update_code(path)
        
        issues = self.scanner.scan_file(path)
        if issues:
            security_panel.update_issues({str(path): issues})
        else:
            security_panel.update_issues({})


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
        app = CodeSecApp()
        app.run()


if __name__ == "__main__":
    main()