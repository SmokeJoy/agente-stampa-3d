## Logbook Unificato Dev AI

### 2023-10-27T10:00:00Z - Inizio Progetto AGENTE STAMPA 3D
- Creata directory `docs/`.
- Creato file `logbook.md` per tracciare le attività.

### 2023-10-27T10:15:00Z - Setup ambiente di sviluppo (Fase 1, Task 1)
- Installate librerie `fastapi` e `uvicorn`.
- Creato file `main.py` con struttura FastAPI di base.
- Struttura progetto iniziale stabilita.

### 2023-10-27T11:00:00Z - Allineamento Roadmap e Struttura G2 (Inizio)
- Ricevute direttive da Andrea per allineamento a checkpoint G2-G10.
- Aggiornato `ROADMAP.md` con la v2 fornita.
- Rimosse sezioni obsolete e citazioni `[cite:...]` da `ROADMAP.md`.
- Verificati `docs/logbook.md` e `docs/decisions.md` per citazioni (nessuna trovata).

### 2023-10-27T11:15:00Z - Creazione Struttura Directory G2
- Create directory: `config`, `services`, `services/google_calendar`, `secrets`, `tests`, `.devcontainer`, `scripts`.
- Aggiornato `.gitignore` per includere `secrets/` e `*.json`.

### 2023-10-27T11:30:00Z - Configurazione Settings e Refactor Auth G2
- Creato `config/settings.py` con Pydantic `BaseSettings` per la gestione delle configurazioni (path file Google, porta OAuth).
- Refactorizzato codice di autenticazione da `authenticate_google.py` a `services/google_calendar/auth_flow.py`:
    - Integrato con `config.settings`.
    - Implementato logging standard.
    - Migliorata gestione errori (no `sys.exit`).
    - Assicurata conversione `Path` a `str` per chiamate di libreria.
    - Aggiunto salvataggio token dopo refresh.
- Eliminato il vecchio file `authenticate_google.py`.

### 2023-10-27T11:45:00Z - Setup Dev Container e Spectral G2
- Creato `.devcontainer/Dockerfile` con base `python:3.12-slim`, Node 20, Spectral CLI, Redocly CLI.
- Creato `.devcontainer/devcontainer.json` con configurazioni per VS Code, estensioni e `postCreateCommand` per installare dipendenze e pre-commit.
- Creato file stub `.spectral.yaml` (da popolare in G4).

### 2023-10-27T12:00:00Z - Configurazione CI Workflow (GitHub Actions) G2
- Create directory `.github/workflows/`.
- Creato `.github/workflows/ci.yml` con:
    - Trigger su push/pull_request a `main`/`develop`.
    - Job `lint-and-test` (utilizzando `devcontainers/ci@v0`):
        - Checkout codice.
        - Installazione `requirements.txt`.
        - Esecuzione `pre-commit run --all-files`.
        - Placeholder per `pytest`.
    - Job `gpg-signature-check` per verificare firme GPG dei commit.

### 2023-10-27T12:15:00Z - Implementazione Test Baseline G2
- Creato `tests/test_auth_flow.py` con test Pytest per `load_credentials`:
    - Fixture `mock_settings` per mockare percorsi file.
    - Test per flusso nuovo token.
    - Test per caricamento token valido esistente.
    - Test per refresh token scaduto (successo).
    - TODO per casi di fallimento e `client_secret.json` non trovato.

### 2023-10-27T12:30:00Z - Script Ausiliari e Conclusione Setup Iniziale G2
- Creato `scripts/generate_fake_secret.py` per generare `client_secret.json` fittizio per la CI.
- Tentativo di creare `.env.example` fallito a causa di restrizioni di sicurezza (azione posticipata/manuale).

### 2023-10-27T13:00:00Z - Finalizzazione G2: Migrazione a Poetry e Direttive Tech Lead
- Ricevute direttive finali dal Tech Lead per chiusura G2.
- **Migrazione a Poetry**: Creato `pyproject.toml` con dipendenze pin-nate come da specifiche (fastapi 0.110.2, uvicorn 0.29.0, pydantic 2.7.1, google libs, etc.). Rimosso `requirements.txt`.
- Modificato `config/settings.py` per importare `BaseSettings` da `pydantic` (invece di `pydantic_settings`) e aggiunto `extra='ignore'`.
- **Dev Container (`.devcontainer/Dockerfile`)**: Aggiornato con versioni specifiche per Node.js (20.14.0), `build-essential`, `git`, Redocly CLI (1.13.1), e Spectral CLI (7.0.0).
- **Dev Container (`.devcontainer/devcontainer.json`)**: Aggiornato `postCreateCommand` per usare `poetry install --no-interaction --no-root && pre-commit install --install-hooks`.
- **Pre-commit (`.pre-commit-config.yaml`)**: Sostituito contenuto con la nuova configurazione degli hook fornita (black 24.4.2, isort 5.13.2, flake8 7.0.0, etc.).
- **CI Workflow (`.github/workflows/ci.yml`)**: Aggiornato job `lint-and-test` per usare `poetry install` e `pytest -q`. Aggiornato job `gpg-signature-check` per usare `docancodes/action-verify-gpg@v1`.
- **README.md**: Aggiornato per riflettere l'uso di Poetry.

### 2023-10-27T14:00:00Z - Completamento Checkpoint G2
- Eseguite direttive finali del Tech Lead per G2.
- Creato placeholder per `poetry.lock`; il file reale verrà generato da `poetry lock --no-update` e verificato.
- Analisi pre-push dei file per conformità a `pre-commit` (black, isort, flake8, etc.) completata con esito positivo atteso.
- Creato file `Repo Dev AI.txt` con placeholder per SHA commit e URL run CI.
- Il sistema è ora pronto per il commit GPG-signed, push e validazione della pipeline CI.
- Link alla run CI (da inserire dopo l'esecuzione): <CI_RUN_URL_PLACEHOLDER_PENDING_ACTUAL_RUN> 