# G5-2: Validazione dialect in CI

## Scope

Integrare la validazione del dialect JSON Schema nel workflow CI per garantire che lo schema OpenAPI 3.1 
sia sempre conforme al dialect definito in `mif_jsonschema_dialect.json`.

## Obiettivi

- [ ] Verificare che i test in `tests/spec/test_schema_dialect.py` funzionino correttamente in ambiente CI
- [ ] Assicurare che la pipeline fallisca se lo schema OpenAPI non è conforme al dialect
- [ ] Documentare il processo di validazione nel logbook
- [ ] Configurare il job CI per eseguire il test come parte dei controlli standard
- [ ] Testare la robustezza della validazione con casi limite

## Implementazione

1. Verifica dei test esistenti:
   - [ ] Confermare che `test_dialect_schema_is_valid` verifica la struttura del dialect
   - [ ] Confermare che `test_dialect_contains_custom_keywords` verifica la presenza di `x-internal` e `x-risk`
   - [ ] Confermare che `test_openapi_schema_validates_against_dialect` esegue la validazione completa

2. Miglioramenti al workflow CI:
   - [ ] Aggiornare il job `lint-and-test` per eseguire i test di dialect
   - [ ] Aggiungere controlli di sicurezza per identificare modifiche non autorizzate al dialect
   - [ ] Configurare la pipeline per fallire esplicitamente se la validazione fallisce

3. Documentazione e reporting:
   - [ ] Aggiornare `docs/processes/ci_pipeline.md` con i dettagli della validazione del dialect
   - [ ] Implementare l'output di report leggibili in caso di errore
   - [ ] Aggiornare il logbook con i dettagli dell'implementazione

## Definition of Done

- [ ] Tutti i test di validazione del dialect passano nell'ambiente CI
- [ ] Le modifiche intenzionalmente non valide causano il fallimento della pipeline
- [ ] Documentazione aggiornata nel logbook e in `docs/processes/ci_pipeline.md`
- [ ] Pull request approvata e mergiata

## Assignee

- Dev AI

## Priority

Alta (dipendenza da G5-1)

## Related

- G5-1: Dialect JSON Schema
- G5-3: Documentazione HTML con Redocly
- G5-4: Spectral Custom Rules "Gap-Fix"
