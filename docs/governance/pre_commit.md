# Configurazione e Utilizzo di Pre-commit

Questo documento descrive come `pre-commit` è configurato e utilizzato nel progetto "AGENTE STAMPA 3D" per mantenere la qualità del codice e l'aderenza agli standard prima che le modifiche vengano committate.

La configurazione degli hook di pre-commit è definita nel file [`/.pre-commit-config.yaml`](../../.pre-commit-config.yaml).

## Obiettivi dell'Utilizzo di Pre-commit

- **Automazione dei Check:** Eseguire automaticamente linting, formattazione e altri controlli di qualità sul codice modificato.
- **Standardizzazione:** Assicurare che tutto il codice committato aderisca a stili e convenzioni definiti.
- **Prevenzione Errori:** Identificare problemi comuni (es. errori di sintassi, formattazione errata, secret committati) prima del commit.
- **Feedback Rapido:** Fornire feedback immediato allo sviluppatore sull'impatto delle proprie modifiche.

## Hook Configurati

Il file `.pre-commit-config.yaml` include una serie di hook. Tra i più importanti (basandosi su configurazioni tipiche e quanto discusso finora) ci sono:

- **Hook Generali (da `pre-commit-hooks`):
  - `check-yaml`: Valida la sintassi dei file YAML.
  - `check-json`: Valida la sintassi dei file JSON.
  - `end-of-file-fixer`: Assicura che i file terminino con una singola newline.
  - `trailing-whitespace`: Rimuove gli spazi bianchi finali.
  - `check-added-large-files`: Previene il commit di file di grandi dimensioni.
- **Formattazione e Linting Python:
  - `isort`: Ordina automaticamente gli import Python.
  - `black`: Formatta il codice Python in modo standardizzato e non negoziabile.
  - `flake8`: Esegue il linting del codice Python per identificare errori e violazioni di stile (PEP8).
- **Linting OpenAPI (Spectral):
  - `spectral-lint` (configurazione custom o tramite un hook pre-esistente come `pre-commit-hooks-openapi-spec-validate` adattato):
    - **ID Hook Esempio (se custom):** `spectral-lint-openapi`
    - **Entrypoint:** Un comando che esegue `spectral lint` sulla specifica OpenAPI (es. `openapi_3_1_demo.json`) utilizzando il ruleset corretto (es. `/.config/.spectral.yaml`).
    - **File Coinvolti:** Tipicamente punta ai file `.json` o `.yaml` che contengono le specifiche OpenAPI.
- **Sicurezza:
  - `detect-secrets`: Scansiona le modifiche per prevenire il commit accidentale di credenziali o altri dati sensibili.

## Esecuzione di Pre-commit

### Installazione Iniziale

Dopo aver clonato il repository e installato Poetry, è necessario installare gli hook di pre-commit nel repository Git locale:

```bash
poetry install # Assicura che pre-commit sia installato come dipendenza di sviluppo
poetry run pre-commit install
```

Questo comando copia gli hook nella directory `.git/hooks/` del repository locale. Da questo momento, gli hook verranno eseguiti automaticamente prima di ogni `git commit`.

### Esecuzione Manuale

È possibile eseguire manualmente gli hook su tutti i file o su file specifici:

- **Eseguire su tutti i file del repository:**

  ```bash
  poetry run pre-commit run --all-files
  ```

- **Eseguire su file specifici (utile per testare un hook particolare):

  ```bash
  poetry run pre-commit run <nome_hook_id> --files <percorso/al/file1> <percorso/al/file2>
  # Esempio per spectral-lint (assumendo che l'ID sia 'spectral-lint'):
  # poetry run pre-commit run spectral-lint --files openapi_3_1_demo.json
  ```

### Integrazione con la CI

La pipeline di CI (vedi `docs/processes/ci_pipeline.md`) dovrebbe includere uno step che esegue `pre-commit run --all-files` per garantire che i controlli vengano eseguiti anche a livello centralizzato, indipendentemente dal fatto che lo sviluppatore li abbia eseguiti localmente.

## Problemi Noti e Considerazioni

- **Errore `FatalError: git failed`:** Durante le fasi S-2 e S-3, l'esecuzione di `pre-commit run spectral-lint` (e di `pre-commit` in generale in alcuni contesti) ha ripetutamente generato un errore `FatalError: git failed. Is it installed, and are you in a Git repository directory?`.
  - Questo problema si è manifestato sia all'interno del Dev Container (quando si interagiva con il filesystem montato da Windows) sia durante tentativi di esecuzione sull'"host" (ambiente di esecuzione dell'AI).
  - Le cause potrebbero essere legate a:
    - Permessi del filesystem e proprietà dei file quando si opera su volumi montati tra sistemi operativi diversi (es. Windows host, Linux container).
    - Configurazioni di `safe.directory` di Git.
    - Accesso di `pre-commit` alla directory `.git` e ai suoi contenuti.
    - Potenziale corruzione della cache di `pre-commit` (l'output dell'errore spesso menziona un file di log nella cache utente).
- **Soluzione Temporanea (Fase S-3):** Per la Fase S-3, si è deciso di NON eseguire `pre-commit run` all'interno del container per la validazione di Spectral, ma di affidarsi all'esecuzione diretta di `spectral lint` e di posticipare la risoluzione completa del problema di `pre-commit`.
- **Verifica Locale:** Si raccomanda agli sviluppatori di assicurarsi che `pre-commit` funzioni correttamente nel loro ambiente locale prima di committare il codice.

Per una risoluzione definitiva del problema `git failed` con `pre-commit`, sarà necessaria un'analisi più approfondita dell'ambiente di esecuzione e delle interazioni tra Git, pre-commit e il filesystem.

---

### Regola GIT-AI-3: Modularità & Code-Review post-AI

> 🎯 *"Un push senza verifica è un rischio; un modulo troppo grande è un debito. La qualità si costruisce un commit alla volta, un modulo alla volta."*

**Descrizione Breve:** Questa regola rafforza l'importanza della modularità del codice (Articolo 12 delle Regole Dev AI) e istituisce una prassi di verifica minima prima di ogni `git push` per mantenere l'integrità del codebase e facilitare la revisione. Si applica specificamente quando il Dev AI ha generato o modificato codice, specialmente se con assistenza AI.

**Azione Obbligatoria (Pre-Push Check):**

1. **`git diff --staged` (o equivalente IDE):** Rivedere attentamente *tutte* le modifiche preparate per il commit. Verificare che siano intenzionali, coerenti con il task e prive di artefatti indesiderati (es. codice di debug, commenti temporanei).
2. **Esecuzione `pytest` Minimale:** Eseguire almeno i test unitari relativi ai moduli modificati o un sottoinsieme rapido di test critici per garantire che non siano state introdotte regressioni evidenti. L'obiettivo è una verifica rapida, non un ciclo completo di CI.

**Azione Raccomandata (Manutenzione della Modularità):**

1. **Obiettivo Granularità Moduli:** Sforzarsi di mantenere i moduli Python (file `.py`) sotto le **300 righe di codice** (esclusi commenti e importazioni).
2. **Gestione Moduli Estesi:**
    - Se un modulo esistente supera significativamente questa soglia (es. >400-500 righe) o se una nuova funzionalità rischia di farlo crescere oltre, considerare attivamente un refactoring.
    - **Azione:** Aprire una issue interna (o segnalare al Teach Lead) con titolo `Refactor [nome_modulo]: split per modularità` proponendo una strategia di divisione. Questo non blocca il task corrente ma pianifica il miglioramento.
