# Regole Spectral Personalizzate e Standard

Questo documento elenca e descrive le regole Spectral utilizzate nel progetto "AGENTE STAMPA 3D" per il linting delle specifiche OpenAPI 3.1.0. Le regole sono definite nel file `.config/.spectral.yaml`.

Il ruleset estende le regole standard di `spectral:oas` e aggiunge/modifica le seguenti regole custom:

## Regole Personalizzate definite in `.config/.spectral.yaml`

Il file di configurazione completo si trova qui: [`/.config/.spectral.yaml`](../../.config/.spectral.yaml).

Di seguito un estratto delle 5 regole personalizzate (o con configurazione specifica) più rilevanti:

### 1. `no-legacy-nullable`

- **Descrizione Fornita:** Evita l'uso di `'nullable: true'` deprecato, preferendo `type: ['type', 'null']`.
- **Messaggio d'Errore/Warning:** "La proprietà '{{property}}' (o percorso '{{path}}') usa 'nullable: true'. OpenAPI 3.1.0 preferisce type: [..., \"null\"]."
- **Logica (`given`):** `$..[?(@ && @.nullable === true)]` (Seleziona qualsiasi oggetto che ha esplicitamente `nullable: true`).
- **Severità:** `warn`
- **Azione (`then`):** La funzione `falsy` fallisce se `nullable: true` è trovato, segnalando la regola.
- **Formati Applicabili:** `oas3_1`
- **Scopo:** Incoraggiare l'uso della sintassi corretta per la nullabilità in OpenAPI 3.1.0, migliorando la chiarezza e l'aderenza allo standard.

### 2. `require-operationid`

- **Descrizione Fornita:** Ogni operazione API deve avere un `operationId` definito e non vuoto.
- **Messaggio d'Errore/Warning:** "L'operazione {{path}} deve avere un 'operationId' univoco e non vuoto."
- **Logica (`given`):** `$.paths.*[get,post,put,delete,patch,options,head,trace]` (Seleziona tutti gli oggetti operazione).
- **Severità:** `error`
- **Azione (`then`):** Il campo `operationId` deve essere `truthy` (esistere e non essere vuoto).
- **Formati Applicabili:** `oas3_1`
- **Scopo:** Garantire che ogni operazione abbia un identificatore univoco, utile per la generazione di codice, la documentazione e il routing.

### 3. `exclusive-minimum-numeric`

- **Descrizione Fornita:** `exclusiveMinimum` deve essere un numero in OpenAPI 3.1.0.
- **Messaggio d'Errore/Warning:** "exclusiveMinimum per {{path}} deve essere un valore numerico."
- **Logica (`given`):** `$..*[?(@ && @.exclusiveMinimum !== undefined)]` (Seleziona oggetti con `exclusiveMinimum` definito).
- **Severità:** `error`
- **Azione (`then`):** Il campo `exclusiveMinimum` deve essere di tipo `number`.
- **Formati Applicabili:** `oas3_1`
- **Scopo:** Assicurare la corretta tipizzazione di `exclusiveMinimum` secondo la specifica OpenAPI 3.1.0, dove il suo valore booleano è stato rimosso e deve essere solo numerico.

### 4. `exclusive-maximum-numeric`

- **Descrizione Fornita:** `exclusiveMaximum` deve essere un numero in OpenAPI 3.1.0.
- **Messaggio d'Errore/Warning:** "exclusiveMaximum per {{path}} deve essere un valore numerico."
- **Logica (`given`):** `$..*[?(@ && @.exclusiveMaximum !== undefined)]` (Seleziona oggetti con `exclusiveMaximum` definito).
- **Severità:** `error`
- **Azione (`then`):** Il campo `exclusiveMaximum` deve essere di tipo `number`.
- **Formati Applicabili:** `oas3_1`
- **Scopo:** Simile a `exclusive-minimum-numeric`, garantisce la corretta tipizzazione di `exclusiveMaximum`.

### 5. `array-query-param-style-explode`

- **Descrizione Fornita:** I parametri di query di tipo array dovrebbero usare `style: form` e `explode: true`.
- **Messaggio d'Errore/Warning:** "Il parametro di query array '{{property}}' (o percorso '{{path}}') dovrebbe usare style: form e explode: true."
- **Logica (`given`):** `$..parameters[?(@ && @.in === 'query' && @.schema && @.schema.type === 'array')]` (Seleziona parametri di query che sono array).
- **Severità:** `warn`
- **Azione (`then`):** Verifica che l'oggetto parametro abbia le proprietà `style` con valore `form` e `explode` con valore `true`.
- **Formati Applicabili:** `oas3_1`
- **Scopo:** Promuovere uno stile di serializzazione standard e ampiamente supportato per i parametri di query di tipo array.

## Utilizzo

Spectral viene eseguito automaticamente come parte degli hook di pre-commit (se configurato correttamente e funzionante) e può essere eseguito manualmente per validare le specifiche OpenAPI. Il comando tipico utilizzato nel progetto è:

```bash
spectral lint --ruleset /workspace/.config/.spectral.yaml openapi_3_1_demo.json
```
(Eseguito dalla root del progetto, assumendo che `/workspace` sia il mount point nel container).

L'output di Spectral viene registrato in `evidence/logs/`. 