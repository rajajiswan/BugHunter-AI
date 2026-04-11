"""AI-powered vulnerability analyzer module for BugHunter-AI.

This module integrates with LLM backends to analyze scan results
and provide intelligent vulnerability assessments and remediation suggestions.
"""

import json
import os
from typing import Optional

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


SYSTEM_PROMPT = """You are an expert cybersecurity analyst and penetration tester.
Analyze the provided scan results and:
1. Identify potential vulnerabilities and their severity (Critical/High/Medium/Low)
2. Explain what each finding means in practical terms
3. Suggest specific remediation steps
4. Highlight false positives if any
5. Provide an overall risk assessment

Be concise but thorough. Use technical language appropriate for security professionals."""


class AIAnalyzer:
    """Analyzes scan results using AI/LLM backends."""

    def __init__(self, backend: str = "openai", model: str = None, api_key: str = None):
        """
        Initialize the AI analyzer.

        Args:
            backend: AI backend to use ('openai' or 'ollama')
            model: Model name to use (defaults vary by backend)
            api_key: API key for cloud-based backends
        """
        self.backend = backend.lower()
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")

        if self.backend == "openai":
            self.model = model or "gpt-4o-mini"
            if OPENAI_AVAILABLE and self.api_key:
                self.client = openai.OpenAI(api_key=self.api_key)
            else:
                self.client = None
        elif self.backend == "ollama":
            self.model = model or "llama3"
            self.client = None  # ollama uses module-level calls
        else:
            raise ValueError(f"Unsupported backend: {backend}. Choose 'openai' or 'ollama'.")

    def is_available(self) -> bool:
        """Check if the configured AI backend is available and ready."""
        if self.backend == "openai":
            return OPENAI_AVAILABLE and bool(self.api_key)
        elif self.backend == "ollama":
            return OLLAMA_AVAILABLE
        return False

    def analyze(self, scan_data: dict, extra_context: str = "") -> Optional[str]:
        """
        Analyze scan results and return AI-generated insights.

        Args:
            scan_data: Dictionary containing scan results (ScanResult.to_dict())
            extra_context: Optional additional context to include in the prompt

        Returns:
            AI-generated analysis string, or None if analysis failed
        """
        if not self.is_available():
            return None

        prompt = self._build_prompt(scan_data, extra_context)

        try:
            if self.backend == "openai":
                return self._query_openai(prompt)
            elif self.backend == "ollama":
                return self._query_ollama(prompt)
        except Exception as e:
            print(f"[AI Analyzer] Error during analysis: {e}")
            return None

    def _build_prompt(self, scan_data: dict, extra_context: str = "") -> str:
        """Build the analysis prompt from scan data."""
        target = scan_data.get("target", "unknown")
        findings = scan_data.get("findings", [])
        raw_output = scan_data.get("raw_output", "")

        prompt_parts = [
            f"Target: {target}",
            f"Scan Type: {scan_data.get('scan_type', 'general')}",
            f"Total Findings: {len(findings)}",
        ]

        if findings:
            prompt_parts.append("\nFindings:\n" + json.dumps(findings, indent=2))

        if raw_output:
            # Truncate raw output to avoid token limits
            truncated = raw_output[:3000] + "..." if len(raw_output) > 3000 else raw_output
            prompt_parts.append(f"\nRaw Tool Output:\n{truncated}")

        if extra_context:
            prompt_parts.append(f"\nAdditional Context:\n{extra_context}")

        return "\n".join(prompt_parts)

    def _query_openai(self, prompt: str) -> str:
        """Send prompt to OpenAI API and return response."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1500,
        )
        return response.choices[0].message.content

    def _query_ollama(self, prompt: str) -> str:
        """Send prompt to local Ollama instance and return response."""
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return response["message"]["content"]
