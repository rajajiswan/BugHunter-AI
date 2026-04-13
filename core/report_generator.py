"""Report generator module for BugHunter-AI.

Generates structured vulnerability reports from scan results
in multiple formats (JSON, Markdown, HTML).
"""

import json
import os
from datetime import datetime
from typing import List, Optional

from core.scanner import ScanResult


class ReportGenerator:
    """Generates vulnerability reports from scan results."""

    SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    SEVERITY_COLORS = {
        "critical": "#ff0000",
        "high": "#ff6600",
        "medium": "#ffaa00",
        "low": "#ffff00",
        "info": "#00aaff",
    }

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _sort_results(self, results: List[ScanResult]) -> List[ScanResult]:
        """Sort results by severity (critical first)."""
        return sorted(
            results,
            key=lambda r: self.SEVERITY_ORDER.get(r.severity.lower(), 99),
        )

    def generate_json(self, results: List[ScanResult], target: str) -> str:
        """Generate a JSON report and save it to disk."""
        timestamp = datetime.utcnow().isoformat()
        report = {
            "report_generated": timestamp,
            "target": target,
            "total_findings": len(results),
            "severity_summary": self._severity_summary(results),
            "findings": [r.to_dict() for r in self._sort_results(results)],
        }
        filename = os.path.join(
            self.output_dir, f"report_{self._safe_name(target)}_{self._ts()}.json"
        )
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        return filename

    def generate_markdown(self, results: List[ScanResult], target: str) -> str:
        """Generate a Markdown report and save it to disk."""
        lines = [
            f"# BugHunter-AI Vulnerability Report",
            f"",
            f"**Target:** `{target}`  ",
            f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC  ",
            f"**Total Findings:** {len(results)}",
            f"",
            f"## Severity Summary",
            f"",
        ]
        summary = self._severity_summary(results)
        for sev, count in summary.items():
            lines.append(f"- **{sev.capitalize()}:** {count}")

        lines += ["", "## Findings", ""]
        for i, result in enumerate(self._sort_results(results), 1):
            lines += [
                f"### {i}. {result.title}",
                f"",
                f"| Field | Value |",
                f"|-------|-------|",
                f"| **Severity** | {result.severity.upper()} |",
                f"| **Tool** | {result.tool} |",
                f"| **Target** | {result.target} |",
                f"",
                f"**Description:**  ",
                f"{result.description}",
                f"",
            ]
            if result.recommendation:
                lines += [f"**Recommendation:**  ", f"{result.recommendation}", ""]

        filename = os.path.join(
            self.output_dir, f"report_{self._safe_name(target)}_{self._ts()}.md"
        )
        with open(filename, "w") as f:
            f.write("\n".join(lines))
        return filename

    def _severity_summary(self, results: List[ScanResult]) -> dict:
        """Return a count of findings per severity level."""
        summary = {sev: 0 for sev in self.SEVERITY_ORDER}
        for r in results:
            key = r.severity.lower()
            if key in summary:
                summary[key] += 1
        return {k: v for k, v in summary.items() if v > 0}

    @staticmethod
    def _safe_name(target: str) -> str:
        """Sanitize target string for use in filenames."""
        return "".join(c if c.isalnum() or c in "-_." else "_" for c in target)[:40]

    @staticmethod
    def _ts() -> str:
        """Return a compact UTC timestamp suitable for filenames."""
        return datetime.utcnow().strftime("%Y%m%d_%H%M%S")
