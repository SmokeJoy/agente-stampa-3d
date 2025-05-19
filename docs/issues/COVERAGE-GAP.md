# Issue: COVERAGE-GAP

**ID:** COVERAGE-GAP-001  
**Tipo:** Enhancement  
**Priorità:** Alta  
**Status:** Aperto  
**Assegnato a:** Dev AI  
**Data apertura:** 2025-05-17  
**Data target:** 2025-05-20 (fine G6)  

## Descrizione

Attualmente la copertura dei test è all'81%, l'obiettivo è raggiungere l'85% entro la fine del milestone G6. Questo miglioramento è necessario per garantire una maggiore robustezza del codice e ridurre i rischi di regressione.

## Piano d'azione

1. **Moduli critici da migliorare:**
   - `services/uploader/validator.py` (+2%)
   - `services/redis/redis_client.py` (+1%)
   - `utils/ratelimit.py` (+1%)
   - `routers/uploader.py` (+1%)

2. **Approccio:**
   - Aggiungere test parametrizzati per coprire più casi d'uso
   - Implementare test per gli edge case (errori di rete, timeout, etc.)
   - Migliorare i mock per simulare scenari di errore
   - Aumentare la copertura delle condizioni di branch nei controlli di validazione

3. **Punti specifici da testare:**
   - Fallimenti di connessione Redis
   - Gestione del rate limit quando Redis non è disponibile
   - Validazione di file con formati non supportati o corrotti
   - Casi limite di dimensione dei file (al limite esatto della soglia)
   - Percorsi di errore nei webhook
   - Risposte HTTP di errore nelle integrazioni esterne

## Metriche

| Modulo | Coverage attuale | Target |
|--------|-----------------|--------|
| Globale | 81% | 85% |
| utils/ratelimit.py | 78% | 90% |
| services/uploader/validator.py | 75% | 88% |
| services/redis/redis_client.py | 72% | 85% |
| routers/uploader.py | 80% | 88% |

## Note

Il miglioramento della coverage si concentrerà sulla qualità dei test, non solo sulla percentuale. L'obiettivo è assicurare che i test siano significativi e contribuiscano a prevenire regressioni e bug nel codice. 
 
