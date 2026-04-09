"""Core vulnerability scanner module for BugHunter-AI.

Handles target enumeration, port scanning, and vulnerability detection
using AI-assisted analysis.
"""

import socket
import subprocess
import json
import logging
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    """Represents the result of a vulnerability scan."""
    target: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    open_ports: list = field(default_factory=list)
    services: dict = field(default_factory=dict)
    vulnerabilities: list = field(default_factory=list)
    scan_duration: float = 0.0
    status: str = "pending"

    def to_dict(self) -> dict:
        return {
            "target": self.target,
            "timestamp": self.timestamp,
            "open_ports": self.open_ports,
            "services": self.services,
            "vulnerabilities": self.vulnerabilities,
            "scan_duration": self.scan_duration,
            "status": self.status,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class Scanner:
    """Main scanner class that orchestrates vulnerability discovery."""

    # Common ports to check during quick scans
    COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445,
                    3306, 3389, 5432, 6379, 8080, 8443, 27017]

    def __init__(self, timeout: float = 1.0, max_threads: int = 50):
        """
        Initialize the scanner.

        Args:
            timeout: Socket connection timeout in seconds.
            max_threads: Maximum concurrent threads for port scanning.
        """
        self.timeout = timeout
        self.max_threads = max_threads
        logger.debug("Scanner initialized (timeout=%.1fs, threads=%d)",
                     timeout, max_threads)

    def resolve_target(self, target: str) -> Optional[str]:
        """Resolve hostname to IP address."""
        try:
            ip = socket.gethostbyname(target)
            logger.info("Resolved %s -> %s", target, ip)
            return ip
        except socket.gaierror as exc:
            logger.error("Failed to resolve target '%s': %s", target, exc)
            return None

    def check_port(self, host: str, port: int) -> bool:
        """Check if a single TCP port is open."""
        try:
            with socket.create_connection((host, port), timeout=self.timeout):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

    def scan_ports(self, host: str, ports: Optional[list] = None) -> list:
        """Scan a list of ports and return open ones."""
        ports = ports or self.COMMON_PORTS
        open_ports = []
        for port in ports:
            if self.check_port(host, port):
                open_ports.append(port)
                logger.debug("Open port found: %s:%d", host, port)
        return open_ports

    def grab_banner(self, host: str, port: int) -> Optional[str]:
        """Attempt to grab a service banner from an open port."""
        try:
            with socket.create_connection((host, port), timeout=self.timeout) as sock:
                sock.sendall(b"\r\n")
                banner = sock.recv(1024).decode(errors="ignore").strip()
                return banner if banner else None
        except Exception:
            return None

    def run(self, target: str, ports: Optional[list] = None) -> ScanResult:
        """Execute a full scan against the given target."""
        start = datetime.utcnow()
        result = ScanResult(target=target)

        ip = self.resolve_target(target)
        if not ip:
            result.status = "failed"
            return result

        logger.info("Starting port scan on %s", ip)
        result.open_ports = self.scan_ports(ip, ports)

        for port in result.open_ports:
            banner = self.grab_banner(ip, port)
            if banner:
                result.services[port] = banner

        result.scan_duration = (datetime.utcnow() - start).total_seconds()
        result.status = "complete"
        logger.info("Scan complete: %d open ports found in %.2fs",
                    len(result.open_ports), result.scan_duration)
        return result
