-- Platform Hub schema: optional agent_interactions.severity, platform_sessions,
-- cross_app_findings, platform_alerts, platform_hub_kpis view
-- Run in Supabase SQL Editor (paste without markdown fences)
--
-- If agent_interactions does not exist yet (e.g. fresh Sovereign project), skip
-- section 1: comment out the ALTER TABLE and CREATE INDEX below, then run the rest.

-- ── 1. Optional: severity on agent_interactions (skip entire block if table missing)
ALTER TABLE agent_interactions
  ADD COLUMN IF NOT EXISTS severity TEXT
    NOT NULL DEFAULT 'medium'
    CHECK (severity IN ('critical','high','medium','low'));

CREATE INDEX IF NOT EXISTS idx_ai_severity
  ON agent_interactions (severity);

-- ── 2. platform_sessions ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS platform_sessions (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    app_name    TEXT        NOT NULL
                    CHECK (app_name IN (
                        'auditshield','starguard',
                        'sovereignshield','platform_hub'
                    )),
    session_id  TEXT,
    org_id      TEXT,
    user_context JSONB DEFAULT '{}'::JSONB,
    metadata    JSONB DEFAULT '{}'::JSONB
);

CREATE INDEX IF NOT EXISTS idx_ps_app     ON platform_sessions (app_name);
CREATE INDEX IF NOT EXISTS idx_ps_created ON platform_sessions (created_at);

-- ── 3. cross_app_findings ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cross_app_findings (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_app      TEXT        NOT NULL
                        CHECK (source_app IN (
                            'auditshield','starguard','sovereignshield'
                        )),
    finding_type    TEXT        NOT NULL,
    severity        TEXT        NOT NULL DEFAULT 'medium'
                        CHECK (severity IN ('critical','high','medium','low')),
    status          TEXT        NOT NULL DEFAULT 'open'
                        CHECK (status IN (
                            'open','in_review','remediated','suppressed','closed'
                        )),
    title           TEXT        NOT NULL,
    description     TEXT,
    measure_id      TEXT,
    hcc_code        TEXT,
    policy_id       TEXT,
    implicated_apps TEXT[],
    audit_run_id    UUID,
    star_run_id     UUID,
    remediation_task_id UUID,
    session_id      UUID REFERENCES platform_sessions (id) ON DELETE SET NULL,
    payload         JSONB DEFAULT '{}'::JSONB
);

CREATE INDEX IF NOT EXISTS idx_caf_status   ON cross_app_findings (status);
CREATE INDEX IF NOT EXISTS idx_caf_source   ON cross_app_findings (source_app);
CREATE INDEX IF NOT EXISTS idx_caf_severity ON cross_app_findings (severity);
CREATE INDEX IF NOT EXISTS idx_caf_measure  ON cross_app_findings (measure_id);

-- ── 4. platform_alerts ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS platform_alerts (
    id                          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at                 TIMESTAMPTZ,
    alert_type                  TEXT        NOT NULL,
    severity                    TEXT        NOT NULL DEFAULT 'medium'
                                    CHECK (severity IN ('critical','high','medium','low')),
    status                      TEXT        NOT NULL DEFAULT 'active'
                                    CHECK (status IN ('active','acknowledged','resolved')),
    title                       TEXT        NOT NULL,
    message                     TEXT,
    trigger_app                 TEXT
                                    CHECK (trigger_app IN (
                                        'auditshield','starguard','sovereignshield'
                                    )),
    affected_apps               TEXT[],
    finding_id                  UUID REFERENCES cross_app_findings (id) ON DELETE CASCADE,
    auto_remediation_suggested  BOOLEAN DEFAULT FALSE,
    remediation_hint            TEXT,
    payload                     JSONB DEFAULT '{}'::JSONB
);

-- ── 5. platform_hub_kpis view ─────────────────────────────────────
CREATE OR REPLACE VIEW platform_hub_kpis AS
SELECT
    COUNT(*) FILTER (WHERE status = 'open')                                  AS open_findings_total,
    COUNT(*) FILTER (WHERE source_app = 'auditshield'     AND status = 'open') AS open_audit_flags,
    COUNT(*) FILTER (WHERE source_app = 'starguard'       AND status = 'open') AS open_star_gaps,
    COUNT(*) FILTER (WHERE source_app = 'sovereignshield' AND status = 'open') AS open_policy_violations,
    COUNT(*) FILTER (WHERE severity = 'critical'          AND status = 'open') AS critical_open,
    COUNT(*) FILTER (WHERE status = 'remediated')                              AS remediated_total
FROM cross_app_findings;

-- ── Verification (run separately after migration) ────────────────────
-- SELECT * FROM platform_hub_kpis;
-- SELECT column_name, data_type FROM information_schema.columns
--   WHERE table_name = 'agent_interactions' AND column_name = 'severity';
