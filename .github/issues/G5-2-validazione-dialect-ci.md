# G5-2: Validazione dialect in CI

## Scope

Integrare la validazione del dialect JSON Schema nel workflow CI per garantire che lo schema OpenAPI 3.1 sia sempre conforme al dialect definito in `mif_jsonschema_dialect.json`.

## Obiettivi

- [x] Creare test `tests/spec/test_schema_dialect.py` che valida lo schema OpenAPI 3.1 contro il dialect
- [ ] Integrare il test nel workflow CI esistente
- [ ] Assicurare che la pipeline fallisca se il test fallisce
- [ ] Verificare che tutti i test passino in ambiente dev-container

## Implementazione

1. Creazione di test robusti:
   - Fixture per caricare il dialect e lo schema OpenAPI
   - Test per verificare la validità del dialect
   - Test per verificare che lo schema OpenAPI sia conforme al dialect
   - Gestione corretta delle eccezioni e messaggi di errore informativi

2. Integrazione in CI:
   - Aggiornamento del workflow GitHub Actions per eseguire i nuovi test
   - Configurazione delle dipendenze necessarie nel dev-container
   - Verifica che la pipeline fallisca in caso di errori di validazione

## Definition of Done

- [x] Test di validazione dialect implementati
- [ ] Test integrati nel workflow CI
- [ ] Pipeline CI verde con i nuovi test
- [ ] Documentato nel logbook

## Assignee

- Dev AI

## Priority

Alta (dipendenza da G5-1)

## Related

- G5-1: Dialect JSON Schema
- G5-3: Documentazione HTML con Redocly
- G5-4: Spectral Custom Rules "Gap-Fix" 
