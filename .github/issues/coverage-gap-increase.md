# Increase test coverage to 85 percent (G6 target)

## Scope

Incrementare la copertura dei test dal corrente 81% all'85% entro la fine del milestone G6.
Questo miglioramento è fondamentale per garantire la qualità e la stabilità del codice,
focalizzandosi sui componenti critici dell'applicazione.

## Approach

1. **Test parametrizzati per rate limiting:**
   - Aggiungere test per scenari di `burst limit` con vari valori di soglia
   - Implementare test per il reset delle finestre temporali di rate limiting
   - Simulare scenari di fallback quando Redis non è disponibile

2. **Test edge case per uploader:**
   - Validazione di file con dimensioni esattamente al limite consentito
   - Test di file con formati corrotti ma header validi
   - Comportamento con upload paralleli/concorrenti

3. **Test di integrazione webhook:**
   - Simulazione errori di connessione nelle chiamate webhook
   - Verifica politiche di retry con backoff esponenziale
   - Test di timeout e interruzioni durante le notifiche

4. **Copertura delle condizioni branch:**
   - Identificare e testare tutti i percorsi condizionali nei moduli critici
   - Sviluppare scenari che attivino i percorsi di errore meno frequenti
   - Migliorare la simulazione di condizioni di fallimento dei servizi esterni

## Definition of Done (DoD)

- [ ] Copertura test globale ≥ 85% (misurato con `pytest --cov`)
- [ ] Nessun modulo core sotto l'80% di copertura
- [ ] Tutti i percorsi critici di errore coperti da test
- [ ] Report di copertura integrato nella pipeline CI
- [ ] Test parametrizzati per tutti i componenti principali

## Owner

**Assignee:** Dev AI  
**Reviewer:** Teach Lead  
**Deadline:** Fine del milestone G6 (2025-05-20)

## Related

- [PR #feature-ci-integration](https://github.com/organizzazione/agente-stampa-3D/pull/feature-ci-integration)
- Task G6-INIT del logbook unificato
