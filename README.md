# Agente Stampa 3D API

<!-- markdownlint-disable-next-line MD013 MD034 -->
[![CI Pipeline](https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>/actions/workflows/ci.yml/badge.svg)](https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>/actions/workflows/ci.yml) <!-- Sostituisci con il tuo username e repository -->
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](<https://github.com/pre-commit/pre-commit>)

API backend per il GPT "Assistente Lavori Stampa 3D", progettata per cercare opportunità di lavoro nel
settore della stampa 3D e gestire l'agenda dell'utente.

## Quick Start (con Dev Container)

Questo progetto è configurato per utilizzare [Dev Containers](https://code.visualstudio.com/docs/remote/containers)
in VS Code, che fornisce un ambiente di sviluppo Dockerizzato, preconfigurato e consistente.

1. **Prerequisiti:**
   - [Docker Desktop](https://www.docker.com/products/docker-desktop) installato e in esecuzione.
   - [Visual Studio Code](https://code.visualstudio.com/) installato.
   - L'estensione [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
     installata in VS Code.

2. **Clona il repository:**

   ```bash
   git clone https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>.git # Sostituisci!
   cd <YOUR_REPOSITORY>
   ```

3. **Apri in Dev Container:**
   - Apri la cartella del progetto in VS Code.
   - VS Code dovrebbe rilevare automaticamente la configurazione del Dev Container
     (`.devcontainer/devcontainer.json`) e chiederti se vuoi "Riaprire nel container"
     ("Reopen in Container"). Fai clic su quel pulsante.
   - In alternativa, apri la Command Palette (Ctrl+Shift+P o Cmd+Shift+P) e cerca
     "Dev Containers: Reopen in Container".
   - La prima volta, la build dell'immagine Docker potrebbe richiedere alcuni minuti.

4. **Setup Iniziale (all'interno del Dev Container):**
   - Il comando `postCreateCommand` in `devcontainer.json` dovrebbe aver già installato le dipendenze
     usando Poetry e gli hook di `pre-commit`.
   - **Configura le credenziali Google API:**
     - Segui le istruzioni in `docs/SETUP_GOOGLE_API.md` per ottenere il tuo file
       `client_secret.json` da Google Cloud Console.
     - Salva questo file come `secrets/client_secret.json` (la directory `secrets/` è già
       nel `.gitignore`).
     - Esegui il flusso di autenticazione una volta per generare `secrets/token.json`. Puoi farlo
       eseguendo uno script di test o una piccola utility che chiami `load_credentials`
       (da creare se necessario, o tramite i test interattivi se possibile).

5. **Esegui l'applicazione (esempio con Uvicorn):**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   L'API sarà accessibile su `http://localhost:8000`.

6. **Esegui i test:**

   ```bash
   pytest
   ```

7. **Esegui pre-commit hooks manualmente (opzionale):**

   ```bash
   pre-commit run --all-files
   ```

## Struttura del Progetto (Principale)

```text
agente-stampa-3D/
├── .devcontainer/        # Configurazione Dev Container (Dockerfile, devcontainer.json)
├── .github/              # Workflow GitHub Actions (CI)
├── .vscode/              # Impostazioni VS Code (opzionale, es. per launch.json)
├── config/               # Moduli di configurazione (es. settings.py con Pydantic)
├── docs/                 # Documentazione (Roadmap, Logbook, Setup API, etc.)
├── scripts/              # Script di utilità (es. generate_fake_secret.py)
├── secrets/              # File sensibili (ignorati da Git, es. client_secret.json, token.json)
├── services/             # Logica di business e interazione con API esterne
│   └── google_calendar/  # Modulo specifico per Google Calendar
├── tests/                # Test automatici (Pytest)
├── .gitignore            # File e directory da ignorare in Git
├── .pre-commit-config.yaml # Configurazione per Pre-commit
├── .spectral.yaml        # Configurazione Spectral (linter OpenAPI)
├── main.py               # Entry point dell'applicazione FastAPI
├── pyproject.toml        # Dipendenze Python e configurazione del progetto (Poetry)
├── poetry.lock           # File di lock delle dipendenze Poetry
├── ROADMAP.md            # Roadmap del progetto
└── README.md             # Questo file
```

## Roadmap

Consulta il file [ROADMAP.md](ROADMAP.md) per i dettagli sui checkpoint e le scadenze del progetto.

## Contribuire

Assicurati di:

- Firmare i tuoi commit con GPG.
- Seguire le convenzioni di stile del codice (controllate da `pre-commit`).
- Scrivere test per nuove funzionalità o bug fix.
- Mantenere aggiornata la documentazione.

---
*Questa è una bozza iniziale del README e verrà ulteriormente migliorata.*
