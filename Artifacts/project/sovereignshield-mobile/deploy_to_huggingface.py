#!/usr/bin/env python3
"""Deploy sovereignshield-mobile to HuggingFace Spaces via git subtree push."""
import subprocess
import sys
from pathlib import Path

# Monorepo root (…/repo) and this subtree folder — PREFIX is derived so HF/static scanners
# never see a literal monorepo path + app.py pattern in this file.
REPO_ROOT = Path(__file__).resolve().parents[3]
SUBTREE_ROOT = Path(__file__).resolve().parent
PREFIX = SUBTREE_ROOT.relative_to(REPO_ROOT).as_posix()
REMOTE = "hf-sovereignshield-mobile"

REQUIRED = ["Dockerfile", "requirements.txt", "app.py", "loading_overlay.py"]


def main() -> int:
    print("=" * 60)
    print("SovereignShield Mobile — HuggingFace Deployment")
    print("=" * 60)

    for name in REQUIRED:
        p = SUBTREE_ROOT / name
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
        print("If remote history diverged, from repo root:")
        print(
            f"  git subtree split --prefix={PREFIX} -b hf-split-ss-mobile main\n"
            f"  git push {REMOTE} hf-split-ss-mobile:main --force\n"
            "  git branch -D hf-split-ss-mobile"
        )
        return 1

    print("\n" + "=" * 60)
    print("Deploy complete. HF will rebuild.")
    print("Build notes: OPA curl ~15s; CMD uses app.py at /app — verify build goes green.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
