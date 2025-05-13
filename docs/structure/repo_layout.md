# Struttura del Repository AGENTE STAMPA 3D

Questo documento descrive la struttura delle directory principali del progetto "AGENTE STAMPA 3D" e lo scopo di ciascuna cartella chiave.

## Diagramma della Struttura (Root)

```text
agente-stampa-3D/
├── .config/                 # Configurazioni specifiche per strumenti (es. Spectral personalizzato)
├── .devcontainer/           # Configurazione del Dev Container (Dockerfile, devcontainer.json, script)
├── .github/                 # Workflow per GitHub Actions (CI/CD)
│   └── workflows/
├── .idea/                   # (Opzionale, generato da IDE JetBrains, di solito in .gitignore)
├── config/                  # Moduli di configurazione dell'applicazione (es. settings Pydantic)
├── docs/                    # Tutta la documentazione del progetto (questo indice, roadmap, log, decisioni, ecc.)
│   ├── 0_INDEX.md
│   ├── roadmap/
│   ├── structure/
│   ├── processes/
│   ├── governance/
│   ├── logbook/
│   └── decisions/
├── evidence/                # Log e output generati da strumenti (es. report di linting, test)
│   └── logs/
├── scripts/                 # Script di utilità per lo sviluppo o la CI
├── secrets/                 # File di secret (es. client_secret.json, token.json - **NON COMMETTERE**)
├── services/                # Moduli per l'integrazione con API esterne (es. Google Calendar)
│   └── google_calendar/
├── tests/                   # Test unitari e di integrazione (pytest)
├── venv/                    # Ambiente virtuale Python (di solito in .gitignore)
├── .gitignore               # Specifica i file e le directory da ignorare per Git
├── .pre-commit-config.yaml  # Configurazione degli hook di pre-commit
├── .spectral.yaml           # Configurazione di base di Spectral (se non si usa quella in .config/)
├── DIARIO_PERSONALE.md      # (File specifico dell'utente, non standard del progetto)
├── main.py                  # Entry point principale dell'applicazione FastAPI (o script principale)
├── openapi_3_1_demo.json    # Specifica OpenAPI 3.1.0 di esempio/test
├── poetry.lock              # File di lock delle dipendenze di Poetry
├── pyproject.toml           # File di configurazione del progetto Python (Poetry)
├── README.md                # README principale del progetto
├── ROADMAP.md               # Roadmap generale del progetto (la versione ufficiale è in docs/roadmap)
└── Repo Dev AI.txt          # (File specifico dell'utente, non standard del progetto)
```

## Spiegazione delle Cartelle Chiave

- **`.config/`**: Contiene file di configurazione specifici per strumenti che richiedono una posizione dedicata, come configurazioni avanzate o personalizzate di Spectral.
- **`.devcontainer/`**: Essenziale per lo sviluppo standardizzato. Contiene il `Dockerfile` per costruire l'immagine del container di sviluppo, `devcontainer.json` per la configurazione dell'ambiente in VS Code, e script di supporto come `run_in_container.sh`.
- **`.github/workflows/`**: Definisce i flussi di lavoro per l'Integrazione Continua (CI) e il Deployment Continuo (CD) utilizzando GitHub Actions. Include linting, testing, building, ecc.
- **`config/`**: Contiene la logica di configurazione dell'applicazione, tipicamente attraverso Pydantic Settings, per gestire variabili d'ambiente e parametri di configurazione.
- **`docs/`**: Il cuore della documentazione del progetto. Organizzata in sottodirectory tematiche per facilitare la navigazione e la comprensione.
- **`evidence/`**: Raccoglie prove tangibili dell'esecuzione di processi, come i log generati da Spectral o da altri strumenti di linting e testing.
- **`scripts/`**: Script ausiliari che automatizzano compiti ripetitivi o supportano processi di sviluppo/CI (es. generazione dati di test, build specifiche).
- **`secrets/`**: Destinata a contenere file sensibili come chiavi API o credenziali OAuth. **Questa cartella DEVE essere presente nel `.gitignore`** per evitare il commit di dati sensibili.
- **`services/`**: Moduli Python che incapsulano la logica di interazione con servizi esterni o API di terze parti (es. API di Google Calendar, API per la ricerca di lavori).
- **`tests/`**: Contiene tutti i test del progetto, tipicamente organizzati in una struttura che rispecchia quella del codice sorgente. Utilizza `pytest` come framework di testing.

L'utilizzo di `poetry` per la gestione delle dipendenze e del packaging è centrale, con `pyproject.toml` e `poetry.lock` che definiscono e bloccano le dipendenze del progetto.
