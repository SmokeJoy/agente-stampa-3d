# Configurazione del Dev Container

Questo documento fornisce una sintesi della configurazione dell'ambiente di sviluppo containerizzato utilizzato nel progetto "AGENTE STAMPA 3D". L'ambiente è definito principalmente tramite i file `.devcontainer/Dockerfile` e `.devcontainer/devcontainer.json` (quest'ultimo non attualmente presente nel progetto ma è parte dello standard Dev Container).

## `.devcontainer/Dockerfile`

Il `Dockerfile` definisce l'immagine Docker utilizzata per l'ambiente di sviluppo. Ecco i punti salienti:

- **Immagine Base:** Parte da `python:3.12-slim` per un ambiente Python leggero e aggiornato.
- **Variabili d'Ambiente (ARG/ENV):**
    - `NODE_VERSION`: Specificata a `20.14.0` (anche se l'installazione avviene poi tramite `apt-get`).
    - `POETRY_HOME`: Impostato a `/opt/poetry`.
    - `POETRY_VERSION`: Impostato a `1.8.3`.
    - `PATH`: Esteso per includere la directory `bin` di Poetry.
- **Directory di Lavoro:** Impostata a `/app` all'interno del container (anche se lo script `run_in_container.sh` poi opera in `/workspace` che è il volume montato).

- **Dipendenze di Sistema Installate (tramite `apt-get`):**
    - `curl`, `gnupg`, `build-essential`, `git`
    - `nodejs`, `npm` (per l'esecuzione di strumenti JavaScript/Node.js)

- **Strumenti Specifici Installati:**
    - **Node.js e npm:** Installati via `apt-get`. Versioni verificate con `node -v` e `npm -v`.
    - **Spectral CLI:** Installato globalmente via `npm` alla versione `@stoplight/spectral-cli@6.15.0`. Verificato con `spectral --version`.
    - **Poetry:** Installato tramite lo script ufficiale `install.python-poetry.org` alla versione `1.8.3`. Verificato con `poetry --version`.
    - **Git:** Installato via `apt-get`. Verificato con `git --version`.

- **Script Personalizzati:**
    - `run_in_container.sh`: Copiato in `/usr/local/bin/run_in_container.sh` e reso eseguibile. Questo script è l'entrypoint per eseguire operazioni di build, linting e test all'interno del container.

- **Copia del Progetto:** L'intera directory del progetto (il contesto della build) viene copiata in `/app` (o `/workspace` a seconda di come si interpreta `WORKDIR` vs il mount point effettivo) con `COPY . .`.

## `.devcontainer/devcontainer.json` (Standard, non presente attualmente)

Sebbene non esplicitamente fornito nei file attuali, un file `devcontainer.json` è tipicamente usato per:
- Specificare quale Dockerfile usare.
- Definire il nome del servizio/container.
- Configurare i mount dei volumi (es. la directory del progetto locale in `/workspace` nel container).
- Impostare variabili d'ambiente specifiche per il container.
- Elencare le estensioni VS Code da installare automaticamente nel container.
- Definire comandi da eseguire post-creazione del container.

## Script `.devcontainer/run_in_container.sh`

Questo script è cruciale per l'esecuzione di task all'interno del container. La versione attuale semplificata esegue:
1. `cd /workspace`
2. `poetry lock --no-update`
3. `poetry install --no-root --no-interaction`
4. Genera il log di `spectral lint` in `evidence/logs/spectral_lint_run2.log` utilizzando il ruleset `/workspace/.config/.spectral.yaml`.
5. Esce con l'exit code di Spectral.

## Comandi Utili (Esempio)

- **Build dell'immagine:**
  ```bash
  docker build -t agente-stampa-3d-dev-image .devcontainer
  ```
- **Avvio del container in background (per esecuzioni successive con `docker exec`):
  ```bash
  docker run -d --name agente-stampa-3d-dev-container -v "$(pwd):/workspace" agente-stampa-3d-dev-image tail -f /dev/null
  # Su Windows, potrebbe essere necessario usare %CD% o un path assoluto per il volume:
  # docker run -d --name agente-stampa-3d-dev-container -v "E:\agente-stampa-3D:/workspace" agente-stampa-3d-dev-image tail -f /dev/null
  ```
- **Esecuzione dello script nel container (dopo l'avvio):
  ```bash
  docker exec agente-stampa-3d-dev-container /bin/bash -c 'cd /workspace && ./.devcontainer/run_in_container.sh'
  # Oppure, dato che è nel PATH e è eseguibile:
  # docker exec agente-stampa-3d-dev-container run_in_container.sh
  ```
- **Accesso interattivo al container:
  ```bash
  docker exec -it agente-stampa-3d-dev-container /bin/bash
  ```

Questo setup mira a fornire un ambiente di sviluppo consistente e riproducibile per tutti i collaboratori del progetto. 