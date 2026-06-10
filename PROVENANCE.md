# Provenienza — da dove viene ogni cosa

Questo file risponde a una domanda precisa: **quanto di questo sistema è preso dalle risorse di partenza (coldemailchris/RevGrowth) e quanto è composizione/aggiunta?** Tracciabilità riga per riga, perché un sistema di outbound vale solo se sai cosa è metodologia provata e cosa è applicazione.

Le risorse di partenza sono in `resources/`:
- `coldemailchris-tweets.md` — 8 tweet + bonus di Christian Plascencia (@coldemailchris, RevGrowth)
- `coldemailchris-youtube-corso.md` — il corso completo RevGrowth trascritto (9 moduli)

Tre livelli di provenienza:
- **🟢 SORGENTE** — preso direttamente dalle risorse (metodologia, struttura, regole, specifiche). Invariante: non si tocca.
- **🟡 APPLICAZIONE** — composizione mia che *esegue* la metodologia sorgente (es. il testo italiano degli script, calibrato sull'offer). La struttura è loro, le parole sono adattate.
- **🔵 AGGIUNTA** — layer organizzativo che NON è nelle risorse (es. il sistema di versioning). Serve a far durare il sistema nel tempo, ma non è metodologia RevGrowth.

---

## Mappa di provenienza

| Elemento del sistema | Livello | Fonte esatta |
|----------------------|---------|--------------|
| **I 6 framework email** (Lead Magnet, Free Work, Results, Pain, Data, Market Intel) | 🟢 SORGENTE | `coldemailchris-youtube-corso.md` righe 32-39 + tweet 4/6 |
| **Template più performante** (`{{first_name}} - if we...`) | 🟢 SORGENTE | `coldemailchris-youtube-corso.md` righe 42-49 (verbatim, inglese) |
| **Regole copy** (<65-70 parole, subject corto, plain text, no link/emoji) | 🟢 SORGENTE | `coldemailchris-youtube-corso.md` righe 195-204 |
| **Spintax su ogni frase** | 🟢 SORGENTE | youtube riga 184 + tweet 1 punto 5 |
| **Checklist 10 punti** (soglia 8/10) | 🟢 SORGENTE | `coldemailchris-tweets.md` righe 12-25 (tweet 1) |
| **Sequenzialità** (Day 0 / 2-3 / 5-7 / 10-14 / 18-21) | 🟢 SORGENTE | `coldemailchris-youtube-corso.md` righe 186-191 |
| **58% email 1 / 42% follow-up** | 🟢 SORGENTE | youtube righe 180-181 |
| **4-7 email, ogni follow-up un angolo nuovo** | 🟢 SORGENTE | youtube righe 179-183 |
| **Reply management** (master inbox, 4 categorie, <30 min, rispondi in minuti) | 🟢 SORGENTE | `coldemailchris-youtube-corso.md` righe 164-173 |
| **Specs prompt AI** (lunghezza, 3 tier × 3 lunghezze, elementi strutturali, variabili, guardrail) | 🟢 SORGENTE | `coldemailchris-tweets.md` righe 125-141 (BONUS, "RevGrowth's actual AI prompt specs") |
| **Frontend offer = la variabile più pesante** | 🟢 SORGENTE | youtube righe 11-13 + 53-57 |
| **Deliverability protocol** (1:1 ratio, warmup 5→20, Google>Microsoft, kill-switch) | 🟢 SORGENTE | tweet 2 (righe 29-43) + youtube 119-146 |
| **8 data source per le liste, waterfall enrichment** | 🟢 SORGENTE | tweet 7 + youtube 150-160 |
| | | |
| **Testo italiano dei 6 template** (`templates/email/*.md`) | 🟡 APPLICAZIONE | struttura = framework sorgente; parole = composizione mia, calibrata su offer Amazon |
| **Sequenza italiana con spintax** (`sequenze/sequenza-esempio-v1.md`) | 🟡 APPLICAZIONE | timing + logica = sorgente; copy italiana = mia |
| **Prompt 03 (script generation)** | 🟡→🟢 | scaffold mio, ma incorpora le specs RevGrowth **verbatim** (righe 125-141) |
| **Template 4 risposte** (`templates/reply/*.md`) | 🟡 APPLICAZIONE | le 4 categorie = sorgente (youtube 167); il testo italiano = mio |
| **Prompt 01/02/04/05** | 🟡 APPLICAZIONE | i *moduli* esistono nel corso (ICP Modeling, Offer Creation, Reply Mgmt — youtube righe 22-27), ma **il testo completo dei prompt NON è nelle risorse** → li ho scritti per eseguire quella metodologia |
| | | |
| **Status lifecycle** (draft/testing/standard/retired) | 🔵 AGGIUNTA | non in RevGrowth — layer per standardizzare nel tempo |
| **Registry variabili + banca spintax** | 🔵 AGGIUNTA | organizzativo, non metodologico |
| **I due `_CHANGELOG.md`** | 🔵 AGGIUNTA | tracciamento promozioni |
| **Pipeline OSINT open-source** (`scripts/`, waterfall a 8 step) | 🔵 AGGIUNTA | costruita su misura nel caso applicato — RevGrowth usa Clay/Apollo a pagamento, qui c'è l'equivalente open source |

---

## Nota sui prompt 01/02/04/05

Le risorse salvate contengono la **metodologia completa e le specifiche dei prompt**, ma non il testo integrale dei prompt che coldemailchris usa: il corso cita un "7-prompt process" (tweet, riga 146) e un modulo "Strategy Development via AI Prompting" (youtube riga 23) senza trascriverli. Per questo i prompt `01`, `02`, `04`, `05` sono composizione che **esegue la loro metodologia** sui moduli che il corso nomina (ICP Modeling, Offer Creation, Reply Management — youtube 22-27).

**Sono standardizzati come parte del sistema Madani v1.0.** Questo è lo standard: i quattro prompt eseguono fedelmente il metodo RevGrowth e sono i default di produzione. Non c'è un'azione pendente — la mappa qui sopra resta come record onesto di cosa è sorgente verbatim (🟢), cosa è applicazione del metodo (🟡) e cosa è layer aggiunto (🔵).

---

_Aggiornare questo file solo se si aggiunge una nuova risorsa di partenza o si ri-promuove un template/prompt sui dati di una campagna._
