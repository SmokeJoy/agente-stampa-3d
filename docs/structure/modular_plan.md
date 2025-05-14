# Proposta di Piano di Modularizzazione del Codice

Questo documento descrive la struttura modulare futura proposta per il progetto "AGENTE STAMPA 3D", con l'obiettivo di garantire granularità, manutenibilità e scalabilità.

## Diagramma a Blocchi dei Moduli Futuri

```text
+-----------------------+      +-----------------------+      +-------------------------+
|      main.py          |----->|  api_client (HTTPX)   |<-----|   jobs_search_service   |
| (FastAPI Endpoints)   |      +-----------------------+      | (Logica ricerca lavori) |
+-----------------------+               ^                     +-------------------------+
           |                            |
           |                            |                     +---------------------------+
           |                            +---------------------| calendar_sync_service     |
           |                                                  | (Logica sinc. calendario) |
           |                                                  +---------------------------+
           |
           |                            +-----------------------+
           +--------------------------->|   core.config_manager |
                                        | (settings.py Pydantic)|        
                                        +-----------------------+

+-----------------------+
|  cli_orchestrator.py  | (Se necessario per tool CLI o gestione offline)
| (Click/Typer)         |
+-----------------------+

+-----------------------+
|      utils/           | (Moduli di utilità trasversali, es. logging_setup.py, error_handlers.py)
|      - helpers.py     |
|      - custom_types.py|
+-----------------------+

+-----------------------+
|      models/          | (Schemi Pydantic per request/response e dati interni)
|      - job_models.py  |
|      - calendar_models.py|
|      - common_models.py |
+-----------------------+
```

## Descrizione Macro-Aree e Interfacce Pubbliche

**1. `main.py` (o `app/main.py`)**
   - **Responsabilità:** Entry point dell'applicazione FastAPI. Definisce gli endpoint API esposti, gestisce le richieste HTTP in entrata e le risposte.
   - **Interfacce Pubbliche (esempi di endpoint FastAPI):**
     - `POST /search-jobs`: Avvia una ricerca di lavori.
       - Input: `JobSearchRequest` (Pydantic model: keywords, location, platforms, etc.)
       - Output: `JobSearchResponse` (Pydantic model: jobId, status)
     - `GET /job-status/{job_id}`: Controlla lo stato di una ricerca.
       - Output: `JobStatusResponse`
     - `POST /sync-calendar`: Sincronizza eventi con il calendario.
       - Input: `CalendarSyncRequest` (Pydantic model: events_to_sync, calendar_id)
       - Output: `CalendarSyncResponse`
     - `GET /authorize-google`: (Potrebbe reindirizzare o fornire URL per OAuth)
     - `GET /oauth2callback-google`: Callback per il flusso OAuth.

**2. `core/` (nuova directory)**
   - **`config_manager.py` (o `core/settings.py`)**
     - **Responsabilità:** Caricamento e validazione della configurazione dell'applicazione (API keys, percorsi, variabili d'ambiente) utilizzando Pydantic.
     - **Interfacce Pubbliche:**
       - `settings: Settings`: Istanza globale dell'oggetto `Settings` Pydantic.

**3. `services/`**
   - **`api_client.py` (o `shared/http_client.py`)**
     - **Responsabilità:** Wrapper generico per effettuare richieste HTTP (usando `httpx`) verso API esterne (piattaforme di lavoro, API Google, ecc.). Gestisce retries, timeout, error handling HTTP di base.
     - **Interfacce Pubbliche:**
       - `async def get(url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> httpx.Response:`
       - `async def post(url: str, data: Optional[dict] = None, json: Optional[dict] = None, headers: Optional[dict] = None) -> httpx.Response:`

   - **`jobs_search_service.py`**
     - **Responsabilità:** Logica di business per la ricerca di offerte di lavoro. Interagisce con diverse piattaforme di lavoro tramite `api_client`. Aggrega e normalizza i risultati.
     - **Interfacce Pubbliche:**
       - `async def initiate_search(search_params: models.job_models.JobSearchParams) -> str: # returns job_id`
       - `async def get_search_results(job_id: str) -> List[models.job_models.JobPosting]:`

   - **`calendar_sync_service.py`**
     - **Responsabilità:** Logica di business per la sincronizzazione con Google Calendar. Utilizza le credenziali gestite da `google_auth_service.py` e `api_client` per le chiamate API specifiche di Google Calendar.
     - **Interfacce Pubbliche:**
       - `async def sync_events_to_calendar(events: List[models.calendar_models.CalendarEvent], calendar_id: str = "primary") -> models.calendar_models.SyncReport:`
       - `async def get_upcoming_events(calendar_id: str = "primary", max_results: int = 10) -> List[models.calendar_models.CalendarEvent]:`

   - **`google_auth_service.py` (evoluzione di `services/google_calendar/auth_flow.py`)**
     - **Responsabilità:** Gestione completa del flusso di autenticazione e refresh dei token per le API Google.
     - **Interfacce Pubbliche:**
       - `async def get_credentials() -> Optional[google.oauth2.credentials.Credentials]:`
       - `def build_authorization_url() -> str:`
       - `async def process_oauth_callback(code: str) -> Optional[google.oauth2.credentials.Credentials]:`

**4. `models/` (nuova directory)**
   - **Responsabilità Generale:** Contiene tutti gli schemi Pydantic utilizzati per la validazione dei dati di richiesta/risposta API e per la strutturazione dei dati interni.
   - **`job_models.py`**:
     - Schemi: `JobSearchRequest`, `JobSearchResponse`, `JobStatusResponse`, `JobPosting`, `JobSearchParams`
   - **`calendar_models.py`**:
     - Schemi: `CalendarSyncRequest`, `CalendarSyncResponse`, `CalendarEvent`, `SyncReport`
   - **`common_models.py`**:
     - Schemi: `ErrorResponse`, `StatusMessage`

**5. `cli/` (nuova directory, se necessario)**
   - **`cli_orchestrator.py`**:
     - **Responsabilità:** Punto di ingresso per comandi CLI (usando `Typer` o `Click`). Orchestra chiamate ai vari servizi per operazioni da riga di comando.
     - **Interfacce Pubbliche (comandi CLI):**
       - `search-jobs (keywords, ...)`
       - `sync-calendar`

**6. `utils/` (nuova directory)**
   - **Responsabilità Generale:** Contiene moduli di utilità trasversali riutilizzabili in tutto il progetto.
   - **`logging_config.py`**: Configurazione centralizzata e setup del logging per l'applicazione.
   - **`error_handlers.py`**: Gestori di eccezioni FastAPI personalizzati e definizioni di errori comuni dell'applicazione.
   - **`helpers.py`**: Funzioni di utilità generiche (es. manipolazione date, stringhe, ecc.).

Questa struttura è una base di partenza e potrà evolvere con le necessità del progetto. L'obiettivo primario è mantenere ogni modulo focalizzato su una singola responsabilità e con interfacce ben definite. 
