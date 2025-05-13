# Pipeline di Continuous Integration (CI)

Questo documento descrive la pipeline di Continuous Integration (CI) per il progetto "AGENTE STAMPA 3D", come configurata (o pianificata) in `.github/workflows/ci.yml`.

## Obiettivi della CI

- **Qualità del Codice:** Assicurare che ogni modifica rispetti gli standard di codifica e linting.
- **Stabilità:** Verificare che le modifiche non introducano regressioni tramite l'esecuzione automatica dei test.
- **Automazione:** Automatizzare i controlli di routine per liberare tempo agli sviluppatori.
- **Tracciabilità:** Mantenere uno storico delle build e dei test per ogni commit.

## Trigger della Pipeline

La pipeline CI è tipicamente configurata per avviarsi automaticamente su:

- **Push** su branch specifici (es. `main`, `develop`, feature branches).
- Creazione di **Pull Request** verso branch protetti (es. `main`).

## Step Principali della Pipeline (Esempio)

La pipeline definita in `.github/workflows/ci.yml` (o come verrà finalizzata) include (o includerà) i seguenti step principali, eseguiti all'interno dell'ambiente del Dev Container:

1.  **Checkout del Codice:**
    - Azione: `actions/checkout@vX`
    - Descrizione: Scarica il codice sorgente del repository.

2.  **Setup Ambiente di Sviluppo (Dev Container):**
    - Descrizione: Idealmente, la CI dovrebbe utilizzare la stessa immagine Docker definita in `.devcontainer/Dockerfile` per coerenza con l'ambiente di sviluppo locale. Questo può essere ottenuto buildando l'immagine o pullandola da un registry se pre-buildata.
    - Azioni Correlate: Setup di Python, Node.js, Poetry, e altri strumenti come definiti nel Dockerfile.

3.  **Installazione Dipendenze:**
    - Comando: `poetry install --no-root --no-interaction`
    - Descrizione: Installa tutte le dipendenze del progetto definite nel `poetry.lock`.

4.  **Linting e Formatting Check (tramite Pre-commit):**
    - Comando: `pre-commit run --all-files --show-diff-on-failure`
    - Descrizione: Esegue tutti gli hook configurati in `.pre-commit-config.yaml`. Questo include:
        - `isort` (ordinamento import)
        - `black` (formattazione codice Python)
        - `flake8` (linting Python)
        - `spectral-lint` (linting specifiche OpenAPI)
        - Altri check (YAML, JSON, end-of-file, ecc.)
    - Quality Gate: La pipeline fallisce se uno qualsiasi di questi check non passa.

5.  **Esecuzione Test Unitari e di Integrazione:**
    - Comando: `pytest -v -s --cov=src --cov-report=xml` (esempio)
    - Descrizione: Esegue la suite di test utilizzando `pytest`. Potrebbe includere la generazione di un report di code coverage.
    - Quality Gate: La pipeline fallisce se i test non passano o se la coverage scende sotto una certa soglia (se configurato).

6.  **Verifica Firma GPG dei Commit (Opzionale ma Raccomandato):**
    - Descrizione: Assicura che i commit provengano da fonti verificate. Può essere implementato con action specifiche o script.

7.  **Build Artefatti (Se Applicabile):**
    - Descrizione: Se il progetto produce artefatti buildati (es. pacchetti Python, immagini Docker di produzione), questo step li creerebbe.

8.  **Notifiche:**
    - Descrizione: Notifica gli sviluppatori dell'esito della pipeline (es. via Slack, email, o direttamente su GitHub).

## Quality Gates

I "Quality Gates" sono punti cruciali della pipeline che determinano se la build può procedere o deve fallire. Per questo progetto, i quality gates includono (ma non sono limitati a):

- Passaggio di tutti gli hook di `pre-commit`.
- Successo di tutti i test `pytest`.
- (Eventualmente) Copertura minima del codice.

## Badge di Stato della CI

Una volta configurata la pipeline su un repository GitHub, è possibile aggiungere un badge di stato al file `README.md` per visualizzare rapidamente l'esito dell'ultima build sul branch principale.

Esempio di Markdown per un badge (da adattare):
```markdown
[![CI Pipeline](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml)
```

## Note Attuali

- La configurazione di `pre-commit` per `spectral-lint` ha mostrato problemi di esecuzione con errori `git failed` sia localmente (simulato) che nel container (nelle fasi precedenti). Questo aspetto necessita di ulteriore investigazione per un corretto funzionamento nella CI.
- La pipeline CI è ancora in fase di definizione e potrebbe evolvere con l'avanzamento del progetto. 