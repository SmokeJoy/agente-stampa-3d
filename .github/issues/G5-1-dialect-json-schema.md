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
- [x] Integrare il test in CI

## Implementazione

1. Verifica RFC JSON Schema 2020-12 per struttura corretta
2. Includi tutte le parole chiave richieste nel dialect
3. Implementa unit test con jsonschema per validare sia il dialect che lo schema OpenAPI
4. Aggiungi jsonschema come dipendenza in poetry

## Definition of Done

- [x] Il dialect è definito con `$schema` e `$id` corretti
- [x] Il dialect include le keywords custom
- [x] Il test `tests/spec/test_schema_dialect.py` verifica correttamente il dialect
- [x] Commit firmato GPG con messaggio descrittivo
- [x] Documentazione nel logbook e nel decision record

## Assignee

- Dev AI

## Priority

Alta (blocca tutti gli altri task della feature G5)

## Related

- G5-2: Validazione dialect in CI
- G5-3: Documentazione HTML con Redocly
- G5-4: Spectral Custom Rules "Gap-Fix"
