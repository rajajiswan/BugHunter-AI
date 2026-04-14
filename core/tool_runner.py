"""Tool runner module for BugHunter-AI.

Handles execution of security scanning tools (nmap, nikto, gobuster, etc.)
with timeout management and output parsing.
"""

import subprocess
import shutil
import logging
from typing import Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ToolResult:
    """Result from a tool execution."""
    tool: str
    command: str
    stdout: str = ""
    stderr: str = ""
    return_code: int = -1
    success: bool = False
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "tool": self.tool,
            "command": self.command,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "return_code": self.return_code,
            "success": self.success,
            "error": self.error,
        }


# Tools supported by BugHunter-AI and their availability check
SUPPORTED_TOOLS = [
    "nmap",
    "nikto",
    "gobuster",
    "sqlmap",
    "whatweb",
    "curl",
    "whois",
]


def can_run_tool(tool_name: str) -> bool:
    """Check if a tool is available on the system PATH."""
    return shutil.which(tool_name) is not None


def get_available_tools() -> list[str]:
    """Return a list of supported tools that are currently available."""
    return [tool for tool in SUPPORTED_TOOLS if can_run_tool(tool)]


class ToolRunner:
    """Executes external security tools and captures their output."""

    def __init__(self, default_timeout: int = 120):
        """
        Initialize the ToolRunner.

        Args:
            default_timeout: Default timeout in seconds for tool execution.
                             Increased from 60 to 120 since nikto/sqlmap scans
                             frequently exceeded the original default on slow targets.
        """
        self.default_timeout = default_timeout
        self.available_tools = get_available_tools()
        logger.debug("Available tools: %s", self.available_tools)

    def run(self, tool: str, args: list[str], timeout: Optional[int] = None) -> ToolResult:
        """
        Run a security tool with the given arguments.

        Args:
            tool: Name of the tool to run (e.g. 'nmap').
            args: List of arguments to pass to the tool.
            timeout: Timeout in seconds; defaults to self.default_timeout.

        Returns:
            ToolResult containing stdout, stderr, and return code.
        """
        if not can_run_tool(tool):
            logger.warning("Tool '%s' not found on PATH.", tool)
            return ToolResult(
                tool=tool,
                command="",
                error=f"Tool '{tool}' is not installed or not in PATH.",
            )

        cmd = [tool] + args
        cmd_str = " ".join(cmd)
        timeout = timeout or self.default_timeout

        logger.info("Running: %s", cmd_str)
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return ToolResult(
                tool=tool,
                command=cmd_str,
