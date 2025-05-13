# Roadmap per lo Sviluppo del GPT "Assistente Lavori Stampa 3D"

Questa roadmap guida lo sviluppo del GPT personalizzato, concentrandosi sull'integrazione per la ricerca di lavori nel settore stampa 3D e la sincronizzazione del calendario, con un focus sull'utilizzo di OpenAPI 3.1.0.

### Roadmap v2 – conforme ai checkpoint G2‑G10

| Checkpoint | Deadline (dal T0) | Macro‑obiettivo | Deliverable chiave |
|------------|------------------|-----------------|--------------------|
| **G2** | 24 h | Dev‑container, CI, settings, refactor auth | Dockerfile, devcontainer.json, .spectral.yaml stub, tests verdi |
| **G4** | 96 h | Schema demo 3.1 + Spectral 0‑err ≤2‑warn | openapi_3_1_demo.json, spectral_lint_final.log, mif_jsonschema_dialect.json |
| **G6** | 144 h | Script upload Builder + PoC webhook, rate‑limit, Redis stato | test_builder_upload.py, webhook_push_test.log, rate_limit_poc.log, multiturn_redis_test.log |
| **G8** | 192 h | OAuth debugging profondo + migrazione 3.0→3.1 + hosting benchmark | oauth_flow_draft.mmd, migration.diff, api_hosting_benchmark.csv |
| **G10** | 240 h | Report finale & compatibility_matrix | report.pdf, compatibility_matrix.csv, tutti MiF, checklist firmata |
