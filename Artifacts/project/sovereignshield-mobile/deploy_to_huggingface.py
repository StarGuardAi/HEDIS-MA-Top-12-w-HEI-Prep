#!/usr/bin/env python3
"""Deploy sovereignshield-mobile to HuggingFace Spaces via git subtree push."""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
PREFIX = "Artifacts/project/sovereignshield-mobile"
REMOTE = "hf-sovereignshield-mobile"

REQUIRED = ["Dockerfile", "requirements.txt", "app.py", "loading_overlay.py"]


def main() -> int:
    print("=" * 60)
    print("SovereignShield Mobile — HuggingFace Deployment")
    print("=" * 60)

    base = REPO_ROOT / "Artifacts" / "project" / "sovereignshield-mobile"
    for name in REQUIRED:
        p = base / name
        if not p.exists():
            print(f"[FAIL] Missing: {name}")
            return 1
        print(f"[OK] {name}")

    # Check remote exists
    result = subprocess.run(
        ["git", "remote", "get-url", REMOTE],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        print(f"\n[FAIL] Remote '{REMOTE}' not found. Run first:")
        print(f"  git remote add {REMOTE} https://huggingface.co/spaces/rreichert/sovereignshield-mobile")
        return 1
    print(f"\n[OK] Remote: {result.stdout.strip()}")

    # Subtree push — contents of prefix become root of HF repo
    print(f"\nPushing subtree ({PREFIX}) to {REMOTE} main...")
    result = subprocess.run(
        ["git", "subtree", "push", "--prefix=" + PREFIX, REMOTE, "main"],
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        print("\n[FAIL] subtree push failed")
        return 1

    print("\n" + "=" * 60)
    print("Deploy complete. HF will rebuild.")
    print("Build notes: OPA curl ~15s; CMD uses app.py at /app — verify build goes green.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
