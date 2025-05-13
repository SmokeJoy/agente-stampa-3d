# Setup e Utilizzo di Redocly CLI

Questo documento descrive come utilizzare (o come si prevede di utilizzare) `Redocly CLI` nel progetto "AGENTE STAMPA 3D" per la validazione delle specifiche OpenAPI, il bundling e la generazione di documentazione API interattiva.

**Nota Attuale:** Al momento, Redocly CLI (`@redocly/cli`) non è installato nel Dev Container (è stato rimosso per semplificare la risoluzione di problemi con le versioni npm). Questa sezione descrive funzionalità potenziali o una configurazione futura.

## Funzionalità Principali di Redocly CLI

Redocly CLI è uno strumento potente per lavorare con le specifiche OpenAPI. Le sue funzionalità chiave includono:

- **Linting Avanzato:** Validazione delle specifiche OpenAPI contro regole configurabili (similmente a Spectral, ma con un proprio set di regole e plugin).
- **Bundling:** Capacità di unire specifiche OpenAPI multi-file in un unico file, risolvendo i riferimenti `$ref`.
- **Anteprima Documentazione:** Generazione di un'anteprima locale della documentazione API interattiva.
- **Decorators (Plugin):** Possibilità di estendere la funzionalità tramite plugin per modificare o arricchire le specifiche durante il processo di bundling o linting.

## Installazione (Se Reintrodotto)

Se Redocly CLI venisse reintrodotto nel progetto, l'installazione avverrebbe tipicamente tramite `npm` nel `Dockerfile`:

```bash
# Esempio di installazione nel Dockerfile
npm install -g @redocly/cli@<versione_desiderata>
```

E la verifica:

```bash
redocly --version
```

## Comandi Utili (Esempio)

### 1. Linting della Specifica

Simile a Spectral, Redocly può validare la specifica:

```bash
redocly lint openapi_3_1_demo.json
```

Redocly utilizza un file di configurazione (tipicamente `redocly.yaml` o `.redocly.yaml`) per definire regole, plugin, e altre impostazioni. Se non presente, usa configurazioni di default.

### 2. Bundling della Specifica

Se la specifica OpenAPI fosse suddivisa in più file (es. schemi in file separati, percorsi in file diversi), il comando `bundle` li unirebbe in un unico output:

```bash
redocly bundle openapi_3_1_demo.json -o bundled_openapi.json
```

Questo è utile per distribuire una singola specifica o per prepararla per strumenti che non gestiscono bene i riferimenti multi-file.

### 3. Anteprima della Documentazione API

Redocly può generare un'anteprima della documentazione interattiva basata sulla specifica:

```bash
redocly preview-docs openapi_3_1_demo.json
```

Questo comando avvia un server web locale che serve la documentazione.

### Utilizzo di Plugin Decorator (Esempio Concettuale)

I plugin decorator permettono di modificare dinamicamente la specifica. Ad esempio, un decorator potrebbe essere usato per:

- Aggiungere automaticamente esempi.
- Inserire informazioni di contatto standard.
- Modificare descrizioni o sommari.

La configurazione di un decorator avverrebbe nel file `redocly.yaml`.

**Esempio (ipotetico `redocly.yaml`):**

```yaml
apis:
  main: root/openapi_3_1_demo.json # Percorso alla specifica principale

plugins:
  - ./plugins/my-custom-decorator.js # Percorso a un plugin custom

lint:
  extends:
    - recommended
  rules:
    no-sibling-refs: error
```

## Stato Attuale nel Progetto

Come menzionato, Redocly CLI non è una dipendenza attiva. Se la sua necessità emergesse (es. per funzionalità di bundling avanzate o per il suo specifico motore di documentazione API), la sua integrazione verrebbe rivalutata e documentata qui con dettagli specifici per il progetto.
