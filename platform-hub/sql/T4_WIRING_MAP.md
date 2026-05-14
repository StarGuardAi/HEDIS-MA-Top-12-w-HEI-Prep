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

## 5. T4 apply plan (concrete diffs -- v3)

*T3 SQL (`t3_primary_create.sql` / `t3_primary_alter.sql`) adds nullable `sub_surface` with CHECK (`desktop` \| `mobile` \| NULL). This section replaces strategic Section 5 prose with **patchable** before/after snippets. T4-code-stage Phase 1 gate: count `Artifacts/.../*.py` path mentions and `` ```python `` fences in this section only.*

### 5.0 Design locks (operator-approved)

- **D2.1 -- AuditShield Live `sub_surface`:** use Python **`None`** so Postgres stores **NULL** (responsive single-surface web; Hub UI maps NULL to **Live**). When a separate AuditShield Mobile Space ships, that app passes **`"mobile"`** (not covered by the Live tree today).
- **D2.2 -- `PLATFORM_*` env split (findings psycopg2 path only):** apply **only** in the **six** `supabase_findings.py` files listed in Section 1 (`Artifacts/shared` + five vendored copies). **`supabase_platform.py`** (three copies) stays on the existing **`PLATFORM_SUPABASE_URL` / `SUPABASE_URL`** REST chain for **native** project tables (`audit_runs`, `platform_sessions`, etc.) -- **no** D2.2 change there.
- **Branch base for SovereignShield Desktop `insert_finding` rows:** `Artifacts/project/sovereignshield/app.py` gains `insert_finding` call sites on branch **`wip/sovereign-session-end-wiring`** (not on `docs/t3-t4-staging` alone). **T4-code-stage** shall branch from **`wip/sovereign-session-end-wiring`** so line anchors below match `git show wip/sovereign-session-end-wiring:Artifacts/project/sovereignshield/app.py`.

### 5.1 Helper - `insert_finding` signature + INSERT SQL (verbatim BEFORE / AFTER)

D2.2 lock: PLATFORM_* fallback applies only to the six `supabase_findings.py`
copies. `supabase_platform.py` files are NOT modified (native project access).

**File:** `Artifacts/shared/supabase_findings.py` (canonical; full function below - no ellipses)

```python
# BEFORE
def insert_finding(
    *,
    source_app: str,
    finding_type: str,
    severity: str = "info",
    status: str = "open",
    title: str | None = None,
    description: str | None = None,
    trigger_type: str,
    session_id: str | None = None,
    extra_metadata: dict[str, Any] | None = None,
    measure_id: str | None = None,
    policy_id: str | None = None,
) -> bool:
    """Insert one row into cross_app_findings. Returns True on success.

    Args:
        source_app:     "auditshield" | "starguard" | "sovereignshield"
        finding_type:   "audit_flag" | "star_gap" | "policy_violation" | "session_end"
        severity:       "info" | "low" | "medium" | "high" | "critical"
        status:         "open" (action triggers) | "remediated" (session-end rows)
        title:          short human-readable label shown in Hub
        description:    optional longer detail
        trigger_type:   "action" | "session_end"
        session_id:     client session uuid
        extra_metadata: any additional key/value pairs stored in metadata jsonb
        measure_id:     folded into metadata if table has no top-level column
        policy_id:      folded into metadata if table has no top-level column
    """
    dsn = _get_postgres_dsn()
    if not dsn:
        print(
            "[findings] No postgres DSN (PLATFORM_DATABASE_URL / DATABASE_URL / SUPABASE_DB_URL) "
            "— skipping insert (http(s):// URLs are ignored)",
            file=sys.stderr,
        )
        return False

    now = datetime.now(timezone.utc)
    meta: dict[str, Any] = {
        "trigger_type": trigger_type,
        "client_session_id": session_id,
        **(extra_metadata or {}),
    }
    if measure_id is not None:
        meta["measure_id"] = str(measure_id)
    if policy_id is not None:
        meta["policy_id"] = str(policy_id)

    sql = (
        f"INSERT INTO {_TABLE} "
        "(source_app, finding_type, severity, status, title, description, metadata, created_at, updated_at) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    args = (
        source_app,
        finding_type,
        severity,
        status,
        title,
        description,
        Json(meta),
        now,
        now,
    )

    try:
        conn = psycopg2.connect(dsn, connect_timeout=10)
        try:
            with conn.cursor() as cur:
                cur.execute(sql, args)
            conn.commit()
        finally:
            conn.close()
        return True
    except Exception as exc:
        print(
            f"[findings] insert failed ({exc}) — source_app={source_app} "
            f"finding_type={finding_type} trigger_type={trigger_type}",
            file=sys.stderr,
        )
        return False
```

```python
# AFTER
def insert_finding(
    *,
    source_app: str,
    finding_type: str,
    severity: str = "info",
    status: str = "open",
    title: str | None = None,
    description: str | None = None,
    trigger_type: str,
    session_id: str | None = None,
    extra_metadata: dict[str, Any] | None = None,
    measure_id: str | None = None,
    policy_id: str | None = None,
    sub_surface: str | None = None,
) -> bool:
    """Insert one row into cross_app_findings. Returns True on success.

    Args:
        source_app:     "auditshield" | "starguard" | "sovereignshield"
        finding_type:   "audit_flag" | "star_gap" | "policy_violation" | "session_end"
        severity:       "info" | "low" | "medium" | "high" | "critical"
        status:         "open" (action triggers) | "remediated" (session-end rows)
        title:          short human-readable label shown in Hub
        description:    optional longer detail
        trigger_type:   "action" | "session_end"
        session_id:     client session uuid
        extra_metadata: any additional key/value pairs stored in metadata jsonb
        measure_id:     folded into metadata if table has no top-level column
        policy_id:      folded into metadata if table has no top-level column
    """
    dsn = _get_postgres_dsn()
    if not dsn:
        print(
            "[findings] No postgres DSN (PLATFORM_DATABASE_URL / DATABASE_URL / SUPABASE_DB_URL) "
            "— skipping insert (http(s):// URLs are ignored)",
            file=sys.stderr,
        )
        return False

    now = datetime.now(timezone.utc)
    meta: dict[str, Any] = {
        "trigger_type": trigger_type,
        "client_session_id": session_id,
        **(extra_metadata or {}),
    }
    if measure_id is not None:
        meta["measure_id"] = str(measure_id)
    if policy_id is not None:
        meta["policy_id"] = str(policy_id)

    sql = (
        f"INSERT INTO {_TABLE} "
        "(source_app, finding_type, severity, status, title, description, metadata, sub_surface, created_at, updated_at) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    args = (
        source_app,
        finding_type,
        severity,
        status,
        title,
        description,
        Json(meta),
        sub_surface,
        now,
        now,
    )

    try:
        conn = psycopg2.connect(dsn, connect_timeout=10)
        try:
            with conn.cursor() as cur:
                cur.execute(sql, args)
            conn.commit()
        finally:
            conn.close()
        return True
    except Exception as exc:
        print(
            f"[findings] insert failed ({exc}) — source_app={source_app} "
            f"finding_type={finding_type} trigger_type={trigger_type}",
            file=sys.stderr,
        )
        return False
```

Apply the SAME pattern to the five vendored copies (path inventory in Section 1):

- `Artifacts/project/auditshield/shared/supabase_findings.py`
- `Artifacts/project/auditshield/starguard-desktop/shared/supabase_findings.py`
- `Artifacts/project/auditshield/starguard-mobile/Artifacts/app/shared/supabase_findings.py`
- `Artifacts/project/sovereignshield/shared/supabase_findings.py`
- `Artifacts/project/sovereignshield-mobile/shared/supabase_findings.py`

Each copy gets the same signature add (`sub_surface: str | None = None`) and the same
INSERT column list / VALUES tuple extension (`sub_surface` after `metadata`, matching T3 DDL).
### 5.2 Call sites — `insert_finding(...)` (add `sub_surface=` literal)

Literal rule used below (extends D2.1):

| Path pattern | `sub_surface` literal |
|--------------|------------------------|
| `Artifacts/project/auditshield/app.py` (Live) | `None` |
| `Artifacts/project/auditshield/starguard-desktop/...` | `"desktop"` |
| `Artifacts/project/auditshield/starguard-mobile/...` | `"mobile"` |
| `Artifacts/project/sovereignshield/...` (desktop Shiny) | `"desktop"` |
| `Artifacts/scripts/smoke_test_findings.py` | `None` for `auditshield` rows; `"desktop"` for `starguard` and `sovereignshield` rows in `TEST_CASES` (script runs as a dev harness, not a mobile Space) |

#### 5.2a `Artifacts/project/auditshield/app.py` — line ~708 — `sub_surface=None`

```python
# BEFORE
        insert_finding(
            source_app="auditshield",
            finding_type="session_end",
            severity="info",
            status="remediated",
            title="Session ended",
            trigger_type="session_end",
            session_id=_SESSION_ID,
        )
```

```python
# AFTER
        insert_finding(
            source_app="auditshield",
            finding_type="session_end",
            severity="info",
            status="remediated",
            title="Session ended",
            trigger_type="session_end",
            session_id=_SESSION_ID,
            sub_surface=None,
        )
```

#### 5.2b `Artifacts/project/auditshield/starguard-desktop/app.py` — line ~1991 — `sub_surface="desktop"`

```python
# BEFORE
        insert_finding(
            source_app="starguard",
            finding_type="session_end",
            severity="info",
            status="remediated",
            title="Session ended",
            trigger_type="session_end",
            session_id=_fc_sid,
            extra_metadata={"session_duration_s": int(time.monotonic() - _fc_t0)},
        )
```

```python
# AFTER
        insert_finding(
            source_app="starguard",
            finding_type="session_end",
            severity="info",
            status="remediated",
            title="Session ended",
            trigger_type="session_end",
            session_id=_fc_sid,
            extra_metadata={"session_duration_s": int(time.monotonic() - _fc_t0)},
            sub_surface="desktop",
        )
```

#### 5.2c `Artifacts/project/auditshield/starguard-desktop/app.py` — line ~4429 — `sub_surface="desktop"`

```python
# BEFORE
            insert_finding(
                source_app="starguard",
                finding_type="star_gap",
                severity="info",
                status="open",
                title="HEDIS calculate run",
                trigger_type="action",
                session_id=_fc_sid,
                extra_metadata={"action": "hedis_run_single"},
            )
```

```python
# AFTER
            insert_finding(
                source_app="starguard",
                finding_type="star_gap",
                severity="info",
                status="open",
                title="HEDIS calculate run",
                trigger_type="action",
                session_id=_fc_sid,
                extra_metadata={"action": "hedis_run_single"},
                sub_surface="desktop",
            )
```

#### 5.2d `Artifacts/project/auditshield/starguard-mobile/Artifacts/app/app.py` — line ~349 — `sub_surface="mobile"`

```python
# BEFORE
        insert_finding(
            source_app="starguard",
            finding_type="session_end",
            severity="info",
            status="remediated",
            title="Session ended",
            trigger_type="session_end",
            session_id=_fc_sid,
            extra_metadata={"session_duration_s": int(time.monotonic() - _fc_t0)},
        )
```

```python
# AFTER
        insert_finding(
            source_app="starguard",
            finding_type="session_end",
            severity="info",
            status="remediated",
            title="Session ended",
            trigger_type="session_end",
            session_id=_fc_sid,
            extra_metadata={"session_duration_s": int(time.monotonic() - _fc_t0)},
            sub_surface="mobile",
        )
```

#### 5.2e `Artifacts/project/auditshield/starguard-mobile/Artifacts/app/pages/hedis_analyzer.py` — line ~177 — `sub_surface="mobile"`

```python
# BEFORE
        insert_finding(
            source_app="starguard",
            finding_type="star_gap",
            severity="info",
            status="open",
            title="Gaps and ROI analysis run",
            trigger_type="action",
            session_id=findings_session_id,
            extra_metadata={"action": "analyze_btn"},
        )
```

```python
# AFTER
        insert_finding(
            source_app="starguard",
            finding_type="star_gap",
            severity="info",
            status="open",
            title="Gaps and ROI analysis run",
            trigger_type="action",
            session_id=findings_session_id,
            extra_metadata={"action": "analyze_btn"},
            sub_surface="mobile",
        )
```

#### 5.2h `Artifacts/scripts/smoke_test_findings.py` — loop + session_end

**Loop body (~line 91):** add `sub_surface` per `tc` dict — extend each `TEST_CASES` dict with the literal, *or* pass at call site:

```python
# BEFORE
for tc in TEST_CASES:
    ok = insert_finding(session_id=_SESSION_ID, **tc)
```

```python
# AFTER (explicit per-row literals; preferred for gate clarity)
for tc in TEST_CASES:
    surf = None
    if tc["source_app"] == "auditshield":
        surf = None
    elif tc["source_app"] == "starguard":
        surf = "desktop"
    elif tc["source_app"] == "sovereignshield":
        surf = "desktop"
    ok = insert_finding(session_id=_SESSION_ID, sub_surface=surf, **tc)
```

```python
# BEFORE (session_end row ~line 100)
ok = insert_finding(
    source_app="auditshield",
    finding_type="session_end",
    severity="info",
    status="remediated",
    title="[SMOKE TEST] Session ended",
    trigger_type="session_end",
    session_id=_SESSION_ID,
    extra_metadata={"action": "smoke_test_teardown"},
)
```

```python
# AFTER
ok = insert_finding(
    source_app="auditshield",
    finding_type="session_end",
    severity="info",
    status="remediated",
    title="[SMOKE TEST] Session ended",
    trigger_type="session_end",
    session_id=_SESSION_ID,
    extra_metadata={"action": "smoke_test_teardown"},
    sub_surface=None,
)
```

#### 5.2i `Artifacts/project/sovereignshield/app.py` — **wip branch** — session_end + policy_violation inserts — `sub_surface="desktop"` each

*Source: `wip/sovereign-session-end-wiring` (two `insert_finding` blocks inside `server()`).*

```python
# BEFORE
        insert_finding(
            source_app="sovereignshield",
            finding_type="session_end",
            severity="info",
            status="remediated",
            title="Session ended",
            trigger_type="session_end",
            session_id=_fc_sid,
            extra_metadata={"session_duration_s": int(time.monotonic() - _fc_t0)},
        )
```

```python
# AFTER
        insert_finding(
            source_app="sovereignshield",
            finding_type="session_end",
            severity="info",
            status="remediated",
            title="Session ended",
            trigger_type="session_end",
            session_id=_fc_sid,
            extra_metadata={"session_duration_s": int(time.monotonic() - _fc_t0)},
            sub_surface="desktop",
        )
```

```python
# BEFORE
        insert_finding(
            source_app="sovereignshield",
            finding_type="policy_violation",
            severity="info",
            status="open",
            title="OPA policy evaluation run",
            trigger_type="action",
            session_id=_fc_sid,
            extra_metadata={"action": "opa_eval"},
        )
```

```python
# AFTER
        insert_finding(
            source_app="sovereignshield",
            finding_type="policy_violation",
            severity="info",
            status="open",
            title="OPA policy evaluation run",
            trigger_type="action",
            session_id=_fc_sid,
            extra_metadata={"action": "opa_eval"},
            sub_surface="desktop",
        )
```

### 5.2j `record_finding(...)` call sites — pass `sub_surface` through kwargs to REST row

`insert_cross_app_finding` merges `**kwargs` into the insert row (see `Artifacts/project/auditshield/supabase_platform.py`). **Do not edit** `supabase_platform.py` for D2.2 — add the kwarg at **call sites** only.

#### `Artifacts/project/auditshield/app.py` ~1648 — `sub_surface=None`

```python
# BEFORE
                record_finding(
                    source_app="auditshield",
                    finding_type="hcc_flag",
                    title=f"RADV Audit {audit_id}",
                    description=f"Audit {input.new_audit_notice_id()} - {input.new_contract_id()}",
                    severity="high" if sample_size > 100 else "medium",
                    session_id=getattr(session, "session_id", None),
                )
```

```python
# AFTER
                record_finding(
                    source_app="auditshield",
                    finding_type="hcc_flag",
                    title=f"RADV Audit {audit_id}",
                    description=f"Audit {input.new_audit_notice_id()} - {input.new_contract_id()}",
                    severity="high" if sample_size > 100 else "medium",
                    session_id=getattr(session, "session_id", None),
                    sub_surface=None,
                )
```

#### `Artifacts/project/auditshield/starguard-desktop/app.py` ~2126 — `sub_surface="desktop"`

```python
# BEFORE
                record_finding(
                    source_app="starguard",
                    finding_type="hedis_gap",
                    title=f"{record.get('measure_code', 'HEDIS')} gap — {record.get('member_id', 'unknown')}",
                    description=record.get("claude_recommendation"),
                    severity=_gap_severity(record),
                    session_id=getattr(session, "session_id", None),
                    measure_id=record.get("measure_code"),
                    payload={"provider": record.get("provider_name"), "star_value": record.get("star_impact")},
                )
```

```python
# AFTER
                record_finding(
                    source_app="starguard",
                    finding_type="hedis_gap",
                    title=f"{record.get('measure_code', 'HEDIS')} gap — {record.get('member_id', 'unknown')}",
                    description=record.get("claude_recommendation"),
                    severity=_gap_severity(record),
                    session_id=getattr(session, "session_id", None),
                    measure_id=record.get("measure_code"),
                    payload={"provider": record.get("provider_name"), "star_value": record.get("star_impact")},
                    sub_surface="desktop",
                )
```

#### `Artifacts/project/sovereignshield/app.py` ~1194 — `sub_surface="desktop"`

```python
# BEFORE
                    record_finding(
                        source_app="sovereignshield",
                        finding_type="opa_violation",
                        title=f"Policy violation: {violation.get('violation_type', violation.get('rule', 'unknown'))}",
                        description=violation.get("detail", violation.get("message")),
                        severity=_opa_severity(violation),
                        session_id=getattr(session, "session_id", None),
                        policy_id=violation.get("violation_type", violation.get("rule")),
                        payload={
                            "opa_result": violation,
                            "terraform_file": uploaded_filename,
                            "audit_run_id": run_id,
                        },
                    )
```

```python
# AFTER
                    record_finding(
                        source_app="sovereignshield",
                        finding_type="opa_violation",
                        title=f"Policy violation: {violation.get('violation_type', violation.get('rule', 'unknown'))}",
                        description=violation.get("detail", violation.get("message")),
                        severity=_opa_severity(violation),
                        session_id=getattr(session, "session_id", None),
                        policy_id=violation.get("violation_type", violation.get("rule")),
                        payload={
                            "opa_result": violation,
                            "terraform_file": uploaded_filename,
                            "audit_run_id": run_id,
                        },
                        sub_surface="desktop",
                    )
```
#### 5.2-DEFERRED - SovereignShield Mobile (psycopg2 findings path)

Original #### 5.2f / #### 5.2g are removed in Section 5 v3: they assumed psycopg2 findings inserts on branch ``wip/sovereign-session-end-wiring @ eb9c888`` under ``Artifacts/project/sovereignshield-mobile/``. On that base, ``grep`` for the shared helper used by other apps shows **no** call sites in that tree (only ``sys.path.insert`` / ``audit_runs`` patterns). SovereignShield Mobile is not a ``cross_app_findings`` emitter today.

Adding emissions is a **new feature**, not T4 prep. Tracked as **T4.5** follow-up sprint:

- Design call sites mirroring SovereignShield Desktop session_end + policy_violation emissions
- Bank on focused branch ``feat/sovereignshield-mobile-findings-wiring``
- Then a thin T4.5 code-stage adds ``sub_surface="mobile"`` to those new calls

Out of scope for T4 round 1.

### 5.3 D2.2 — `_get_postgres_dsn` env fallback (six `supabase_findings.py` copies only)

**BEFORE** (all six copies today — excerpt):

```python
def _get_postgres_dsn() -> str:
    for name in ("PLATFORM_DATABASE_URL", "DATABASE_URL", "SUPABASE_DB_URL"):
        v = (os.environ.get(name) or "").strip()
        if not v:
            continue
        low = v.lower()
        if low.startswith("http://") or low.startswith("https://"):
            continue
        if low.startswith("postgresql://") or low.startswith("postgres://"):
            return v
    return ""
```

**AFTER** — insert optional **`PLATFORM_DB_URL`** (Space-specific alias) **after** `PLATFORM_DATABASE_URL`, still rejecting `http(s)://` values (REST bases must not be mistaken for DSN):

```python
def _get_postgres_dsn() -> str:
    # D2.2 — cross_app_findings psycopg2 path: platform-scoped TCP DSNs before generic app secrets.
    for name in (
        "PLATFORM_DATABASE_URL",
        "PLATFORM_DB_URL",
        "DATABASE_URL",
        "SUPABASE_DB_URL",
    ):
        v = (os.environ.get(name) or "").strip()
        if not v:
            continue
        low = v.lower()
        if low.startswith("http://") or low.startswith("https://"):
            continue
        if low.startswith("postgresql://") or low.startswith("postgres://"):
            return v
    return ""
```

Replicate verbatim across: `Artifacts/shared/supabase_findings.py`, `Artifacts/project/auditshield/shared/supabase_findings.py`, `Artifacts/project/auditshield/starguard-desktop/shared/supabase_findings.py`, `Artifacts/project/auditshield/starguard-mobile/Artifacts/app/shared/supabase_findings.py`, `Artifacts/project/sovereignshield/shared/supabase_findings.py`, `Artifacts/project/sovereignshield-mobile/shared/supabase_findings.py`.

### 5.4 Gate self-check (T4-code-stage Phase 1)

Run on this section substring only (between `## 5.` and `## 6.`).

- **Total files referenced:** 29 (Section 5 substring: `Artifacts/.../*.py` regex count)
- **Total fenced blocks:** 29 (markdown fenced code blocks opened with the python tag in Section 5 only)

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
- [ ] Implement Section 5; re-run `smoke_test_findings.py` against Primary.  
- [ ] Option A (Primary MCP) recommended for T4/T5 durable access.
