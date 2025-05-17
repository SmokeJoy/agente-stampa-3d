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
   - [ ] Confermare che `test_openapi_schema_validates_against_dialect` valida lo schema OpenAPI
   - [ ] Aggiungere assertion più specifiche per verificare campi critici
   
2. Aggiornamento workflow CI:
   - [ ] Aggiungere step dedicated nel file `.github/workflows/ci.yml`
   - [ ] Installare dipendenze necessarie (jsonschema)
   - [ ] Configurare output di test per diagnostica
   
3. Artefatti CI:
   - [ ] Generare report di validazione leggibili
   - [ ] Salvare report come artefatto della pipeline

## Definition of Done

- [ ] Pipeline CI esegue correttamente il test del dialect
- [ ] Pipeline fallisce se lo schema non è valido
- [ ] Report di validazione generato e salvato come artefatto
- [ ] Documentazione aggiornata nel logbook

## Assignee

- Dev AI

## Priority

Alta (dipendenza da G5-1)

## Related

- G5-1: Dialect JSON Schema
- G5-3: Documentazione HTML con Redocly
- G5-4: Spectral Custom Rules "Gap-Fix"
