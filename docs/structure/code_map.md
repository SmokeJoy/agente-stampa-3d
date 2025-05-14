# Mappatura del Codice Sorgente Python Esistente

Questo documento mappa i file Python (`.py`) presenti nel progetto "AGENTE STAMPA 3D" alla data di creazione di questo documento, con una breve descrizione della loro responsabilità principale.

| Percorso File                           | Responsabilità Dichiarata (1 riga)                                       | Righe di Codice (approx) |
| --------------------------------------- | ------------------------------------------------------------------------ | ------------------------ |
| `main.py`                               | Entry point dell'applicazione FastAPI, definisce endpoint di root.       | 7                        |
| `services/google_calendar/auth_flow.py` | Gestisce il flusso di autenticazione OAuth2 per le API di Google Calendar. | 52                       |
| `config/settings.py`                    | Definisce e carica le impostazioni di configurazione dell'applicazione.  | 14                       |
| `scripts/generate_fake_secret.py`       | Genera un file `client_secret.json` fittizio per ambienti di test/CI.    | 45                       |

**Nota:** Tutti i file esistenti rispettano ampiamente il limite di 300 righe per modulo. 
