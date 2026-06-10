# Prompt AI — pipeline di generazione

L'AI non scrive cold email a caso: esegue **prompt strutturati** che incorporano il sistema (i 6 framework, le regole copy, le variabili canonical). Questa cartella è la pipeline di prompt, dal research alla classificazione delle risposte. Sono i prompt che si standardizzano nel tempo — quando uno produce output migliori, si versiona e diventa lo standard.

## La pipeline

| # | Prompt | Input | Output |
|---|--------|-------|--------|
| 01 | `01-icp-research.md` | Descrizione business + offer | ICP definito, ruolo decisore, criteri di targeting |
| 02 | `02-offer-creation.md` | Servizio + capacità | Frontend offer ad alto valore percepito |
| 03 | `03-script-generation.md` | Framework + segmento + variabili | Script email (3 tier × 3 lunghezze) |
| 04 | `04-personalization.md` | Dati enrichment per-contatto | La riga `{{trigger}}` personalizzata |
| 05 | `05-reply-classification.md` | Testo della risposta | Categoria (interested/objection/timing/referral) + bozza |

## Come si usano

Ogni prompt è copia-incolla in Claude/GPT. I blocchi `[...]` sono da riempire con i dati reali. L'output di un prompt è spesso l'input del successivo (01 → 02 → 03).

## Come crescono (versioning)

Stesso principio dei template (`templates/_CONVENZIONI.md`):
- Ogni prompt ha `status` e `versione` nel frontmatter.
- Quando una versione produce output sistematicamente migliori (meno editing manuale, reply rate più alto sugli script che genera), si promuove a `standard` e si logga in `_CHANGELOG.md`.
- Le varianti in test si nominano con suffisso (`03-script-generation-b.md`).

## Regola trasversale

Ogni prompt che genera copy DEVE incorporare le guardrail della §7.4 della guida: <70 parole, spintax, no emoji, no link, variabili Clay-merge-safe, soft CTA. Sono già scritte dentro ogni prompt — non si rimuovono.
