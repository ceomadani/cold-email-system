---
id: subsequence-nurture
tipo: follow-up
status: standard
versione: 1.0
segmento: generico
lingua: it
ultimo_aggiornamento: 2026-06-10
metrica: "riciclo non-responder, il 'no' di marzo è spesso 'non ora'"
---

# Subsequence di nurture — riciclo non-responder

**Quando:** un contatto ha completato la sequenza (incluso il breakup) senza rispondere. NON si butta — si ricicla dopo **60-90 giorni** con un angolo nuovo (§8 guida). La lista è già pagata; riprovare costa quasi zero.

**Logica:** il silenzio non è un "no" definitivo. È "non in questo momento, con questo angolo". Tre mesi dopo, con un trigger diverso (una notizia, un nuovo case study, un cambio di stagione del loro business), lo stesso contatto può rispondere.

## Touch di riattivazione (60-90 giorni dopo il breakup)
```
{{first_name}},

{Ti riscrivo perché|Torno da te perché} {{nuovo_trigger}}.

{Mi è venuto in mente|Ho pensato a} {{company_name}} — {{aggancio_specifico}}.

{Ha senso|Vale} un confronto rapido, ora che {{condizione_cambiata}}?

{{firma}}
```

## Variabili
`{{first_name}}`, `{{company_name}}`, `{{firma}}` + `{{nuovo_trigger}}`, `{{aggancio_specifico}}`, `{{condizione_cambiata}}` (il motivo NUOVO del ricontatto)

## Regola
Il ricontatto deve avere una **ragione nuova e genuina** — un trigger fresco, non "volevo solo ricontrollare". Senza ragione nuova è nagging e brucia la possibilità definitivamente.

## Cadenza
- Riattivazione singola a 60-90 giorni
- Se silenzio → seconda subsequence a +90 giorni con angolo ancora diverso
- Massimo 2-3 cicli di nurture, poi il contatto esce dalla rotazione attiva (resta nel DB, stato `dormiente`)
