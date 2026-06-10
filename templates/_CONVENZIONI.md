# Convenzioni della libreria template

Questo file è la legge della libreria. Ogni template (email, follow-up, risposta) e ogni prompt rispetta queste regole. Servono perché la libreria **cresce nel tempo**: senza convenzioni, dopo sei mesi hai 40 template incompatibili tra loro e merge che si rompono.

---

## 1 · Il ciclo di vita di un template (status lifecycle)

Ogni template ha uno `status` nel frontmatter. È il cuore del sistema di standardizzazione: un template non nasce "standard", lo diventa quando i dati lo provano.

| Status | Significato | Chi lo usa |
|--------|-------------|-----------|
| `draft` | Scritto, mai testato | Nessuno in produzione — solo review interna |
| `testing` | In A/B test su un segmento, volume limitato | Va in campagna ma marcato come variante sperimentale |
| `standard` | Ha vinto il test, è il default per quel framework/segmento | Default di produzione |
| `retired` | Superato da una versione migliore | Archivio — si tiene per storico, non si usa |

**La promozione `testing → standard` è l'unico modo per cambiare lo standard.** Quando una variante batte lo standard corrente su un segmento (reply rate, a parità di lista e infrastruttura), si promuove la nuova a `standard`, si manda la vecchia in `retired`, e si scrive una riga nel `_CHANGELOG.md` con il numero che ha giustificato la decisione. Mai cambiare lo standard "a sensazione" — è la stessa disciplina della §9.4 della guida (iterazione per segmento).

---

## 2 · Frontmatter obbligatorio

Ogni file template inizia con questo blocco:

```yaml
---
id: framework-2-free-work          # univoco, = nome file senza .md
tipo: email                        # email | follow-up | reply
framework: 2                       # 1-6 per le email, vuoto per reply
status: standard                   # draft | testing | standard | retired
versione: 1.0
segmento: generico                 # generico | <nome-segmento> (es. casa, cosmetica)
lingua: it
ultimo_aggiornamento: 2026-06-10
metrica: "reply rate 7.2% su 420 contatti (batch casa, mag 2026)"   # il dato che giustifica lo status
---
```

Il campo `metrica` è quello che rende la libreria un sistema e non una cartella di bozze: dice *perché* questo template è dov'è. Su un `draft` è vuoto; su uno `standard` contiene il numero che l'ha promosso.

---

## 3 · Registry delle variabili (Clay-merge-safe)

**Solo queste variabili.** Doppia graffa, snake_case, nomi esatti. Se ne serve una nuova, si aggiunge qui PRIMA di usarla in un template — così il merge da Clay/Smartlead non si rompe mai per una variabile orfana.

| Variabile | Cosa contiene | Fonte (enrichment) | Note |
|-----------|---------------|--------------------|------|
| `{{first_name}}` | Nome di battesimo | lista / `name_guard.py` | Mai cognome da solo |
| `{{company_name}}` | Nome azienda pulito | lista / `dedup_segment.py` | Senza "Srl/SpA" se suona meglio |
| `{{trigger}}` | L'aggancio personalizzato reale e specifico | `osint_enrich.py` (news, sito, Amazon) | La riga che dimostra che hai guardato davvero (§7.5) |
| `{{categoria}}` | Settore/nicchia del prospect | lista | Es. "cosmetica", "arredamento" |
| `{{proof_clienti}}` | 2-3 brand riconoscibili del tuo portfolio | manuale | **Solo con autorizzazione scritta** (§13 guida) |
| `{{case_study}}` | Caso concreto con numero | manuale | "un brand X ha fatto Y in Z mesi" |
| `{{peer_company}}` | Un competitor/pari diretto del prospect | `osint_enrich.py` | Per il framework 4 (identificazione) |
| `{{dato_segmento}}` | Dato di mercato per quel segmento | manuale / research | Es. "crescono del 40% nel primo anno" |
| `{{recent_news}}` | Notizia recente sull'azienda | `osint_enrich.py` (Google news) | Alimenta `{{trigger}}` |
| `{{competitor_touch}}` | Cosa fa un competitor che il prospect non fa | `osint_enrich.py` (Amazon) | Per il framework 5 (data-driven) |
| `{{firma}}` | Firma completa: nome, ruolo, indirizzo fisico | fisso per mailbox | CAN-SPAM richiede l'indirizzo |
| `{{calendar_link}}` | Link di booking | fisso | **MAI nelle cold** — solo nelle risposte (§7.4: no link) |

Regola d'oro: ogni variabile deve avere un **fallback** sensato nel sistema di invio. Se `{{trigger}}` è vuoto per un contatto, l'email deve restare grammaticale senza — altrimenti quel contatto si salta, non si manda monco.

---

## 4 · Spintax — la banca dei frammenti

Lo spintax (`{opzione A|opzione B|opzione C}`) va su **ogni frase**, non solo sul saluto (§7.4 guida): è ciò che impedisce ai filtri di vedere centinaia di email identiche. Frammenti riusabili, da copiare nei template:

**Saluti:** `{Buongiorno|Ciao|Salve}`
**Aperture-aggancio:** `{Ho notato|Ho visto|Mi è capitato di vedere}`
**Proposta-valore:** `{gestiamo|seguiamo|ci occupiamo di}`
**CTA soft:** `{Ha senso|Vale la pena|Avrebbe senso}` · `{parlarne|sentirci|confrontarci}` · `{15 minuti|una call breve|un confronto rapido}`
**Apertura dato:** `{Un dato rapido|Un numero|Una cosa concreta}`
**Condizionale:** `{potrebbe significare|vorrebbe dire|si tradurrebbe in}`

Regole spintax:
- Ogni opzione dentro le graffe deve essere **intercambiabile senza rompere la frase** (stessa funzione grammaticale, stesso registro).
- Minimo 2 varianti per frase, idealmente 3.
- Mai spintax dentro le variabili (`{{first_name}}` resta intatta).
- Lo spintax si espande al momento dell'invio (lo fa Smartlead/Instantly): nel template resta in chiaro.

---

## 5 · Naming dei file

- Email framework: `framework-N-nome.md` (es. `framework-2-free-work.md`)
- Follow-up: `follow-up-nome.md`
- Risposte: `reply-categoria.md` (es. `reply-objection.md`)
- Le **varianti in test** aggiungono un suffisso lettera: `framework-2-free-work-b.md` → quando vince diventa la nuova `framework-2-free-work.md` (la vecchia → `retired/`).

---

## 6 · Regole copy ereditate dalla guida (§7.4)

Valgono per ogni template, non si ripetono nei singoli file:

- Subject 1-3 parole, no punteggiatura, in spintax
- Body sotto 65-70 parole
- Prima frase interamente sul destinatario, problema prima della soluzione
- CTA singola, binaria, soft
- Plain text only — no HTML, immagini, emoji, link nelle cold
- Spintax su ogni frase
- Firma con indirizzo fisico
- Ogni script passa la checklist 10 punti (almeno 8/10) prima di entrare in `testing`
