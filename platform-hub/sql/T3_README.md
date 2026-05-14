# T3 Primary Migration — Branch Selection

Two SQL files. Run exactly **ONE** against Primary
(`wiwmphjkupcnntawpafg`) based on T2.c output:

| T2.c result | Run this file |
|-------------|---------------|
| `relation "public.cross_app_findings" does not exist` | `t3_primary_create.sql` |
| Table exists (empty or with rows) | `t3_primary_alter.sql` |

Both files are written to be **idempotent** where possible (safe re-run for policies, indexes, view). After applying, verify:

```sql
SELECT * FROM public.platform_hub_kpis ORDER BY source_app, sub_surface;
SELECT * FROM pg_policies WHERE tablename = 'cross_app_findings';
```

Then proceed to T4 (wire `sub_surface` + env rotation); T2.c still needs Primary credentials (Option A MCP or Option B `.env`).

---

## Schema reconciliation notes (2026-05-14)

- **Source of truth:** `Artifacts/shared/supabase_findings.py` (`insert_finding` → SQL columns) and `Artifacts/project/*/supabase_platform.py` (`insert_cross_app_finding` → row dict for PostgREST). Both agree on **`source_app`, `finding_type`, `title`, `description`, `severity`, `status`**; psycopg2 adds **`metadata`, `created_at`, `updated_at`**; REST optionally adds **`session_id`** and kwargs **`measure_id`, `policy_id`, `payload`**.
- **`sub_surface`** is the **only net-new** column for D2 (desktop | mobile | NULL for live / unknown).
- **No `remediated` boolean:** session teardown uses **`status = 'remediated'`** (text), per helper docstrings.
- **Status CHECK** allows: `open`, `remediated`, `resolved`, `dismissed` (covers live + Hub semantics).
- **Severity CHECK** allows: `info`, `low`, `medium`, `high`, `critical` (matches `insert_finding` docstring; REST sends explicit values).
- **`resolved_at`:** optional column for future Hub workflows; helpers do not set it today.
- **`updated_at` trigger:** `caf_set_updated_at` fires `BEFORE UPDATE` so REST writes that omit `updated_at` still refresh the column.
- **Backfill (`t3_primary_alter.sql`):** `sub_surface` from `metadata->>'sub_surface'`, `payload->>'sub_surface'`, or `metadata->>'platform'` when those values are `desktop` or `mobile` (case-insensitive). Path-based heuristics stay in **app code (T4)**, not SQL.

### Trigger compatibility

If `CREATE TRIGGER ... EXECUTE FUNCTION public.caf_set_updated_at()` errors on your Postgres build, replace **`EXECUTE FUNCTION`** with **`EXECUTE PROCEDURE`** (older trigger syntax) per your server version.

### View compatibility (`security_invoker`)

`platform_hub_kpis` is created **`WITH (security_invoker = false)`** so the Hub **anon** client can `SELECT` aggregated KPIs without a policy on `cross_app_findings` for `anon`. If **`CREATE VIEW ... WITH (security_invoker = false)`** errors on your Postgres build, `DROP VIEW` then recreate without the clause and run **`ALTER VIEW public.platform_hub_kpis SET (security_invoker = false);`** (when supported), or consult your Postgres version docs.

---

## RLS security model (2026-05-14)

**Hub auth (`platform-hub/app.py`):** `create_client` resolves the key in order **`SUPABASE_ANON_KEY`** → **`PLATFORM_SUPABASE_ANON_KEY`** → **`SUPABASE_KEY`** → **`SUPABASE_SERVICE_ROLE_KEY`** — the intended Hub path is the **anon** publishable key, not service_role.

**Roles vs object access**

|  | `anon` | `authenticated` | `service_role` |
|--|--------|-----------------|----------------|
| **`public.cross_app_findings` (base table)** | no access (explicit `REVOKE ALL`); RLS policies only `SELECT` for `authenticated` + `service_role`; `INSERT`/`UPDATE` only `service_role` | `SELECT` | `SELECT`, `INSERT`, `UPDATE` |
| **`public.platform_hub_kpis` (view)** | `SELECT` | `SELECT` | `SELECT` |

**Rationale:** Hub reads **aggregated** KPIs only via the anon key — no direct row-level `SELECT` on individual findings for `anon`. Sub-app inserts use a **service_role** (or equivalent) key in Space secrets. Hub does not write findings.

**View definition:** `security_invoker = false` (definer-style evaluation) so querying the view as `anon` does not evaluate base-table RLS as the `anon` principal for the inner scan (see Postgres view option docs for your version).
