# Roadmap per lo Sviluppo del GPT "Assistente Lavori Stampa 3D"
<!-- markdownlint-disable MD013 -->

Questa roadmap guida lo sviluppo del GPT personalizzato,
concentrandosi sull'integrazione per la ricerca di lavori nel settore stampa 3D
e la sincronizzazione del calendario, con un focus sull'utilizzo di OpenAPI 3.1.0.

## Roadmap v2 – conforme ai checkpoint G2‑G10

| Checkpoint | Deadline (dal T0) | Macro‑obiettivo                                  | Deliverable chiave                                           |
|------------|------------------|--------------------------------------------------|--------------------------------------------------------------|
| **G2**     | 24h              | Dev‑container, CI, settings, refactor auth       | Dockerfile, devcontainer.json, .spectral.yaml stub,          |
|            |                  |                                                  | tests verdi                                                  |
| **G4**     | 96h              | Schema demo 3.1 + Spectral 0‑err ≤2‑warn         | openapi_3_1_demo.json, spectral_lint_final.log,              |
|            |                  |                                                  | mif_jsonschema_dialect.json                                  |
| **G6**     | 144h             | Script upload Builder + PoC webhook, rate‑limit, | test_builder_upload.py, webhook_push_test.log,               |
|            |                  | Redis stato                                      | rate_limit_poc.log, multiturn_redis_test.log                 |
| **G8**     | 192h             | OAuth debugging profondo + migrazione 3.0→3.1 +  | oauth_flow_draft.mmd, migration.diff,                        |
|            |                  | hosting benchmark                                | api_hosting_benchmark.csv                                    |
| **G10**    | 240h             | Report finale & compatibility_matrix             | report.pdf, compatibility_matrix.csv, tutti MiF,             |
|            |                  |                                                  | checklist firmata                                            |
<!-- markdownlint-enable MD013 -->
