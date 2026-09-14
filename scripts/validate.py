#!/usr/bin/env python3
"""Deterministic repository and public-skill contract validator."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXPECTED_FILES = (
    "korea-transit-planner/SKILL.md",
    "README.md",
    "README.en.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "korea-transit-planner/references/map-routing.md",
    "korea-transit-planner/references/source-verification.md",
    "korea-transit-planner/references/gtx-routing.md",
    "korea-transit-planner/references/local-modes.md",
    "korea-transit-planner/examples/route-briefing.md",
    "scripts/validate_agent_skill.py",
    ".github/workflows/ci.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
)

TEXT_SUFFIXES = {"", ".md", ".py", ".yml", ".yaml", ".json", ".txt"}


def _chars(*codepoints: int) -> str:
    return "".join(chr(value) for value in codepoints)


PRIVATE_LITERALS = {
    "private-neighborhood-default": _chars(0xC591, 0xC7AC),
    "private-street-fragment": _chars(0xBC14, 0xC6B0, 0xBA2C),
    "private-chat-address": _chars(0xBCF4, 0xD5E4, 0x20, 0xD615, 0xB2D8),
}

SENSITIVE_PATTERNS = {
    "email-address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "generic-secret-assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}"
    ),
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "machine-home-path": re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+/"),
}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter at byte 0")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([a-z_]+):\s*(.+?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip('"\'')
    return values


def iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        relative_parts = path.relative_to(root).parts
        if not path.is_file() or any(part in {".git", ".tmp-hermes", "__pycache__"} for part in relative_parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def privacy_findings(root: Path) -> list[str]:
    findings: list[str] = []
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"{rel}: non-UTF-8 text")
            continue
        for label, literal in PRIVATE_LITERALS.items():
            if literal in text:
                findings.append(f"{rel}: forbidden {label}")
        for label, pattern in SENSITIVE_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{rel}: possible {label}")
    return findings


def contract_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in EXPECTED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    package = root / "korea-transit-planner"
    skill_path = package / "SKILL.md"
    if not skill_path.is_file():
        return errors
    skill = skill_path.read_text(encoding="utf-8")

    try:
        frontmatter = parse_frontmatter(skill)
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    required_frontmatter = {
        "name": "korea-transit-planner",
        "version": "0.1.0",
        "license": "MIT",
    }
    for key, expected in required_frontmatter.items():
        if frontmatter.get(key) != expected:
            errors.append(f"frontmatter {key!r} must be {expected!r}")
    description = frontmatter.get("description", "")
    if not description or len(description) > 60 or not description.endswith("."):
        errors.append("description must be a sentence of at most 60 characters")
    if "platforms" not in frontmatter:
        errors.append("frontmatter must declare platforms")

    origin_clauses = (
        "Explicit origin; it overrides every inferred or stored location.",
        "Do not use this skill until an origin is known.",
        "Require an explicit origin",
    )
    for clause in origin_clauses:
        if clause not in skill:
            errors.append(f"missing explicit-origin contract: {clause}")

    gtx_clauses = (
        "If and only if the user explicitly mentions GTX or names a GTX station",
        "Otherwise perform no GTX lookup or comparison.",
        "GTX routing — explicit opt-in only",
    )
    gtx_path = package / "references" / "gtx-routing.md"
    combined_gtx = skill + "\n" + gtx_path.read_text(encoding="utf-8") if gtx_path.is_file() else skill
    for clause in gtx_clauses:
        if clause not in combined_gtx:
            errors.append(f"missing GTX opt-in contract: {clause}")

    mode_terms = {
        "ordinary subway": ("ordinary subway", "일반 지하철"),
        "city/intercity bus": ("city/intercity bus", "시내·시외버스"),
        "village bus": ("마을버스", "village bus"),
        "Nuri Bus/DRT": ("누리버스/DRT", "Nuri Bus/DRT"),
        "walking": ("walking", "도보"),
        "taxi": ("taxi", "택시"),
        "mixed": ("mixed", "혼합"),
    }
    for label, alternatives in mode_terms.items():
        if not any(term in skill for term in alternatives):
            errors.append(f"missing required mode: {label}")

    constrained_station = "user-named boarding, transfer, or alighting station; preserve it as a hard constraint"
    if constrained_station not in skill:
        errors.append("missing user-named station hard constraint")

    comparison_terms = (
        "first mile",
        "initial wait/headway",
        "transfers",
        "exit/stop walking",
        "fare and fare confidence",
        "appointment buffer",
        "lookup timestamp with timezone",
    )
    for term in comparison_terms:
        if term not in skill:
            errors.append(f"missing door-to-door comparison field: {term}")

    linked = set(re.findall(r"\]\(((?:references|examples|scripts|assets)/[^)#?]+)\)", skill))
    required_support = {
        "references/map-routing.md",
        "references/source-verification.md",
        "references/gtx-routing.md",
        "references/local-modes.md",
        "examples/route-briefing.md",
    }
    missing_links = sorted(required_support - linked)
    for rel in missing_links:
        errors.append(f"support file is not linked from SKILL.md: {rel}")
    for rel in sorted(linked):
        if not (package / rel).is_file():
            errors.append(f"linked support file does not exist: {rel}")

    errors.extend(privacy_findings(root))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    errors = contract_errors(root)
    if errors:
        print(f"FAIL: {len(errors)} validation finding(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    count = sum(1 for _ in iter_text_files(root))
    print(f"PASS: skill structure, contract, and privacy checks ({count} text files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
