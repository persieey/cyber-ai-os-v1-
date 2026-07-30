#!/usr/bin/env python3
"""
tests/validate.py — System integrity validator for Cyber AI OS
Usage: python3 tests/validate.py [--verbose]

Checks:
  1. All role files in department/*/manifest.yaml exist
  2. All workflow files in manifests exist
  3. All skill directories in manifests have a SKILL.md
  4. All role paths in .claude/agents/*.md exist
  5. All file paths in .claude/commands/*.md exist
"""

import os
import re
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv

GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"
PASS  = f"{GREEN}✓{RESET}"
FAIL  = f"{RED}✗{RESET}"

issues: list[tuple[str, str]] = []  # (source, message)
checked = 0


def resolve(path_str: str, manifest_dir: Path | None = None) -> Path | None:
    """Try project-root first, then relative to manifest dir."""
    p = ROOT / path_str
    if p.exists():
        return p
    if manifest_dir:
        p2 = manifest_dir / path_str
        if p2.exists():
            return p2
    return None


def check(source: str, path_str: str, manifest_dir: Path | None = None) -> bool:
    global checked
    checked += 1
    found = resolve(path_str, manifest_dir)
    if found:
        if VERBOSE:
            print(f"    {PASS} {path_str}")
        return True
    issues.append((source, f"NOT FOUND: {path_str}"))
    if VERBOSE:
        print(f"    {FAIL} {path_str}")
    return False


def check_skill_dir(source: str, dir_str: str, manifest_dir: Path | None = None) -> bool:
    """Skills are directories — check that SKILL.md exists inside."""
    global checked
    checked += 1
    skill_md = dir_str.rstrip("/") + "/SKILL.md"
    found = resolve(skill_md, manifest_dir)
    if found:
        if VERBOSE:
            print(f"    {PASS} {skill_md}")
        return True
    issues.append((source, f"SKILL.md missing: {skill_md}"))
    if VERBOSE:
        print(f"    {FAIL} {skill_md}")
    return False


# ── Manifest walker ─────────────────────────────────────────────────────────

def extract_role_files(roles) -> list[str]:
    """Extract file paths from roles regardless of structure."""
    files = []
    if isinstance(roles, str):
        files.append(roles)
    elif isinstance(roles, dict):
        for key, val in roles.items():
            if isinstance(val, str):
                files.append(val)   # manager: path/to/file.md
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        f = item.get("file", item.get("role_file", ""))
                        if f:
                            files.append(f)
                    elif isinstance(item, str):
                        files.append(item)
    elif isinstance(roles, list):
        for item in roles:
            if isinstance(item, dict):
                f = item.get("file", item.get("role_file", ""))
                if f:
                    files.append(f)
    return files


def extract_skill_paths(skills) -> list[str]:
    """Extract skill directory paths."""
    paths = []
    if isinstance(skills, list):
        for item in skills:
            if isinstance(item, str):
                paths.append(item)
            elif isinstance(item, dict):
                f = item.get("skill_file", item.get("file", ""))
                if f:
                    paths.append(f)
    elif isinstance(skills, dict):
        for key, val in skills.items():
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, str):
                        paths.append(item)
                    elif isinstance(item, dict):
                        f = item.get("skill_file", item.get("file", ""))
                        if f:
                            paths.append(f)
    return paths


def validate_manifests():
    print("\n[1] Manifest validation...")
    manifests = list(ROOT.glob("department/*/manifest.yaml"))
    ok = fail = 0

    for mf in sorted(manifests):
        mf_dir = mf.parent
        rel = str(mf.relative_to(ROOT))
        if VERBOSE:
            print(f"\n  {rel}")
        try:
            data = yaml.safe_load(mf.read_text(encoding="utf-8"))
        except Exception as e:
            issues.append((rel, f"YAML parse error: {e}"))
            fail += 1
            continue

        dept = data.get("name", rel)

        # Check agent file
        agent = data.get("agent", "")
        if agent:
            if check(f"{dept} > agent", agent, mf_dir):
                ok += 1
            else:
                fail += 1

        # Check role files
        for role_path in extract_role_files(data.get("roles", {})):
            if check(f"{dept} > roles", role_path, mf_dir):
                ok += 1
            else:
                fail += 1

        # Check skill directories
        for skill_path in extract_skill_paths(data.get("skills", {})):
            if skill_path.endswith(".md"):
                if check(f"{dept} > skills", skill_path, mf_dir):
                    ok += 1
                else:
                    fail += 1
            else:
                if check_skill_dir(f"{dept} > skills", skill_path, mf_dir):
                    ok += 1
                else:
                    fail += 1

        # Check workflow files
        for wf in data.get("workflows", []):
            if isinstance(wf, dict):
                wf_file = wf.get("file", "")
            else:
                wf_file = str(wf)
            if wf_file:
                if check(f"{dept} > workflows", wf_file, mf_dir):
                    ok += 1
                else:
                    fail += 1

    print(f"  {len(manifests)} manifests | {ok} paths OK | {fail} failed")


# ── Agent role table paths ───────────────────────────────────────────────────

# Matches lines like: → department/foo/roles/bar.md or `department/foo/...md`
AGENT_PATH_RE = re.compile(
    r'(?:→\s*|`)((?:department|skills|knowledge|workspace|templates)/[^\s`\'"\n]+\.md)'
)

def validate_agents():
    print("\n[2] Agent role table validation...")
    agents = list((ROOT / ".claude/agents").glob("*.md"))
    ok = fail = 0
    for agent in sorted(agents):
        rel = str(agent.relative_to(ROOT))
        if VERBOSE:
            print(f"\n  {rel}")
        content = agent.read_text(encoding="utf-8")
        for path in AGENT_PATH_RE.findall(content):
            if check(rel, path):
                ok += 1
            else:
                fail += 1
    print(f"  {len(agents)} agents | {ok} paths OK | {fail} failed")


# ── Command file paths ──────────────────────────────────────────────────────

CMD_PATH_RE = re.compile(
    r'`((?:workspace|department|skills|knowledge|templates)[^`\n]+\.(?:md|yaml|sh|py))`'
)

def validate_commands():
    print("\n[3] Command file path validation...")
    commands = list((ROOT / ".claude/commands").glob("*.md"))
    ok = fail = 0
    for cmd in sorted(commands):
        rel = str(cmd.relative_to(ROOT))
        if VERBOSE:
            print(f"\n  {rel}")
        content = cmd.read_text(encoding="utf-8")
        for path in CMD_PATH_RE.findall(content):
            if "session.md" in path:  # runtime-generated, skip
                continue
            if check(rel, path):
                ok += 1
            else:
                fail += 1
    print(f"  {len(commands)} commands | {ok} paths OK | {fail} failed")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  Cyber AI OS — System Integrity Validator")
    print("=" * 55)

    validate_manifests()
    validate_agents()
    validate_commands()

    print("\n" + "=" * 55)
    print(f"  Paths checked: {checked}")

    if issues:
        print(f"  {FAIL} {len(issues)} issue(s) found:\n")
        for src, msg in issues:
            print(f"  [{src}]")
            print(f"    {msg}")
        print()
        sys.exit(1)
    else:
        print(f"  {PASS} All paths valid — system is clean")
        print("=" * 55)
        sys.exit(0)


if __name__ == "__main__":
    main()
