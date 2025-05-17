# G5-1: Dialect JSON Schema

## Scope

Implementare e validare un dialect JSON Schema personalizzato per il progetto AGENTE STAMPA 3D, 
che estende le funzionalità standard di OpenAPI 3.1 con parole chiave custom necessarie per le regole Spectral.

## Obiettivi

- [x] Definire il file `mif_jsonschema_dialect.json` nella root del progetto
- [x] Impostare `$schema` che punta a `https://json-schema.org/draft/2020-12/schema`
- [x] Aggiungere parole chiave custom richieste da Spectral:
  - [x] `x-internal` (boolean) per marcare endpoint/operazioni ad uso interno
  - [x] `x-risk` (enum) per indicare il livello di rischio di sicurezza/affidabilità
- [x] Impostare un `$id` univoco con URI del repository raw
- [x] Creare test per validare lo schema dialect con `jsonschema`

## Implementazione

1. Definizione del dialect con supporto per:
   - Validazione struttura OpenAPI 3.1.0
   - Estensioni custom `x-internal` e `x-risk`
   - Pattern per `operationId` in camelCase

2. Test di validazione:
   - Creazione di test in `tests/spec/test_schema_dialect.py`
   - Verifica che il dialect sia valido
   - Verifica che il dialect contenga le keyword custom
   - Verifica che lo schema OpenAPI 3.1 sia valido secondo il dialect

## Definition of Done

- [x] File `mif_jsonschema_dialect.json` creato e popolato correttamente
- [x] Test `tests/spec/test_schema_dialect.py` scritto e passante
- [x] Schema OpenAPI esistente convalidato con successo contro il dialect
- [x] Documentato nel logbook

## Assignee

- Dev AI

## Priority

Alta (blocca gli altri task G5)

## Related

- G5-2: Validazione dialect in CI
- G5-3: Documentazione HTML con Redocly
- G5-4: Spectral Custom Rules "Gap-Fix"
