# T4 Secret audit — Hugging Face Spaces (sub-apps + context)

**Generated:** 2026-05-14 (America/New_York)  
**Method:** `GET https://huggingface.co/api/spaces/{repo}/secrets` and `.../variables` with bearer **`HF_TOKEN`** (value never logged). Secret **values** are never returned by the secrets API; only **key names** and **`updatedAt`** metadata. **Variables** endpoint returned **empty objects** for all five Spaces at audit time (no key/value pairs to report).  
**Branch at audit run:** `fix/sovereign-id-typo` (operator may merge T3.5 separately).  
**Cross-app writers (from `T4_WIRING_MAP.md` §2):** all five Spaces host code paths that call `insert_finding` and/or `record_finding` → `cross_app_findings` (AuditShield Live, StarGuard desktop/mobile, SovereignShield desktop/mobile).

---

## 1. Methodology

| Item | Detail |
|------|--------|
| API | Hugging Face Hub REST, same pattern as T2.a Hub probe |
| Auth | `Authorization: Bearer <HF_TOKEN>` |
| Rate limit | ~300 ms delay between Space requests |
| Date heuristics (metadata only) | **`updatedAt` &lt; 2026-04-01** → treat as **pre–Q1 / likely legacy project** (often Sovereign-era or early Primary; **host not visible in API**). **`updatedAt` &gt; 2026-05-01** → **recent touch** (may already match intended target; still verify in UI). Between 04/01 and 05/01 → **review**. |
| Limits | No POST/PUT; no DB; no secret values printed |

---

## 2. Per-Space inventory

### 2.1 `rreichert/auditshield-live`

**Errors:** none.

**Space variables:** none returned.

**Secret keys (key + `updatedAt` only):**

| Key | updatedAt (UTC) |
|-----|-----------------|
| ANTHROPIC_API_KEY | 2026-05-04T19:41:50.107Z |
| GSHEETS_CREDS_JSON | 2026-03-05T22:46:31.585Z |
| AUDIT_SHEET_ID | 2026-03-05T22:51:48.512Z |
| AUDIT_SHEET | 2026-03-05T22:54:21.457Z |
| SUPABASE_URL | 2026-03-06T03:30:12.281Z |
| SUPABASE_ANON_KEY | 2026-03-06T03:31:21.983Z |
| PLATFORM_SUPABASE_ANON_KEY | 2026-03-24T18:49:12.132Z |
| PLATFORM_SUPABASE_URL | 2026-03-24T18:48:45.957Z |
| DATABASE_URL | 2026-03-28T01:55:05.565Z |

**Notes:** Native `SUPABASE_*` touched **2026-03-06** (before 04/01). `PLATFORM_SUPABASE_*` touched **2026-03-24** (before 04/01). Matches **split pattern** (native app vs platform / findings path per `supabase_platform.py`).

---

### 2.2 `rreichert/starguard-desktop`

**Errors:** none.

**Space variables:** none returned.

**Secret keys:**

| Key | updatedAt (UTC) |
|-----|-----------------|
| ANTHROPIC_API_KEY | 2026-05-14T00:52:28.365Z |
| GSHEETS_CREDS_JSON | 2026-03-05T22:57:39.013Z |
| HEDIS_SHEET_ID | 2026-03-05T22:58:11.899Z |
| STAR_CACHE_SHEET_ID | 2026-03-05T22:58:43.803Z |
| SUPABASE_ANON_KEY | 2026-03-06T03:33:52.646Z |
| SUPABASE_URL | 2026-03-06T03:34:31.241Z |
| PLATFORM_SUPABASE_ANON_KEY | 2026-03-17T18:33:03.598Z |
| PLATFORM_SUPABASE_URL | 2026-03-17T18:33:49.262Z |
| DATABASE_URL | 2026-03-28T15:24:35.173Z |

**Notes:** Same split. `ANTHROPIC_API_KEY` shows **2026-05-14** (recent); Supabase-related rows remain **March 2026**.

---

### 2.3 `rreichert/starguard-mobile`

**Errors:** none.

**Space variables:** none returned.

**Secret keys:**

| Key | updatedAt (UTC) |
|-----|-----------------|
| ANTHROPIC_API_KEY | 2026-05-13T02:19:20.404Z |
| STAR_CACHE_SHEET_ID | 2026-03-05T23:55:31.447Z |
| HEDIS_SHEET_ID | 2026-03-05T23:55:04.777Z |
| GSHEETS_CREDS_JSON | 2026-03-05T23:54:14.715Z |
| SUPABASE_URL | 2026-03-06T03:35:57.399Z |
| SUPABASE_ANON_KEY | 2026-03-06T03:37:27.794Z |
| PLATFORM_SUPABASE_ANON_KEY | 2026-03-24T18:06:39.704Z |
| PLATFORM_SUPABASE_URL | 2026-03-24T18:07:11.468Z |
| DATABASE_URL | 2026-03-28T15:25:24.846Z |

---

### 2.4 `rreichert/sovereignshield`

**Errors:** none.

**Space variables:** none returned.

**Secret keys:**

| Key | updatedAt (UTC) |
|-----|-----------------|
| ANTHROPIC_API_KEY | 2026-03-10T01:07:02.196Z |
| SOVEREIGN_SUPABASE_ANON_KEY | 2026-03-12T02:43:46.596Z |
| SOVEREIGN_SUPABASE_URL | 2026-03-12T02:44:21.335Z |
| PLATFORM_SUPABASE_URL | 2026-03-17T18:28:47.975Z |
| PLATFORM_SUPABASE_ANON_KEY | 2026-03-17T18:29:19.378Z |
| DATABASE_URL | 2026-03-28T15:25:57.861Z |

**Notes:** **No `SUPABASE_URL` secret key** — native project uses **`SOVEREIGN_SUPABASE_URL`** / **`SOVEREIGN_SUPABASE_ANON_KEY`** naming. `supabase_platform.py` still resolves **`SUPABASE_URL` OR `PLATFORM_SUPABASE_URL`** for cross-app inserts; confirm in Space UI that env injection maps native URL to these keys or that `SUPABASE_URL` is set elsewhere (e.g. Docker env not listed as HF “secret”).

---

### 2.5 `rreichert/sovereignshield-mobile`

**Errors:** none.

**Space variables:** none returned.

**Secret keys:**

| Key | updatedAt (UTC) |
|-----|-----------------|
| SUPABASE_URL | 2026-03-28T14:28:31.341Z |
| SUPABASE_ANON_KEY | 2026-03-28T14:29:12.175Z |
| DATABASE_URL | 2026-03-28T15:26:34.618Z |
| PLATFORM_SUPABASE_URL | 2026-04-29T15:07:15.201Z |
| PLATFORM_SUPABASE_ANON_KEY | 2026-04-29T15:05:33.654Z |
| ANTHROPIC_API_KEY | 2026-04-29T17:26:43.354Z |

**Notes:** `PLATFORM_*` touched **2026-04-29** (after 04/01, before 05/01 — **review band**). Native `SUPABASE_*` **2026-03-28**.

---

## 3. Rotation surface summary

**Host is unknown from API** (no secret values). Use **HF Space → Settings → Secrets** to read URL host: compare to **Primary** `wiwmphjkupcnntawpafg.supabase.co`, **Sovereign** `jdvtlonnejybqivcjtsj.supabase.co`, and each app’s **native** project if split.

| Space | Primary native `SUPABASE_URL` updatedAt (or substitute) | `PLATFORM_SUPABASE_URL` updatedAt | `cross_app_findings` writer (T4 map) | Likely rotation need (Q1: findings on Primary) |
|-------|----------------------------------------------------------|-------------------------------------|--------------------------------------|-----------------------------------------------|
| auditshield-live | 2026-03-06 | 2026-03-24 | Yes | **Yes** — rotate **`PLATFORM_SUPABASE_*`** (and matching service key if used) to **Primary** once T3 applied; re-validate native `SUPABASE_*` only if app data should also move. |
| starguard-desktop | 2026-03-06 | 2026-03-17 | Yes | **Yes** — same pattern for `PLATFORM_*`. |
| starguard-mobile | 2026-03-06 | 2026-03-24 | Yes | **Yes** — same. |
| sovereignshield | *no `SUPABASE_URL` key*; `SOVEREIGN_SUPABASE_URL` 2026-03-12 | 2026-03-17 | Yes | **Yes** for **`PLATFORM_SUPABASE_*` → Primary**; native likely stays Sovereign unless product decision migrates OPA tables. |
| sovereignshield-mobile | 2026-03-28 | 2026-04-29 | Yes | **Review** — `PLATFORM_*` newer than 04/01 but still verify host; native keys end of March. |

**“Needs rotation?”** = operator must **open UI** and confirm host; **metadata alone cannot prove Sovereign vs Primary.**

---

## 4. Operator HF UI checklist

Base URL pattern: `https://huggingface.co/spaces/<repo>/settings` (Secrets tab).

| Space | Settings URL |
|-------|----------------|
| AuditShield Live | https://huggingface.co/spaces/rreichert/auditshield-live/settings |
| StarGuard Desktop | https://huggingface.co/spaces/rreichert/starguard-desktop/settings |
| StarGuard Mobile | https://huggingface.co/spaces/rreichert/starguard-mobile/settings |
| SovereignShield | https://huggingface.co/spaces/rreichert/sovereignshield/settings |
| SovereignShield Mobile | https://huggingface.co/spaces/rreichert/sovereignshield-mobile/settings |
| Platform Hub (context) | https://huggingface.co/spaces/rreichert/reichert-platform-hub/settings |

### Option A — **Split** (recommended where app has native Supabase + cross-app)

| Action | Detail |
|--------|--------|
| Keep or set native secrets | `SUPABASE_URL` / `SUPABASE_ANON_KEY` (or `SOVEREIGN_*` on Sovereign desktop) for **app-local** tables. |
| Point platform secrets to Primary | `PLATFORM_SUPABASE_URL` = `https://wiwmphjkupcnntawpafg.supabase.co` |
| Keys for platform client | `PLATFORM_SUPABASE_ANON_KEY` = Primary **anon** (Hub-style reads OK). If REST **insert** to `cross_app_findings` uses **service_role**, add **`PLATFORM_SUPABASE_SERVICE_ROLE_KEY`** or use existing `SUPABASE_SERVICE_ROLE_KEY` only if code path reads it (see `supabase_platform.py`). |
| Pros | Minimal risk to native app DB; aligns with `T3` RLS (service_role insert). |
| Cons | Two URL/key pairs to manage per Space; must not swap accidentally. |

### Option B — **Single URL** (native only)

| Action | Detail |
|--------|--------|
| Set single `SUPABASE_URL` to Primary | Everything (native + findings) hits one project. |
| Pros | One secret pair. |
| Cons | **High risk** unless native schema already lives on Primary; Sovereign OPA data would be wrong project. **Not recommended** for SovereignShield without explicit migration. |

### Order of operations

1. **Sub-apps first** (table + RLS live on Primary after T3 apply).  
2. **Platform Hub last** — avoids Hub showing empty KPIs while writers still point at Sovereign.  
3. Expect **~60–120 s** Space rebuild per secret save.

---

## 5. Risk notes

| Risk | Mitigation |
|------|------------|
| Hot rotation triggers HF rebuild | Schedule during low traffic; verify health URL after each Space. |
| Hub before writers | Hub first → transient empty KPIs on Primary; prefer **writers → Hub**. |
| `anon` vs `service_role` on `cross_app_findings` | Per staged T3: **insert/update** expect **service_role**; anon Hub reads **view** only. Sub-apps using **anon** for inserts may fail until policy or key updated. |
| Sovereign desktop naming | Missing `SUPABASE_URL` in secret list — confirm Docker/HF env still exposes what `create_client` expects. |
| API 401/403 | Re-audit with token scopes **Read** + **Manage repository settings** for each Space org; this run had **no HTTP errors**. |

---

## 6. Raw audit artifact

Ephemeral helper file `_audit_raw.json` (if present) was used only for drafting and **should be deleted** before commit; the canonical operator artifact is **this** `T4_SECRET_AUDIT.md`.
