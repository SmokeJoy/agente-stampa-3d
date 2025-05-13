## Decisioni Architetturali e Tecniche

Qui verranno documentate le decisioni significative prese durante lo sviluppo del progetto, con la motivazione alla base di ciascuna scelta. 

### 2023-10-27: Finalizzazione G2 e Migrazione a Poetry

- **Gestione Dipendenze**: Migrazione da `requirements.txt` a `pyproject.toml` con Poetry come gestore di dipendenze e packaging. Questa scelta è stata fatta per una gestione più robusta, risoluzione delle dipendenze migliorata, e per allinearsi alle best practice moderne dei progetti Python. Le dipendenze sono state pin-nate a versioni specifiche come da direttive del Tech Lead.
- **Configurazione Pydantic**: Modificato l'import di `BaseSettings` in `config/settings.py` per utilizzare `pydantic.BaseSettings` (Pydantic v2) invece di `pydantic_settings`, semplificando le dipendenze dirette.
- **Ambiente di Sviluppo (Dev Container)**: Raffinata la configurazione del Dockerfile e del `devcontainer.json` per includere versioni specifiche di Node.js, Spectral, Redocly, e per utilizzare Poetry nell'installazione delle dipendenze e nella configurazione di pre-commit.
- **CI Workflow**: Ottimizzato il workflow GitHub Actions (`ci.yml`) per utilizzare Poetry per l'installazione delle dipendenze e una action dedicata (`docancodes/action-verify-gpg@v1`) per un controllo più affidabile delle firme GPG.
- **Pre-commit Hooks**: Aggiornata la configurazione di `pre-commit` con URL dei repository e revisioni degli hook specificate dal Tech Lead per garantire coerenza e standard di linting/formatting.

### 2023-10-27: Struttura Iniziale e Allineamento G2

- **Roadmap**: Adottata la Roadmap v2 fornita da Andrea, focalizzata sui checkpoint G2-G10, per allineare le tempistiche e i deliverable del progetto. La precedente roadmap basata su fasi temporali più lunghe è stata scartata.
- **Modularità del Codice**: Adottato un approccio modulare fin dall'inizio, come da direttive. Il codice di autenticazione Google è stato isolato in `services/google_calendar/auth_flow.py` e la configurazione centralizzata in `config/settings.py`.
- **Gestione Secrets**: Implementata gestione dei secret tramite file `client_secret.json` e `token.json` nella directory `secrets/` (ignorata da Git). Le Pydantic settings (`config/settings.py`) gestiscono i path a questi file. Creato script `scripts/generate_fake_secret.py` per la CI.
- **Dev Container**: Adottato un approccio basato su Dev Container (`.devcontainer/Dockerfile` e `.devcontainer/devcontainer.json`) per standardizzare l'ambiente di sviluppo e includere strumenti come Python 3.12, Node 20, Spectral e Redocly CLI.
- **CI/CD (GitHub Actions)**: Impostato un workflow CI base (`.github/workflows/ci.yml`) che include linting tramite pre-commit (all'interno del dev container) e un controllo della firma GPG. Placeholder per i test Pytest.
- **Linting e Formatting**: Configurati `pre-commit` con `isort`, `black --check`, `flake8`, `end-of-file-fixer`, `check-yaml`, `detect-secrets` per mantenere la qualità del codice.
- **Testing**: Introdotti test unitari con Pytest per il modulo di autenticazione (`tests/test_auth_flow.py`), utilizzando mock per isolare le dipendenze esterne e i file system.

### 2023-10-27: Checkpoint G2 Completato

- **Conferma Migrazione a Poetry**: La migrazione a Poetry è stata finalizzata e tutti i file di configurazione (pyproject.toml, Dockerfile, devcontainer.json, CI workflow) sono stati allineati per utilizzare Poetry come unico gestore delle dipendenze. Questo include il pinning esatto delle versioni come da specifiche.
- **Validazione Strumenti CI/CD**: La configurazione per pre-commit, linting, formatting, test e GPG signature check è stata completata e verificata (a livello di configurazione). L'effettiva esecuzione e il passaggio "verde" della pipeline CI sono il prossimo passo di validazione dopo il push.
- **Struttura Progetto Stabile per G2**: Tutti i deliverable richiesti per il checkpoint G2 sono stati implementati. Il progetto ha una base solida per le fasi successive (G4 e oltre). 