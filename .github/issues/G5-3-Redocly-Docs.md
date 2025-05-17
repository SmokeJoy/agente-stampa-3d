# G5-3: Documentazione HTML con Redocly

## Scope

Implementare la generazione di documentazione HTML per l'API OpenAPI 3.1 utilizzando Redocly, 
per fornire una documentazione interattiva, esteticamente gradevole e sempre aggiornata.

## Obiettivi

- [ ] Configurare Redocly CLI per la generazione di documentazione HTML
- [ ] Integrare la generazione della documentazione nel workflow CI
- [ ] Pubblicare la documentazione HTML come artefatto della pipeline CI
- [ ] Assicurare che la documentazione rifletta le estensioni custom del dialect JSON Schema
- [ ] Migliorare l'esperienza utente con esempi e descrizioni esaustive

## Implementazione

1. Setup iniziale:
   - [ ] Installare e configurare `@redocly/cli` come dipendenza di sviluppo
   - [ ] Creare file di configurazione `redocly.yaml` nella root del progetto
   - [ ] Definire lo stile e le opzioni di personalizzazione della documentazione

2. Integrazione con OpenAPI 3.1:
   - [ ] Verificare la compatibilità di Redocly con le funzionalità di OpenAPI 3.1
   - [ ] Configurare il rendering delle estensioni custom `x-internal` e `x-risk`
   - [ ] Assicurare che la validazione di Redocly non interferisca con il dialect personalizzato

3. Integrazione CI:
   - [ ] Aggiungere step nel workflow CI per generare la documentazione HTML
   - [ ] Configurare l'archiviazione della documentazione come artefatto della pipeline
   - [ ] Implementare un meccanismo di deploy automatico (opzionale)

4. Miglioramenti alla documentazione:
   - [ ] Aggiungere esempi realistici per ogni endpoint
   - [ ] Migliorare le descrizioni di campi e parametri
   - [ ] Organizzare gli endpoint in gruppi logici con tag appropriati

## Definition of Done

- [ ] Documentazione HTML generata automaticamente ad ogni push
- [ ] Estensioni custom visualizzate correttamente nella documentazione
- [ ] Artefatto di documentazione disponibile per il download nelle esecuzioni CI
- [ ] Feedback positivo dal team sulla qualità e usabilità della documentazione
- [ ] Procedura documentata nel logbook

## Assignee

- Dev AI

## Priority

Media (dopo G5-1 e G5-2)

## Related

- G5-1: Dialect JSON Schema
- G5-2: Validazione dialect in CI
- G5-4: Spectral Custom Rules "Gap-Fix"
