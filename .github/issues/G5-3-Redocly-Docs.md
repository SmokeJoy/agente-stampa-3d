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
   - [ ] Creare file di configurazione `redocly.yaml` nel root del progetto
   - [ ] Testare la generazione HTML locale

2. Integrazione CI:
   - [ ] Aggiungere step nel workflow GitHub Actions
   - [ ] Configurare cache per le dipendenze npm
   - [ ] Salvare output HTML come artefatto della pipeline

3. Personalizzazione:
   - [ ] Configurare tema e stile
   - [ ] Migliorare esempi API
   - [ ] Aggiungere guide d'uso
   - [ ] Rendere visibili le estensioni custom (x-internal, x-risk)

## Definition of Done

- [ ] Documentazione HTML generata con successo durante la CI
- [ ] Artefatti HTML disponibili per ogni build di PR
- [ ] Rendering corretto di tutte le operazioni API
- [ ] Visualizzazione corretta delle estensioni custom

## Assignee

- Dev AI

## Priority

Media (dipendenza da G5-1 e G5-2)

## Related

- G5-1: Dialect JSON Schema
- G5-2: Validazione dialect in CI
- G5-4: Spectral Custom Rules "Gap-Fix"
