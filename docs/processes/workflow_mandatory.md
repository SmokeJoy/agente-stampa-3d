# Flusso di Lavoro Obbligatorio – AGENTE STAMPA 3D DEV AI

Questo documento definisce il flusso di lavoro operativo che il Dev AI deve seguire scrupolosamente per ogni ciclo di sviluppo nel progetto "AGENTE STAMPA 3D". Questo flusso è estratto dall'Articolo 9 delle "Linee Guida Operative e Regolamento d'Eccellenza".

---

🚨 **FLUSSO DI LAVORO OBBLIGATORIO – AGENTE STAMPA 3D DEV AI** 🚨

📦 **INIZIO CICLO DI LAVORO**
    │
    ▼
📩 **1. Ricezione Ordine di Lavoro dal Teach Lead (Supervisore AI)**
    │   (Deve essere associato a una Roadmap Ufficiale in `docs/roadmap/`)
    │   (Se Roadmap mancante, vedi Articolo 8.3 del Regolamento: richiedi Roadmap prima di procedere)
    │
    │   *Esempio Pratico:*
    │   Il Teach Lead assegna un task come: "Implementare l'endpoint `/searchJobs` secondo lo schema `openapi_3_1_demo.json`, assicurando la validazione dei parametri `keyword` e `location`."
    │   Il Dev AI verifica che questo task sia collegato a una roadmap attiva (es. `ROADMAP_v2.md`, Fase di Sviluppo API).
    ▼
📁 **2. Controllo Preliminare e Immersione Documentale da Fuoriclasse:**
    │   → **Lettura obbligatoria e analisi critica** dei documenti rilevanti per il task in `docs/`, guidato da `docs/0_INDEX.md`.
    │     *Focus specifico su: Roadmap attiva, Logbook (voci precedenti relative a task simili o dipendenti), Toolset (es. `governance/spectral_rules.md` se si modifica l'API), Regole Dev AI (incluso Articolo 12 sulla Modularità), Architettura Progetto (`structure/repo_layout.md`).*
    │
    │   *Esempio Pratico:*
    │   Per l'endpoint `/searchJobs`, il Dev AI consulta:
    │   - La specifica `openapi_3_1_demo.json` per capire i requisiti.
    │   - `docs/governance/spectral_rules.md` per le regole di linting OpenAPI.
    │   - `docs/logbook/logbook_unificato_dev_ai.md` per vedere se ci sono state implementazioni simili o problemi riscontrati.
    │   - Articolo 12 sulla modularità per progettare il codice in modo granulare.
    ▼
📗 **3. Conferma Interna di Piena Comprensione Documentale.**
    │   (Il Dev AI si assicura di aver compreso tutti gli aspetti del task e come si inserisce nel progetto esistente).
    ▼
🔍 **4. Analisi Strategica del Task (Considerando la Modularità):**
    │   → Definire *cosa* (quali file modificare/creare, quali funzioni implementare) e *come* (algoritmi, strutture dati), in coerenza con: Architettura, Sicurezza, **Modularità (Articolo 12)**, Specifiche API.
    │
    │   *Esempio Pratico:*
    │   Per `/searchJobs`, il Dev AI pianifica:
    │   - Creazione/modifica di un modulo Python in `services/jobs_service.py`.
    │   - Definizione di modelli Pydantic per request/response.
    │   - Implementazione della logica di ricerca, possibilmente suddividendola in funzioni più piccole per la validazione dei parametri, l'interrogazione di un (ipotetico) database, e la formattazione della risposta.
    ▼
🧰 **5. Sviluppo / Refactoring del Codice con Maestria (e Modularità):**
    │   → Implementare o modificare, **applicando attivamente il principio di granularità (Articolo 12)**. Fare riferimento costante alla documentazione.
    │   → Rispettare type hinting, logging, commenti significativi, sicurezza (es. validazione input). Scrivere/aggiornare test (Articolo 5).
    │
    │   *Esempio Pratico:*
    │   Il Dev AI scrive il codice per `/searchJobs` in FastAPI, aggiunge type hints, log per il debugging, e crea test unitari in `tests/test_jobs_service.py` che coprano vari scenari (keyword presente/assente, location valida/non valida, ecc.).
    ▼
🤔 **6. Gestione Dubbi Operativi con Protocollo (Articolo 4 del Regolamento):**
    │   → **PRIMO:** Rileggere tutta la documentazione rilevante (come al punto 2).
    │   → **SECONDO (SOLO SE NECESSARIO):** Sospendere l'attività, formulare domanda chiara e dettagliata al Teach Lead (Supervisore AI), indicando i documenti già consultati e il punto esatto di incertezza.
    ▼
📝 **7. Documentazione Post-Sviluppo Impeccabile (Articolo 11 del Regolamento):**
    │   → **Aggiornare immediatamente** `docs/logbook/logbook_unificato_dev_ai.md` con:
    │     - Data e ora ISO-8601.
    │     - ID del task/riferimento Roadmap.
    │     - Descrizione del lavoro svolto.
    │     - Elenco file modificati/creati.
    │     - Motivazioni delle scelte chiave (se non ovvie).
    │     - Esito dei test.
    │   → **Aggiornare** `docs/0_INDEX.md` se sono stati aggiunti nuovi documenti principali o sezioni.
    │   → Aggiornare documentazione specifica di moduli, schemi API, toolset (es. se `/searchJobs` è un nuovo tool, documentarlo in un ipotetico `docs/toolset/api_endpoints.md`).
    │   → Aggiornare stato task sulla Roadmap (`docs/roadmap/ROADMAP_v2.md` - spuntare la checkbox o aggiornare lo stato).
    │
    │   *Esempio Pratico:*
    │   Completato `/searchJobs`, il Dev AI aggiorna il logbook, descrive le modifiche, elenca i file toccati, conferma test OK. Se è stato creato un nuovo file di documentazione per l'endpoint, lo aggiunge all'indice.
    ▼
✅ **8. Esecuzione e Validazione Test Rigorosa.**
    │   (Eseguire tutti i test pertinenti – unit, integration – e assicurarsi che passino. Es. `pytest -v -s`).
    ▼
📨 **9. Report Formale di Completamento Task al Teach Lead (Supervisore AI):**
    │   → Inviare report con: task ID, descrizione lavoro (evidenziando l'approccio modulare se rilevante), link ai file modificati (se su VCS), conferma test OK (es. allegando output di pytest o screenshot), riferimenti alla documentazione aggiornata (link a logbook, indice, ecc.).
    │   → Attendere validazione e/o nuovo ordine di lavoro.
    ▼
🔁 **10. Ritorno a Fase 1 (Pronto per Nuove Sfide d'Eccellenza).**

---

Questo flusso garantisce tracciabilità, qualità e allineamento con gli obiettivi del progetto e le aspettative del Teach Lead.
