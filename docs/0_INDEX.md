# Indice della Documentazione del Progetto "AGENTE STAMPA 3D"

Benvenuto nella documentazione ufficiale del progetto "AGENTE STAMPA 3D". Questo file funge da indice principale per navigare tra tutti i documenti rilevanti.

## Struttura della Documentazione

Ecco un elenco gerarchico dei documenti disponibili. Ogni voce è un link cliccabile al relativo file Markdown.

- **`docs/`**
  - [`0_INDEX.md`](./0_INDEX.md) (Questo file)
  - **`roadmap/`**
    - [`ROADMAP_v2.md`](./roadmap/ROADMAP_v2.md) - Roadmap ufficiale del progetto (Versione 2).
  - **`structure/`**
    - [`repo_layout.md`](./structure/repo_layout.md) - Descrizione della struttura delle directory del repository.
    - [`devcontainer.md`](./structure/devcontainer.md) - Dettagli sulla configurazione del Dev Container.
  - **`processes/`**
    - [`workflow_mandatory.md`](./processes/workflow_mandatory.md) - Flusso di lavoro obbligatorio per il Dev AI.
    - [`ci_pipeline.md`](./processes/ci_pipeline.md) - Descrizione della pipeline di Continuous Integration.
  - **`governance/`**
    - [`spectral_rules.md`](./governance/spectral_rules.md) - Regole Spectral per il linting delle OpenAPI.
    - [`redocly_setup.md`](./governance/redocly_setup.md) - Informazioni sull'utilizzo (potenziale) di Redocly CLI.
    - [`pre_commit.md`](./governance/pre_commit.md) - Configurazione e utilizzo degli hook di pre-commit e Regola GIT-AI-3.
  - **`logbook/`**
    - [`logbook_unificato_dev_ai.md`](./logbook/logbook_unificato_dev_ai.md) - Logbook cronologico delle attività di sviluppo.
  - **`decisions/`**
    - [`decisions.md`](./decisions/decisions.md) - Registro delle decisioni architetturali e tecniche chiave.

## 🔄 Stato Roadmap Principale (v2)

La tabella seguente mostra lo stato di avanzamento delle principali fasi e checkpoint definiti nella [`ROADMAP_v2.md`](./roadmap/ROADMAP_v2.md).

| Fase / Checkpoint                                   | Scadenza (da T0) | Stato       |
| --------------------------------------------------- | ---------------- | ----------- |
| **S-1 (Setup Iniziale Progetto)**                   | N/A              | ✅ Completata |
| **S-2 (Dev Container & Linting Setup)**             | (cfr. G2)        | ✅ Completata |
| **S-3 (Fix Spectral Warnings & Pre-commit)**        | (cfr. G4)        | ✅ Completata |
| **D-1 (Documentazione Iniziale Strutturata)**       | (T0 + 48h)       | ✅ Completata |
| **G4-MOD (Docs Struttura: Code Map & Modular Plan)**| (cfr. G4)        | ✅ *completato* |
| ---                                                 | ---              | ---         |
| **G2** (Dev‑container, CI, settings, refactor auth) | 24h              | ✅ Completato |
| **G4** (Schema demo 3.1 + Spectral 0‑err ≤2‑warn)   | 96h              | ⏳ In corso  |
| **G6** (Script upload Builder + PoC webhook, ecc.)  | 144h             | ❌ Pending  |
| **G8** (OAuth debugging, migrazione 3.0→3.1, ecc.) | 192h             | ❌ Pending  |
| **G10** (Report finale & compatibility_matrix)      | 240h             | ❌ Pending  |

**Legenda Stato:**

- ✅: Completato / Chiuso
- ⏳: In Corso / Aperto
- ❌: Pending / Non iniziato

---
*Questo indice deve essere mantenuto aggiornato con ogni nuova aggiunta o modifica significativa alla struttura della documentazione.*
