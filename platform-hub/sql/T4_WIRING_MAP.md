# T4 Wiring Map — `cross_app_findings` (read-only inventory)

**Generated:** 2026-05-14  
**Scope:** `C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep` monorepo (grep + file reads; no DB, no runtime edits).  
**Context:** Q1 locks Hub reads to **Primary** (`wiwmphjkupcnntawpafg`). Hub Space secrets `SUPABASE_*` last touched **2026-03-24** — high probability still **Sovereign** until rotation + T2.c confirms.

---

## 1. Helper location (`supabase_findings.py`)

Vendored copies of the same module (psycopg2 direct INSERT path):

| Full path |
|-----------|
| `Artifacts\shared\supabase_findings.py` |
| `Artifacts\project\auditshield\shared\supabase_findings.py` |
| `Artifacts\project\auditshield\starguard-desktop\shared\supabase_findings.py` |
| `Artifacts\project\auditshield\starguard-mobile\Artifacts\app\shared\supabase_findings.py` |
| `Artifacts\project\sovereignshield\shared\supabase_findings.py` |
| `Artifacts\project\sovereignshield-mobile\shared\supabase_findings.py` |

**Contract (helper):** `insert_finding(...)` builds SQL for columns  
`(source_app, finding_type, severity, status, title, description, metadata, created_at, updated_at)`  
using DSN from **`PLATFORM_DATABASE_URL` → `DATABASE_URL` → `SUPABASE_DB_URL`** (TCP `postgres://` / `postgresql://` only; HTTP URLs ignored).

**Other helper:** `supabase_platform.py` (REST `supabase-py`) — **three copies** (identical pattern):

- `Artifacts\project\auditshield\supabase_platform.py`
- `Artifacts\project\auditshield\starguard-desktop\supabase_platform.py`
- `Artifacts\project\sovereignshield\supabase_platform.py`

Uses **`PLATFORM_SUPABASE_URL` or `SUPABASE_URL`** and anon/service keys for `create_client`.

---

## 2. Write call sites

### 2A. `insert_finding` (psycopg2 → direct SQL)

| File | Line (approx) | `source_app` | `sub_surface` today | `finding_type` (representative) |
|------|---------------|--------------|---------------------|----------------------------------|
| `Artifacts\project\auditshield\app.py` | 708 | `auditshield` | **not passed** (NULL until T4) | `session_end` |
| `Artifacts\project\auditshield\starguard-desktop\app.py` | 1991 | `starguard` | **not passed** | `session_end` |
| `Artifacts\project\auditshield\starguard-desktop\app.py` | 4429 | `starguard` | **not passed** | `star_gap` |
| `Artifacts\project\auditshield\starguard-mobile\Artifacts\app\app.py` | 349 | `starguard` | **not passed** | `session_end` |
| `Artifacts\project\auditshield\starguard-mobile\Artifacts\app\pages\hedis_analyzer.py` | 177 | `starguard` | **not passed** | `star_gap` |
| `Artifacts\project\sovereignshield\app.py` | 600 | `sovereignshield` | **not passed** | `session_end` |
| `Artifacts\project\sovereignshield\app.py` | 681 | `sovereignshield` | **not passed** | `policy_violation` |
| `Artifacts\project\sovereignshield-mobile\app.py` | 168 | `sovereignshield` | **not passed** | `session_end` |
| `Artifacts\project\sovereignshield-mobile\app.py` | 353 | `sovereignshield` | **not passed** | `policy_violation` |
| `Artifacts\scripts\smoke_test_findings.py` | 91, 100 | all three families | **not passed** | `audit_flag`, `star_gap`, `policy_violation`, `session_end` |

### 2B. `insert_cross_app_finding` (REST via `supabase_platform`)

Defined at `insert_cross_app_finding` in each `supabase_platform.py` (~line 82: `.table("cross_app_findings").insert(row)`).

**Callers (`record_finding` → `insert_cross_app_finding`):**

| Integration module | Called from (examples) |
|----------------------|-------------------------|
| `Artifacts\project\auditshield\auditshield_platform_integration.py` | `Artifacts\project\auditshield\app.py` ~1648 |
| `Artifacts\project\auditshield\starguard-desktop\starguard_platform_integration.py` | `starguard-desktop\app.py` ~2126 |
| `Artifacts\project\sovereignshield\sovereignshield_platform_integration.py` | `sovereignshield\app.py` ~1233 |

**Row shape today:** `source_app`, `finding_type`, `title`, `description`, `severity`, `status` (`open`), optional **`session_id`**, plus `**kwargs` (e.g. `measure_id`, `policy_id`, `payload` dict merged into row).

**Note:** `auditshield_platform_integration.record_finding` passes `session_id=None` explicitly (comment: UUID expectation) — other apps pass Shiny `session_id` in some paths.

### 2C. Hub read-only (no insert)

| File | Line | Role |
|------|------|------|
| `platform-hub\app.py` | 265–268 | `select` on `cross_app_findings` for UI DataFrame |

---

## 3. Env var contract (by sub-app / area)

Summarized from `os.environ.get` / `getenv` on `SUPABASE*` under `Artifacts\project` (+ `platform-hub` from prior read).

| Area | Env vars read (typical) | Notes |
|------|-------------------------|--------|
| **platform-hub** | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `PLATFORM_SUPABASE_*`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_KEY` | HF Space secrets names match `SUPABASE_*` |
| **supabase_platform** (auditshield, starguard-desktop, sovereignshield) | `PLATFORM_SUPABASE_URL` \|\| `SUPABASE_URL`; `PLATFORM_SUPABASE_ANON_KEY` \|\| `SUPABASE_ANON_KEY` \|\| `SUPABASE_SERVICE_ROLE_KEY` \|\| `SUPABASE_KEY` | REST path for `record_finding` |
| **supabase_findings** (all copies) | `PLATFORM_DATABASE_URL`, `DATABASE_URL`, `SUPABASE_DB_URL` | Direct Postgres; not HTTP |
| **sovereignshield-mobile `app.py`** | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY` | **Hardcoded default URL still typo Sovereign:** `jdvtlonneybqivcjtsj` (see §4) |
| **sovereignshield `core/audit_log.py`, `audit_db.py`** | `SUPABASE_URL`, `SUPABASE_ANON_KEY` / `SUPABASE_SERVICE_KEY` | App-local Supabase (not findings helper) |
| **hedis_gap_trail** (desktop + mobile) | `SUPABASE_URL`, `SUPABASE_ANON_KEY` | Gap trail feature |
| **auditshield `audit_trail.py`** | `SUPABASE_URL`, `SUPABASE_KEY` | Audit trail |

**Finding types observed in calls:** `session_end`, `star_gap`, `audit_flag`, `policy_violation`, `hcc_flag`, `hedis_gap`, `opa_violation` (ensure T3 / Hub KPI view tolerates full set).

---

## 4. Sovereign / Primary refs to rotate or fix

| Path | Line | Pattern |
|------|------|---------|
| `Artifacts\project\sovereignshield-mobile\app.py` | 103 | Default `SUPABASE_URL` → **`https://jdvtlonneybqivcjtsj.supabase.co`** (**wrong project id substring** vs corrected `jdvtlonnejybqivcjtsj`) |
| `Artifacts\scripts\smoke_test_findings.py` | 12 (comment) | Documents `jdvtlonneybqivcjtsj` |
| `Artifacts\project\sovereignshield\scripts\audit_runs_schema.sql` | 2 (comment) | `jdvtlonneybqivcjtsj` |

**Primary ref `wiwmphjkupcnntawpafg`** in repo today: only under `platform-hub\sql\` (T3 files + this map) — **no app runtime** hardcodes Primary yet.

---

## 5. T4 apply plan (proposed — **not implemented**)

*T3 SQL in `platform-hub/sql/` was reconciled on **2026-05-14** to match the live helper column set + additive `sub_surface`. T4 no longer needs column renames or a `payload`-only migration for inserts.*

1. **`sub_surface` on every insert (only new required field after T3)**
   - **Rule of thumb:** path or app id containing `mobile` / `starguard-mobile` / `sovereignshield-mobile` → `'mobile'`; desktop Shiny apps → `'desktop'`; **AuditShield Live** (single responsive Space) → operator choice: `'desktop'` or **NULL** (“live” variant) per D2 note.
   - Extend **`insert_finding`** SQL in **all** `supabase_findings.py` copies to include **`sub_surface`** in the INSERT column list (default `NULL` until each call site passes an explicit value).
   - Extend **`insert_cross_app_finding`** / `record_finding` callers to pass **`sub_surface`** in the row dict (same folder heuristic).

2. **Primary vs Sovereign hosts**
   - HF Hub + each Space: set **`SUPABASE_URL` / keys to Primary** when Q1 is enforced.
   - **Focused branch (T3.5, deferred):** fix **sovereignshield-mobile** default URL typo (`jdvtlonneybqivcjtsj` → `jdvtlonnejybqivcjtsj`) or remove hardcoded default — **not bundled** with T3 SQL per focused-branch rule.

3. **Unify two write paths** (optional but reduces drift)
   - Today: psycopg2 (`insert_finding`) vs REST (`insert_cross_app_finding`). T4 may standardize on one + one env story (`DATABASE_URL` vs `SUPABASE_URL`).

4. **`platform-hub`**
   - After Primary migration: point Hub secrets to Primary; `fetch_findings` / KPI queries use `platform_hub_kpis`. **RLS refinement (same day):** anon Hub key does **not** need rotation for KPI reads — `GRANT SELECT` on the **view** plus `security_invoker = false` replaces adding an `anon` policy on raw `cross_app_findings`. **Sub-app** `SUPABASE_URL` rotation (Sovereign → Primary) is still T4/T2.c if T2.c confirms the wrong project.

---

## 6. Risk notes

| Risk | Detail |
|------|--------|
| **Legacy Primary shape** | If an existing `cross_app_findings` table on Primary predates helpers (extra/renamed columns), run a **manual diff** before `t3_primary_alter.sql`; script uses `ADD COLUMN IF NOT EXISTS` only — never drops legacy columns. |
| **RLS vs anon Hub reads** | Addressed in T3 SQL: **`GRANT SELECT` on `platform_hub_kpis` to `anon`** + view **`WITH (security_invoker = false)`** + **`REVOKE ALL` on `cross_app_findings` FROM `anon`**. Hub keeps using **`SUPABASE_ANON_KEY`** (no key-type change for this RLS tweak). |
| **INSERT role** | Policies allow **INSERT/UPDATE** for **`service_role`** only. Spaces posting with **anon** key will fail until policy or client key alignment is decided. |
| **Duplicate modules** | Six `supabase_findings.py` + three `supabase_platform.py` — edits must be **replicated or consolidated** (shared-first policy). |
| **`finding_type` vocabulary** | Includes `hcc_flag`, `hedis_gap`, `opa_violation` — confirm Hub KPI / view logic counts desired subset. |
| **Sovereign mobile typo** | Wrong ref `jdvtlonneybqivcjtsj` — **T3.5** focused branch (not this deliverable). |
| **No `sub_surface` in app inserts yet** | All current writes omit D2 `sub_surface`; T4 adds it in Python/SQL insert lists once T3 is applied. |
| **Trigger syntax** | If `EXECUTE FUNCTION` on `caf_set_updated_at` fails, use `EXECUTE PROCEDURE` per `T3_README.md`. |

---

## 7. Operator checklist (post T2.c / T3)

- [ ] Run T2.c SQL on Primary; pick **T3 branch A vs B** per `T3_README.md`.  
- [ ] Reconcile T3 DDL with **actual** `cross_app_findings` shape if table pre-exists on Sovereign dump.  
- [ ] Rotate HF Hub `SUPABASE_URL` + `SUPABASE_ANON_KEY` to **Primary**.  
- [ ] Implement §5; re-run `smoke_test_findings.py` against Primary.  
- [ ] Option A (Primary MCP) recommended for T4/T5 durable access.
