# Phase 5 Seed — Post-Phase 4

## Objectives

1. **PyPI publish** — starguard-core as installable package
2. **Customer DB tier resolution** — resolve FREE/PRO/ENTERPRISE from customer database
3. **Real plan data ingestion** — replace synthetic scenarios with real plan data
4. **Lead pipeline activation** — capture_lead(), email sequences
5. **First paying client** — onboarding, API keys, usage tracking

---

## Architecture Decisions (Hold)

- starguard-core module boundaries (RADV, HCC, HEDIS, Stars)
- _FEATURE_TIERS pattern
- run_command_center() compound narrative
- Four-repo layout (starguard-core, auditshield, starguard-desktop, starguard-mobile)

---

## Authorized to Change in Phase 5

- Tier resolution logic (database lookup vs. API key pattern)
- Synthetic → real data pipelines
- PyPI package metadata, versioning
- Lead capture implementation (currently no-op)
- Customer onboarding flows

---

## Dependencies

- Phase 4 close gate passes
- All three Spaces deploy automatically (HF_TOKEN configured)
- .cursorrules v3 in place for handoff
