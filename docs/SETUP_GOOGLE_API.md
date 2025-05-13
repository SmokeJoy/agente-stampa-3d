# Guida alla Configurazione dell'API di Google Calendar

Questa guida descrive i passaggi necessari per configurare l'accesso all'API di Google Calendar per il progetto "Agente Stampa 3D".

## 1. Creazione di un Progetto in Google Cloud Console

1.  Vai alla [Google Cloud Console](https://console.cloud.google.com/).
2.  Crea un nuovo progetto (o selezionane uno esistente).
3.  Assicurati che il nome del progetto sia descrittivo (es. "Agente Stampa 3D API Access").

## 2. Abilitazione dell'API di Google Calendar

1.  Nel pannello di navigazione, vai su "API e servizi" > "Libreria".
2.  Cerca "Google Calendar API" e abilitala per il tuo progetto.

## 3. Configurazione della Schermata di Consenso OAuth

1.  Vai su "API e servizi" > "Schermata consenso OAuth".
2.  Scegli il tipo di utente:
    *   **Interno**: Se l'applicazione è usata solo da utenti all'interno della tua organizzazione Google Workspace.
    *   **Esterno**: Se l'applicazione sarà usata da qualsiasi utente con un account Google.
3.  Compila i dettagli richiesti:
    *   **Nome dell'applicazione**: Es. "Agente Stampa 3D"
    *   **Email di assistenza utenti**: La tua email.
    *   **Logo dell'applicazione** (opzionale).
    *   **Domini autorizzati**: Se applicabile, aggiungi il dominio dell'applicazione.
    *   **Informazioni di contatto dello sviluppatore**: La tua email.
4.  Salva e continua.

## 4. Aggiunta degli Scopes

1.  Nella sezione "Scopes" della configurazione della schermata di consenso OAuth, fai clic su "Aggiungi o rimuovi ambiti".
2.  Cerca e aggiungi gli scopes necessari per l'accesso al calendario. Per questo progetto, potrebbero includere:
    *   `https://www.googleapis.com/auth/calendar.events` (Lettura/Scrittura eventi)
    *   `https://www.googleapis.com/auth/calendar.readonly` (Solo lettura, se sufficiente per alcune funzionalità)
    *   *Assicurati di richiedere solo gli scopes minimi necessari.*
3.  Aggiorna e salva.

## 5. Creazione delle Credenziali OAuth 2.0 (ID Client OAuth)

1.  Vai su "API e servizi" > "Credenziali".
2.  Fai clic su "+ CREA CREDENZIALI" e seleziona "ID client OAuth".
3.  Scegli il "Tipo di applicazione":
    *   Per questo progetto, che eseguirà uno script localmente per ottenere il token iniziale, "Applicazione desktop" è una scelta appropriata per il flusso di autorizzazione iniziale.
    *   Se l'API backend dovesse gestire autonomamente il refresh del token per più utenti in un contesto web, "Applicazione Web" potrebbe essere più adatta, ma la configurazione del flusso sarebbe diversa.
4.  Dai un nome all'ID client (es. "Agente Stampa 3D Desktop Client").
5.  Fai clic su "CREA".
6.  Apparirà una finestra con il tuo **ID client** e il **Client secret**. **Scarica il file JSON** (solitamente nominato `client_secret_XXXXXXXX.json`).
    *   **IMPORTANTE**: Rinomina questo file in `client_secret.json`.
    *   **SICUREZZA**: Conserva questo file in modo sicuro. **NON committarlo MAI al repository Git.** Mettilo nella directory `secrets/` del tuo progetto, che è inclusa nel `.gitignore`.

## 6. Gestione del File `token.json`

Lo script di autenticazione (`services/google_calendar/auth_flow.py`) genererà un file `token.json` (o `secrets/token.json` come configurato in `config/settings.py`) dopo il primo flusso di autorizzazione andato a buon fine. Questo file contiene il token di accesso e il token di refresh.

*   **SICUREZZA**: Anche questo file contiene informazioni sensibili e **NON deve essere committato al repository Git**. La directory `secrets/` è già configurata per essere ignorata.

## 7. VARIABILI D'AMBIENTE (Opzionale, per override dei default)

Il file `config/settings.py` utilizza Pydantic `BaseSettings` per gestire la configurazione. Di default, si aspetta di trovare i file delle credenziali in percorsi specifici (`secrets/client_secret.json` e `secrets/token.json`) e usa una porta di default per il server OAuth locale (8765).

Se desideri sovrascrivere questi default, puoi creare un file `.env` nella root del progetto e specificare le seguenti variabili:

```env
# Percorso del file JSON scaricato da Google Cloud Console (rinominato)
# GOOGLE_CLIENT_SECRET_FILE=secrets/client_secret.json

# Percorso del file dove verranno salvati i token di accesso/refresh
# GOOGLE_TOKEN_FILE=secrets/token.json

# Porta da utilizzare per il server locale durante il flusso OAuth 2.0
# GOOGLE_OAUTH_PORT=8765
```

**Nota:** Se i file si trovano nei percorsi di default e la porta è corretta, non è necessario impostare queste variabili nel file `.env`.

Ricorda di consultare la documentazione ufficiale di Google Cloud e dell'API di Google Calendar per informazioni più dettagliate e aggiornate.