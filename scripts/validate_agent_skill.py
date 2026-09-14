#!/usr/bin/env python3
"""Validate the portable Agent Skills package with the Python stdlib."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter at byte 0")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([a-z][a-z0-9_-]*):\s*(.*?)\s*$", line)
        if match and match.group(2):
            values[match.group(1)] = match.group(2).strip('"\'')
    return values


def agent_skill_errors(package: Path) -> list[str]:
    errors: list[str] = []
    skill_path = package / "SKILL.md"
    if not skill_path.is_file():
        return ["missing required file: SKILL.md"]
    try:
        text = skill_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ["SKILL.md must be UTF-8"]
    try:
        metadata = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not name:
        errors.append("frontmatter requires name")
    elif len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        errors.append("name must be <=64 lowercase letters, digits, and single hyphens")
    elif name != package.name:
        errors.append("name must match the parent directory name")
    if not description:
        errors.append("frontmatter requires a non-empty description")
    elif len(description) > 1024:
        errors.append("description must be <=1024 characters")
    if "compatibility" in metadata and len(metadata["compatibility"]) > 500:
        errors.append("compatibility must be <=500 characters")

    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or target.startswith("#"):
            continue
        path_text = unquote(parsed.path)
        if not path_text:
            continue
        pure = PurePosixPath(path_text)
        if pure.is_absolute() or ".." in pure.parts:
            errors.append(f"linked package path escapes skill directory: {path_text}")
            continue
        if not (package / pure).is_file():
            errors.append(f"linked package file does not exist: {path_text}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", nargs="?", default="korea-transit-planner")
    args = parser.parse_args(argv)
    package = Path(args.package).resolve()
    errors = agent_skill_errors(package)
    if errors:
        print(f"FAIL: {len(errors)} Agent Skills finding(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: Agent Skills package and local references ({package.name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
