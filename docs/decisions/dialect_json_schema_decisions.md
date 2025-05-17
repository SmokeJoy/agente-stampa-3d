# Decisioni per JSON Schema Dialect

**Data**: 2024-09-24
**Autore**: Dev AI
**Issue di riferimento**: G5-1 Dialect JSON Schema

## Contesto

Per il progetto AGENTE STAMPA 3D, è stato richiesto di definire un dialect JSON Schema personalizzato che estende le funzionalità standard di OpenAPI 3.1 con parole chiave custom necessarie per le regole Spectral.

## Decisioni

### 1. Scelta delle parole chiave personalizzate

Abbiamo scelto di implementare le seguenti parole chiave personalizzate:

1. **`x-internal` (tipo boolean)**
   - **Scopo**: Marcare endpoint, operazioni, schemi o parametri come ad uso interno.
   - **Motivazione**: Permette di distinguere chiaramente le API pubbliche da quelle interne, facilitando la gestione della documentazione e delle politiche di sicurezza/accesso.
   - **Uso in Spectral**: Può essere usato per regole che avvisano quando un endpoint interno viene esposto senza adeguate protezioni o per escludere gli endpoint interni da certe validazioni.

2. **`x-risk` (tipo boolean)**
   - **Scopo**: Indicare se un'operazione, schema o parametro comporta rischi di sicurezza o affidabilità.
   - **Motivazione**: Fornisce un modo semplice per evidenziare componenti che richiedono particolare attenzione in termini di sicurezza o robustezza.
   - **Uso in Spectral**: Può essere usato per applicare regole più severe o per richiedere documentazione aggiuntiva per le API marcate come rischiose.

### 2. Strategia per proprietà non riconosciute

Abbiamo impostato `"unevaluatedProperties": false` nel dialect per garantire che vengano rifiutate tutte le proprietà non espressamente definite. Questa scelta:

1. **Migliora la sicurezza e la governance**: Impedisce l'introduzione accidentale di estensioni o campi non documentati.
2. **Facilita la validazione**: Tutte le estensioni devono essere dichiarate esplicitamente nel dialect per essere accettate.
3. **Garantisce coerenza**: Assicura che tutte le API del progetto seguano lo stesso set di regole e convenzioni.

### 3. Pattern per validazione degli ID operazione

Abbiamo definito un pattern `"^[a-z][a-zA-Z0-9]*$"` per gli `operationId` che assicura:
1. L'uso di camelCase come convenzione di nomenclatura
2. Che ogni ID inizi con una lettera minuscola
3. Che vengano utilizzati solo caratteri alfanumerici

### 4. Definizione del vocabolario personalizzato

Abbiamo aggiunto una sezione `meta.vocabulary` che definisce formalmente le nostre parole chiave personalizzate, migliorando l'interoperabilità con altri strumenti che potrebbero utilizzare il nostro dialect.

## Impatto

Queste decisioni garantiscono che:

1. Lo schema OpenAPI 3.1 sarà validato in modo coerente e prevedibile
2. Le estensioni personalizzate saranno documentate e utilizzate in modo uniforme
3. Spectral e altri strumenti potranno sfruttare queste estensioni per implementare regole di governance specifiche

## Note di implementazione

Il dialect è stato implementato nel file `mif_jsonschema_dialect.json` nella root del progetto, con `$schema` che punta a `https://json-schema.org/draft/2020-12/schema` e `$id` che rispecchia l'URL raw del repository GitHub.

Tutti i test di validazione sono stati implementati in `tests/spec/test_schema_dialect.py`. 
