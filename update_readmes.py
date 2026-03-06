#!/usr/bin/env python3
# update_readmes.py
# ─────────────────────────────────────────────────────────────
# Injects complete, pre-built README files into all 3 GitHub
# repositories for reichert-science-intelligence.
#
# MODE A (default): Pushes the full README file for each repo
# MODE B (--patch):  Injects only the cloud summary block,
#                    replacing between sentinel markers
#
# Usage:
#   export GITHUB_TOKEN=ghp_your_token
#
#   # Full README replacement (recommended first run):
#   python update_readmes.py
#
#   # Patch-only — update cloud block, preserve rest of README:
#   python update_readmes.py --patch
#
# Requirements:
#   pip install requests
# ─────────────────────────────────────────────────────────────

import os
import sys
import base64
import requests
from datetime import datetime
from pathlib import Path

# ── Config ───────────────────────────────────────────────────
GITHUB_ORG   = "reichert-science-intelligence"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# ── Sentinel markers ─────────────────────────────────────────
START_MARKER = "<!-- CLOUD_DEPLOYMENT_SUMMARY_START -->"
END_MARKER   = "<!-- CLOUD_DEPLOYMENT_SUMMARY_END -->"

# ── Repo → local README file mapping ─────────────────────────
REPOS = [
    {
        "repo":        "AuditShield",
        "branch":      "main",
        "path":        "README.md",
        "label":       "AuditShield-Live",
        "local_file":  "README_auditshield.md",
    },
    {
        "repo":        "StarGuard",
        "branch":      "main",
        "path":        "README.md",
        "label":       "StarGuard Desktop",
        "local_file":  "README_starguard_desktop.md",
    },
    {
        "repo":        "StarGuard-Mobile",
        "branch":      "main",
        "path":        "README.md",
        "label":       "StarGuard Mobile",
        "local_file":  "README_starguard_mobile.md",
    },
]

# ─────────────────────────────────────────────────────────────
# GITHUB API HELPERS
# ─────────────────────────────────────────────────────────────

def gh_headers() -> dict:
    if not GITHUB_TOKEN:
        raise EnvironmentError(
            "\n❌ GITHUB_TOKEN not set.\n"
            "   Generate one at: https://github.com/settings/tokens/new\n"
            "   Required scope: repo (Contents read + write)\n"
            "   Then run:  export GITHUB_TOKEN=ghp_yourtoken\n"
        )
    return {
        "Authorization":        f"Bearer {GITHUB_TOKEN}",
        "Accept":               "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def fetch_file(org: str, repo: str, path: str, branch: str) -> tuple:
    """Returns (content_str, sha) or ("", None) if not found."""
    url = (
        f"https://api.github.com/repos/{org}/{repo}"
        f"/contents/{path}?ref={branch}"
    )
    r = requests.get(url, headers=gh_headers())
    if r.status_code == 404:
        return ("", None)
    r.raise_for_status()
    data    = r.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return (content, data["sha"])


def push_file(
    org: str, repo: str, path: str, branch: str,
    content: str, sha: str | None, message: str
):
    url = (
        f"https://api.github.com/repos/{org}/{repo}"
        f"/contents/{path}"
    )
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch":  branch,
    }
    if sha:
        payload["sha"] = sha
    r = requests.put(url, headers=gh_headers(), json=payload)
    r.raise_for_status()
    return r.json()


# ─────────────────────────────────────────────────────────────
# README HELPERS
# ─────────────────────────────────────────────────────────────

def load_local(filename: str) -> str:
    p = Path(filename)
    if not p.exists():
        raise FileNotFoundError(
            f"❌ Local file not found: {filename}\n"
            f"   Save it in the same directory as update_readmes.py"
        )
    return p.read_text(encoding="utf-8")


def extract_cloud_block(full_readme: str) -> str:
    """Pull the cloud summary block out of a full README file."""
    if START_MARKER not in full_readme or END_MARKER not in full_readme:
        raise ValueError(
            f"Cloud summary sentinels not found in README file.\n"
            f"Expected: {START_MARKER} ... {END_MARKER}"
        )
    start = full_readme.index(START_MARKER)
    end   = full_readme.index(END_MARKER) + len(END_MARKER)
    return full_readme[start:end]


def patch_readme(existing: str, cloud_block: str) -> tuple:
    """
    Replace cloud block in existing README if present,
    or append it. Returns (new_content, action_label).
    """
    if START_MARKER in existing and END_MARKER in existing:
        before = existing[:existing.index(START_MARKER)]
        after  = existing[existing.index(END_MARKER) + len(END_MARKER):]
        return (before + cloud_block + after, "replaced")
    else:
        sep = "\n\n" if not existing.endswith("\n\n") else ""
        return (existing + sep + cloud_block, "appended")


# ─────────────────────────────────────────────────────────────
# COMMIT MESSAGE
# ─────────────────────────────────────────────────────────────

def commit_msg(label: str, mode: str) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    if mode == "full":
        return (
            f"docs: replace README with full cloud-integrated version [{date}]\n\n"
            f"Auto-generated by update_readmes.py (MODE A — full replacement)\n"
            f"• App header with badges and live demo links\n"
            f"• Feature overview with cloud service table\n"
            f"• Architecture tree\n"
            f"• Quick start + dependencies\n"
            f"• HuggingFace secrets checklist\n"
            f"• Cloud deployment summary block\n"
            f"• Recruiter signals table\n"
            f"• Module map across all 3 apps"
        )
    else:
        return (
            f"docs: patch cloud deployment summary block [{date}]\n\n"
            f"Auto-generated by update_readmes.py (MODE B — patch only)\n"
            f"• Updated cloud module architecture\n"
            f"• Updated HF deployment table\n"
            f"• Updated GCP + Sheets setup\n"
            f"• Updated recruiter signals table"
        )


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    patch_only = "--patch" in sys.argv
    mode_label = "PATCH (cloud block only)" if patch_only else "FULL README replacement"

    print("=" * 62)
    print(f"  README Updater — reichert-science-intelligence")
    print(f"  Mode:      {mode_label}")
    print(f"  Repos:     {len(REPOS)}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 62)

    results = []

    for target in REPOS:
        repo       = target["repo"]
        branch     = target["branch"]
        path       = target["path"]
        label      = target["label"]
        local_file = target["local_file"]

        print(f"\n── {label} ({repo}/{branch}/{path}) ──")

        try:
            # 1. Load local README file
            local_content = load_local(local_file)
            print(f"  📄 Loaded {local_file} ({len(local_content):,} chars)")

            # 2. Fetch existing remote README
            remote_content, sha = fetch_file(GITHUB_ORG, repo, path, branch)
            if sha:
                print(f"  📥 Remote README fetched ({len(remote_content):,} chars)")
            else:
                print(f"  📭 No existing README — will create.")

            # 3. Build new content based on mode
            if patch_only:
                cloud_block  = extract_cloud_block(local_content)
                new_content, action = patch_readme(
                    remote_content if remote_content else local_content,
                    cloud_block
                )
                print(f"  🔧 Cloud block {action} ({len(cloud_block):,} chars)")
            else:
                new_content = local_content
                action      = "replaced" if sha else "created"
                print(f"  📝 Full README {action}")

            # 4. Skip if unchanged
            if new_content == remote_content:
                print(f"  ⏭  No changes detected — skipping commit.")
                results.append({"repo": repo, "status": "⏭ Skipped (no changes)"})
                continue

            # 5. Commit to GitHub
            push_file(
                GITHUB_ORG, repo, path, branch,
                new_content, sha,
                commit_msg(label, "patch" if patch_only else "full")
            )

            char_delta = len(new_content) - len(remote_content or "")
            delta_str  = f"+{char_delta:,}" if char_delta >= 0 else f"{char_delta:,}"
            print(f"  ✅ Committed — {delta_str} chars")
            results.append({"repo": repo, "status": "✅ Success"})

        except FileNotFoundError as e:
            print(f"  ❌ {e}")
            results.append({"repo": repo, "status": f"❌ File not found: {local_file}"})

        except requests.HTTPError as e:
            msg = f"HTTP {e.response.status_code}"
            try:
                detail = e.response.json().get("message", "")[:80]
                msg += f" — {detail}"
            except Exception:
                pass
            print(f"  ❌ {msg}")
            results.append({"repo": repo, "status": f"❌ {msg}"})

        except Exception as e:
            print(f"  ❌ {e}")
            results.append({"repo": repo, "status": f"❌ {str(e)[:80]}"})

    # ── Final summary ──
    print(f"\n{'=' * 62}")
    print(f"  RESULTS")
    print(f"{'=' * 62}")
    for r in results:
        print(f"  {r['status']}  {r['repo']}")
    success = sum(1 for r in results if r["status"].startswith("✅"))
    print(f"\n  {success}/{len(results)} repos updated successfully.")

    if success < len(results):
        print("\n  💡 Troubleshooting:")
        print("     • Token scope: needs repo → Contents (read + write)")
        print("     • Repo names must match exactly (case-sensitive)")
        print("     • Verify org name: reichert-science-intelligence")
        sys.exit(1)


if __name__ == "__main__":
    main()
