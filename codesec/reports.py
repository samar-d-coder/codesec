from pathlib import Path
import json
from typing import Dict, List
from datetime import datetime

class ReportGenerator:
    """Generate security audit reports in various formats."""
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        
    def generate_json(self, data: Dict, output_path: Path) -> None:
        """Generate a JSON format report."""
        report = {
            'timestamp': self.timestamp,
            'summary': {
                'total_issues': len(data.get('issues', [])),
                'severity_counts': self._count_severities(data.get('issues', []))
            },
            'details': data
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)