#!/usr/bin/env python3
"""Validation script for public OmniForge distribution repository."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    required_files = [
        "README.md",
        ".github/workflows/build-release.yml",
        "scripts/install.sh",
        "scripts/install.ps1",
    ]
    missing = [f for f in required_files if not (ROOT / f).exists()]
    if missing:
        print(f"FAIL: Missing public distribution files: {missing}")
        return 1

    # Security check: Zero Leakage of private/internal files
    forbidden = ["AGENTS.md", "CURRENT.md", "STATUS.md", "NEXT.md", "docs"]
    leaks = [f for f in forbidden if (ROOT / f).exists()]
    if leaks:
        print(f"SECURITY FAIL: Leaked internal files detected in public repo: {leaks}")
        return 1

    workflow = ROOT / ".github" / "workflows" / "build-release.yml"
    content = workflow.read_text(encoding="utf-8")
    if "sparse-checkout" not in content or "secrets.CORE_REPO" not in content:
        print("FAIL: build-release.yml must enforce air-gapped sparse-checkout with secret-driven repository")
        return 1

    # Sensitive keyword scan across all files
    sensitive_keywords = ["cloak", "adryfish", "antidetect", "fingerprint", "stealth", "87+"]
    for path in ROOT.rglob("*"):
        if path.is_file() and not path.name.startswith(".git") and path.name != "validate.py":
            try:
                text = path.read_text(encoding="utf-8")
                for kw in sensitive_keywords:
                    if kw.lower() in text.lower():
                        print(f"SECURITY FAIL: Leaked keyword '{kw}' found in {path.relative_to(ROOT)}")
                        return 1
            except Exception:
                pass

    print("PASS: OmniForge public distribution hub validation successful (Zero Leaks, Air-Gapped)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
