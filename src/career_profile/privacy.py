"""Redacting privacy scanner for public repository content."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from .errors import PrivacyError


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    category: str

    def diagnostic(self) -> str:
        return f"{self.path}:{self.line}: detected [REDACTED {self.category}]"


_TAIWAN_STREET_PATTERN = r"(?:路|街|大道).{0,20}"
_TAIWAN_NUMBER_PATTERN = r"(?:號|巷)"

PATTERNS: dict[str, re.Pattern[str]] = {
    "email": re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+", re.IGNORECASE),
    "phone": re.compile(r"(?<!\d)(?:\+?886[- ]?|0)(?:\d[- ]?){8,10}(?!\d)"),
    "taiwan-identity-number": re.compile(r"(?<![A-Z0-9])[A-Z][12]\d{8}(?!\d)"),
    "secret": re.compile(
        r"(?i)(?:api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"]?[^\s'\"]{8,}"
    ),
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "salary-record": re.compile(
        r"(?i)(?:salary|薪資|月薪|年薪)\s*(?::|\uFF1A|=)?\s*(?:NT\$?|TWD|USD|\$)?\s*\d"
    ),
    "residential-address": re.compile(
        _TAIWAN_STREET_PATTERN + _TAIWAN_NUMBER_PATTERN + "|"
        r"\b\d{1,5}\s+[A-Za-z0-9 .'-]+\s+(?:Street|St|Road|Rd|Ave|Avenue)\b",
        re.IGNORECASE,
    ),
}
NON_ALLOWLISTABLE = {"secret", "private-key", "taiwan-identity-number"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".toml", ".py", ".j2", ".css", ".txt", ".json"}


def load_allowlist(path: Path | None) -> set[str]:
    if path is None or not path.exists():
        return set()
    document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    values = document.get("allowed_public_contact_values", [])
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise PrivacyError("Privacy allowlist must contain a string list")
    for value in values:
        for category in NON_ALLOWLISTABLE:
            if PATTERNS[category].search(value):
                raise PrivacyError(f"Privacy allowlist cannot permit category '{category}'")
    return set(values)


def scan_text(text: str, path: Path, allowlist: set[str] | None = None) -> list[Finding]:
    allowlist = allowlist or set()
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for category, pattern in PATTERNS.items():
            for match in pattern.finditer(line):
                if category not in NON_ALLOWLISTABLE and match.group(0) in allowlist:
                    continue
                findings.append(Finding(path, line_number, category))
    return findings


def scan_public_tree(public_dir: Path, allowlist_path: Path | None = None) -> list[Finding]:
    if not public_dir.is_dir():
        raise PrivacyError(f"Public data directory does not exist: {public_dir}")
    allowlist = load_allowlist(allowlist_path)
    findings: list[Finding] = []
    for path in sorted(public_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            findings.extend(scan_text(path.read_text(encoding="utf-8"), path, allowlist))
    return findings


def scan_repository(root: Path, allowlist_path: Path | None = None) -> list[Finding]:
    allowlist = load_allowlist(allowlist_path)
    excluded_parts = {".git", ".venv", "private", "dist", "__pycache__"}
    findings: list[Finding] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in excluded_parts for part in path.relative_to(root).parts):
            continue
        findings.extend(scan_text(path.read_text(encoding="utf-8"), path, allowlist))
    return findings


def assert_public_tree_safe(public_dir: Path, allowlist_path: Path | None = None) -> None:
    findings = scan_public_tree(public_dir, allowlist_path)
    if findings:
        diagnostics = "\n".join(finding.diagnostic() for finding in findings)
        raise PrivacyError(f"Public privacy check failed:\n{diagnostics}")


def assert_repository_safe(root: Path, allowlist_path: Path | None = None) -> None:
    findings = scan_repository(root, allowlist_path)
    if findings:
        diagnostics = "\n".join(finding.diagnostic() for finding in findings)
        raise PrivacyError(f"Repository privacy check failed:\n{diagnostics}")
