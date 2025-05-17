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
│   │   ├── repo_layout.md
│   │   ├── devcontainer.md
│   │   └── modular_plan.md
│   ├── processes/
│   ├── governance/
│   ├── logbook/
│   └── decisions/
├── evidence/                # Log e output generati da strumenti (es. report di linting, test)
│   └── logs/
├── infra/                   # Infrastruttura come codice (es. Docker Compose files)
│   └── docker-compose.redis.yml
├── scripts/                 # Script di utilità per lo sviluppo o la CI
│   └── test_builder_upload.py
├── secrets/                 # File di secret (es. client_secret.json, token.json - **NON COMMETTERE**)
├── services/                # Moduli per l'integrazione con API esterne o logiche di servizio core
│   ├── google_calendar/     # Modulo specifico per Google Calendar (potrebbe essere refactored)
│   ├── uploader/            # Servizio di upload file (STL/OBJ)
│   │   ├── storage.py
│   │   ├── uploader_service.py
│   │   └── validator.py
│   ├── webhook/             # Servizio Webhook PoC
│   │   ├── router.py
│   │   └── handler.py
│   └── redis/               # Client e utilità Redis
│       └── redis_client.py
├── tests/                   # Test unitari e di integrazione (pytest)
│   └── uploader/
│       └── test_uploader.py
├── utils/                   # Utilità trasversali (es. decoratori, helpers)
│   └── ratelimit.py
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
- **`scripts/`**: Script ausiliari che automatizzano compiti ripetitivi o supportano processi di sviluppo/CI (es. generazione dati di test, build specifiche, test manuali di endpoint).
- **`secrets/`**: Destinata a contenere file sensibili come chiavi API o credenziali OAuth. **Questa cartella DEVE essere presente nel `.gitignore`** per evitare il commit di dati sensibili.
- **`services/`**: Moduli Python che incapsulano la logica di interazione con servizi esterni, API di terze parti, o logiche di business core del progetto (es. upload, webhook, client Redis).
- **`tests/`**: Contiene tutti i test del progetto, tipicamente organizzati in una struttura che rispecchia quella del codice sorgente. Utilizza `pytest` come framework di testing.
- **`utils/`**: Contiene moduli Python con funzioni di utilità generale, decoratori, o classi helper che possono essere riutilizzate in diverse parti del progetto.

L'utilizzo di `poetry` per la gestione delle dipendenze e del packaging è centrale, con `pyproject.toml` e `poetry.lock` che definiscono e bloccano le dipendenze del progetto.

## Struttura del Repository

La struttura del repository è organizzata secondo un approccio modulare che favorisce la separazione delle responsabilità, la manutenibilità e la testabilità.

### Directory Principali

- **`config/`**: Contiene le configurazioni centralizzate dell'applicazione, incluse le impostazioni per upload, rate limiting e autenticazione.

- **`services/`**: Implementa la logica di business dell'applicazione, suddivisa in moduli funzionali:
  - `services/uploader/`: Servizio per l'upload di file 3D
  - `services/google_calendar/`: Integrazione con Google Calendar
  - `services/redis/`: Client e funzionalità Redis
  - `services/webhook/`: Gestione delle notifiche webhook

- **`routers/`**: Definisce gli endpoint FastAPI e le rotte dell'applicazione.

- **`utils/`**: Funzioni e strumenti di utilità riutilizzabili in tutto il progetto:
  - `utils/ratelimit.py`: Implementazione del rate limiting

- **`tests/`**: Test unitari e di integrazione, organizzati per rispecchiare la struttura del progetto.

- **`docs/`**: Documentazione del progetto, organizzata per argomento.

- **`evidence/`**: Contiene log, risultati dei test e artefatti di build per la tracciabilità e la riproducibilità:
  - `evidence/build/`: Log e artefatti delle build
  - `evidence/tests/`: Risultati e report dei test
  - `evidence/logs/`: Log di esecuzione

### Directory di Supporto

- **`.github/workflows/`**: Pipeline CI/CD per automazione di test, build e deploy.
- **`.devcontainer/`**: Configurazione del dev container per ambiente di sviluppo consistente.
- **`.config/`**: Configurazioni specifiche per l'ambiente di sviluppo.

### File Chiave

- **`pyproject.toml`**: Definizione del pacchetto Python, dipendenze e configurazione degli strumenti di sviluppo (Poetry).
- **`main.py`**: Punto di ingresso dell'applicazione FastAPI.
- **`.pre-commit-config.yaml`**: Configurazione hook pre-commit per garantire qualità del codice.
- **`.spectral.yaml`**: Regole di linting per OpenAPI 3.1.

### Organizzazione dei Test

I test seguono una struttura speculare al codice sorgente, facilitando l'associazione tra test e implementazione:

```
tests/
├── integration/  # Test di integrazione end-to-end
├── uploader/     # Test del modulo uploader
└── utils/        # Test delle utility
    └── test_ratelimit.py  # Test per utils/ratelimit.py
```
