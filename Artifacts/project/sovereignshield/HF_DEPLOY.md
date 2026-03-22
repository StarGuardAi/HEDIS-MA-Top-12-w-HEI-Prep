# Deploy SovereignShield to HuggingFace Spaces

The Space runs Docker with `WORKDIR /app` and `shiny run app.py`, so the **repository root must be the sovereignshield app tree** (`app.py`, `core/`, `agents/`, `rag/`, `Dockerfile`, etc.) — not the monorepo. Deploy from the **monorepo root** using **`git subtree push`**, same pattern as [sovereignshield-mobile `deploy_to_huggingface.py`](../sovereignshield-mobile/deploy_to_huggingface.py).

## 1. Create Space (one-time)

1. Go [huggingface.co/spaces](https://huggingface.co/spaces)
2. **Create new Space** — name e.g. `sovereignshield` under `rreichert`
3. **SDK**: Docker
4. **Visibility**: Public or Private

## 2. Add remote (one-time, from monorepo root)

```powershell
cd <path-to-HEDIS-MA-Top-12-w-HEI-Prep>
git remote add hf-sovereignshield https://huggingface.co/spaces/rreichert/sovereignshield
```

If the remote already exists, skip this step (`git remote -v` to verify).

## 3. Push deploy (every release)

From **repository root** (not `Artifacts/project/sovereignshield`):

```powershell
git subtree push --prefix=Artifacts/project/sovereignshield hf-sovereignshield main
```

HF rebuilds on push. Visit `https://rreichert-sovereignshield.hf.space` when the build is green.

**Do not** run `git push hf-sovereignshield main` without subtree — that would push the **entire monorepo** to the Space and break the Docker layout.

### If the Space history has diverged

`git subtree push` can be rejected (`fetch first` / non-fast-forward) when the Space repo has commits that are not ancestors of your subtree history.

**Force-update the Space to match this monorepo’s subtree** (overwrites `main` on the HuggingFace repo — use only when you intend to replace what’s live):

```powershell
git subtree split --prefix=Artifacts/project/sovereignshield -b hf-split-sovereignshield main
git push hf-sovereignshield hf-split-sovereignshield:main --force
git branch -D hf-split-sovereignshield
```

Alternatively, reconcile the Space clone with `git subtree pull` (more involved) if you must preserve unique commits on the Space side.

## 4. Add secrets

In Space **Settings → Repository secrets** add:

- `ANTHROPIC_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`

## 5. Manual copy (legacy / emergency)

If subtree push is blocked, you can still clone the Space, copy the contents of `Artifacts/project/sovereignshield/` to the repo root, commit, and push — same as the original workflow:

```bash
git clone https://huggingface.co/spaces/rreichert/sovereignshield
cd sovereignshield
# Copy app.py, core/, agents/, rag/, ui/, requirements.txt, Dockerfile, README.md, etc.
# from Artifacts/project/sovereignshield/
git add .
git commit -m "Deploy SovereignShield"
git push
```
