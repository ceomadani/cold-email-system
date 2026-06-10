# Cold Email su Scala — Guida Operativa Completa

> Il modus operandi Madani per costruire da zero un'infrastruttura di cold email outreach su scala: scraping e arricchimento liste (tool a pagamento e open source), infrastruttura domini/mailbox, script email esatti, sequenzialità, gestione risposte, costi reali.
>
> Questa guida è self-contained: si prende, si mette in un repo GitHub, e si lancia. Metodologia: Christian Plascencia (@coldemailchris, RevGrowth/Pipeline.tech — $70M+ pipeline, 10M+ email, 1.100+ campagne in 47 verticali) + pipeline OSINT custom Madani (provata su 1.000 brand italiani → 904 decision maker → 420 contatti verificati).

---

## 0 · Il principio che governa tutto

> **"Outbound is an Offers & Targeting game, not a Copywriting game."**

La lista È la campagna. Una copy brillante moltiplica una buona lista ma non salva una lista scadente. **"Shit lead lists = shit campaign."**

Quando i numeri non vanno, si controlla in quest'ordine:

1. **Lista** — è l'ICP giusto? Email verificate?
2. **Offer** — il frontend offer ha valore reale percepito?
3. **Deliverability** — i domini sono in salute? Bounce sotto il 2%?
4. **Copy** — ultimo posto dove cercare il problema, non il primo.

---

## 1 · Architettura end-to-end

```
ICP definito
  → FASE 2: Lista (scraping aziende → contatti → email discovery → verifica)
  → FASE 1: Infrastruttura (domini → DNS → mailbox → warmup 21-28gg)   ← SI AVVIA PER PRIMA (il warmup è il collo di bottiglia)
  → FASE 3: Script (6 framework, <65 parole, spintax totale)
  → FASE 4: Sequenza (4-5 email, Day 0/3/7/12/18, angolo nuovo ogni volta)
  → FASE 5: Lancio (master inbox → reply in minuti → meeting → iterazione)
```

L'ordine di **avvio** non è l'ordine logico: l'infrastruttura va comprata e messa in warmup il giorno 1, perché servono 30-60 giorni di domain age + 21-28 giorni di warmup prima della prima email vera. La lista si costruisce in parallelo durante il warmup.

---

## 2 · La matematica della scala (perché servono TANTI domini e TANTE email)

Questi sono i vincoli fisici del cold email. Non si negoziano: violarli brucia i domini.

| Vincolo | Valore | Perché |
|---------|--------|--------|
| Invii per mailbox/giorno (steady) | **10-20** (max 25-30 assoluto) | Oltre, i provider flaggano il pattern come spam |
| Mailbox per dominio | **2-3** | Più mailbox sullo stesso dominio = stessa reputazione condivisa |
| Ratio sending : warmup reserve | **1:1** | Le mailbox si bruciano; la riserva warmata rimpiazza senza fermare la campagna (rotazione mensile) |
| Domain age pre-uso | **30-60 giorni** | Domini freschi = red flag per i filtri |
| Warmup | **21-28 giorni** | Non negoziabile, mai saltare |
| Giorni di invio (B2B) | **~22/mese** | Mai weekend |

### Tabella di dimensionamento

Calcolo con 15 email/giorno per mailbox (steady prudente) e 3 mailbox per dominio:

| Target invii/giorno | Mailbox sending | + Riserva warmup (1:1) | Mailbox totali | Domini | Email/mese (~22gg) |
|--------------------:|----------------:|-----------------------:|---------------:|-------:|-------------------:|
| 100 | 7 | 7 | 14 | 5 | ~2.200 |
| 250 | 17 | 17 | 34 | 12 | ~5.500 |
| 500 | 34 | 34 | 68 | 23 | ~11.000 |
| 1.000 | 67 | 67 | 134 | 45 | ~22.000 |
| 2.000 | 134 | 134 | 268 | 90 | ~44.000 |

Reference di produzione reale (RevGrowth): **168 sending domains, 3.000+ email account, ~1.800 email/giorno, 1 master inbox.**

Nota per chi parte: in fase pilota (≤150/giorno) la riserva 1:1 può essere ridotta al 50% per contenere i costi — ma a regime il protocollo 1:1 è quello che tiene la campagna viva quando le mailbox si disconnettono o degradano.

---

## 3 · FASE 1 — Infrastruttura

### 3.1 Domini

- **Solo `.com`** — no .io, .co, .agency (deliverability inferiore)
- **Registrar:** Porkbun (o Cloudflare) — ~$11/anno, WHOIS privacy inclusa
- **MAI il dominio principale.** Solo domini secondari dedicati
- **Pattern naming:** `trybrand.com`, `getbrand.com`, `hellobrand.com`, `brandhq.com`
- Comprare **30-60 giorni prima** dell'uso (domain age)
- Redirect 301 di ogni dominio secondario → sito principale (chi controlla il dominio deve trovare un'azienda reale)

### 3.2 DNS — record esatti

**SPF** (Google Workspace):
```
v=spf1 include:_spf.google.com ~all
```
`~all` (soft fail), NON `-all` (hard fail).

**DKIM:** chiave **2048-bit** generata da Google Admin Console → verificare `DKIM=pass` negli header di un'email di test.

**DMARC** iniziale:
```
v=DMARC1; p=none; rua=mailto:dmarc@TUODOMINIO.com; pct=100; aspf=r; adkim=r;
```
Dopo 4-6 settimane di dati puliti → passare a `p=quarantine`.

### 3.3 Mailbox

- **Google Workspace > Microsoft, sempre** (deliverability)
- 2-3 mailbox per dominio
- **Nomi reali di persone** (`mario.rossi@`) — MAI `info@`, `sales@`, `hello@`
- Foto profilo + firma completa (con indirizzo fisico — requisito CAN-SPAM) per ciascuna
- Rotazione mensile: rimpiazzare le disconnesse/degradate con la riserva, senza eccezioni

### 3.4 Warmup (NON NEGOZIABILE)

| Parametro | Valore |
|-----------|--------|
| Durata | 21-28 giorni minimo |
| Ramp | start 5/giorno, +1/giorno fino a 20 |
| Cold ramp post-warmup | di nuovo start 5/giorno, +1/giorno |
| Steady state | 10/giorno per inbox (20 se le campagne performano) |
| Warmup ongoing | in perpetuo, in parallelo alla produzione (20-30% della capacità) |
| Target nella rete di warmup | 30-50% reply rate |
| Verifica finale | inbox placement test (GlockApps / MXToolbox) — >80% inbox |

Tool: warmup built-in di Smartlead/Instantly (incluso nel piano), oppure Mailreach / Warmy / Lemwarm standalone.

---

## 4 · FASE 2 — Lista: scraping e arricchimento su scala

### 4.1 Definire l'ICP prima di scrapare

Settore, fatturato minimo, geografia, ruolo del decisore (chi firma, non chi è famoso — verificato sul campo: per un'agenzia Amazon il decisore è il **responsabile e-commerce**, non il CEO). Se l'ICP è sbagliato, tutto il resto è spreco.

### 4.2 Trovare le aziende

| Fonte | Tipo | Cosa dà |
|-------|------|---------|
| Apollo.io | Paid (free tier) | Database aziende+contatti, filtri fatturato/settore/dipendenti |
| LinkedIn Sales Navigator | Paid | Filtri fini su aziende e ruoli |
| Clay | Paid | Aggregatore multi-fonte + waterfall |
| Crunchbase / BrandNav / Storeleads | Paid | Funding, brand e-commerce, store online |
| Exa (neural search) | API | Ricerca semantica di aziende per descrizione |
| OpenCorporates / registri camerali | Free | Dati societari ufficiali |
| Apify / Zenrows + scraper custom | Paid economico | Directory di settore, marketplace, fiere |

### 4.3 Trovare i contatti (nomi + ruoli)

| Tool | Tipo | Cosa fa |
|------|------|---------|
| Apollo.io | Paid | Nome+ruolo+email in un colpo (credits) |
| **CrossLinked** | Open source | Nomi employee da LinkedIn via Google/Bing — senza credenziali LinkedIn |
| **theHarvester** | Open source | Email pubbliche indicizzate su 30+ fonti per dominio |
| Dehashed / LeakCheck | Paid economico | `@dominio.com` → tutte le email associate nei breach data → si correla nome→ruolo via LinkedIn |
| Exa + news/press | API | CEO/fondatori citati nella stampa di settore |
| **Sherlock** / **holehe** | Open source | Profili social e registrazioni piattaforme (per personalizzazione) |

### 4.4 Email discovery — la waterfall Madani (modus operandi esatto)

Mai un solo metodo. Cascata dalla fonte più economica alla più costosa, ci si ferma alla prima conferma:

```
Dominio noto
  → [1] Scraping sito aziendale (/contatti, /chi-siamo, /team)
  → [2] LinkedIn via search engine (CrossLinked, Exa)
  → [3] News/press per CEO e fondatori
  → [4] Pattern generation: nome.cognome@dominio (copre la maggioranza dei casi italiani)
        + permutazioni: n.cognome@, nome@, cognome@, nomecognome@
  → [5] SMTP RCPT TO verification (porta 25, vedi 4.5)
  → [6] holehe — conferma secondaria su domini catch-all
  → [7] Free API: Hunter.io (25/mese), Tomba.io (25/mese), EmailRep.io
  → [8] Confidence scoring composito 0-100 per ogni email
```

Equivalente "tutto a pagamento": waterfall in **Clay** (find work email → backup provider → merge → verify → master email). Stesso concetto, più costoso, zero codice.

### 4.5 Verifica — MAI saltare

- **SMTP RCPT TO:** connessione diretta al MX server → `RCPT TO:<email>` → `250` = valida, `550` = invalida. Una connessione fresca per email, mai riutilizzare.
- **Catch-all detection:** prima testare un'email palesemente finta sul dominio. Se viene accettata, il dominio è catch-all → la verifica SMTP non dice nulla → flaggare `catch-all`, non `verified`, e confermare via holehe + scraping sito + LinkedIn.
- **Verifica bulk pre-invio:** MillionVerifier o Zerobounce su TUTTA la lista prima del lancio. Target bounce atteso < 2%.
- **User-Agent nello scraping:** `curl/8.7.1` (non `Python-urllib`) per evitare i ban Cloudflare.
- **Tool self-hosted:** **Reacher** (Rust, Docker) — verifica SMTP + catch-all illimitata senza costi per credit.

### 4.6 Pulizia: dedup, segmentazione, scoring

- **Deduplica** per email E per dominio (un'azienda = un thread attivo alla volta)
- **Name guard:** filtrare i nomi-spazzatura estratti via OSINT (blocklist parole comuni, titoli di ruolo come "amministratore delegato" scambiati per nomi, nomi aziendali; min 2 / max 5 parole, ogni parola maiuscola iniziale)
- **Segmentare** per ruolo / settore / dimensione — la copy si scrive per segmento
- **Marcare lo stato:** mai contattato / contattato / risposto / meeting
- **Mai comprare liste pronte.** Bruciano il dominio. Solo email scoperte e verificate.

Script inclusi in questo repo (`scripts/`):

- `dedup_segment.py` — deduplica + segmenta un CSV di contatti (zero dipendenze, gira offline)
- `name_guard.py` — filtra i nomi-spazzatura estratti via OSINT (zero dipendenze)
- `osint_enrich.py` — enrichment OSINT da fonti free: sito aziendale, Amazon, LinkedIn, Google news
- `apollo_enrich.py` — enrichment via Apollo API (richiede `export APOLLO_API_KEY=...`)

---

## 5 · FASE 3 — Gli script email (esatti)

### 5.1 I 6 framework (@coldemailchris)

| # | Framework | Struttura | Quando |
|---|-----------|-----------|--------|
| 1 | **Lead Magnet** | "Created {Lead Magnet} for {COMPANY}" + social proof + interest CTA | Hai un asset di valore da regalare |
| 2 | **Free Work / Intro Offer** | "Interested in {Free Work} for {COMPANY}?" + P.S. social proof | Puoi offrire lavoro gratis/scontato |
| 3 | **Results-Focused** | "Interested in {Dream Result × Mechanism × Timeframe}?" + guarantee | Hai case study con numeri |
| 4 | **Pain Point** | Pain evidenziato → soluzione mirata + P.S. social proof | Conosci il problema specifico del settore |
| 5 | **Data-Driven Insight** | Dato scrapabile che mostra un weak point → soluzione | Puoi mostrare un dato che il prospect non ha |
| 6 | **Market Intelligence** | Insight di mercato unico + free work su quell'insight | Hai intelligence proprietaria |

### 5.2 Il template più performante (verbatim)

```
{{first_name}} - if we {{Offering Service FREE/discount}}
for {{company_name}} to {{achieve result}} - would you be interested?

{{Signature}}

P.S. {{Social Proof}}
```

Funziona SOLO SE: (1) il frontend offer è eccellente, (2) c'è social proof solido fuori dalla cold email.

### 5.3 Regole copy non negoziabili

- Subject: **1-3 parole**, no punteggiatura, in spintax
- Body: **sotto 65-70 parole** (bande target: 30 / 45 / 60)
- Prima frase interamente sul destinatario; problema PRIMA della soluzione
- CTA soft/value-based: "Worth a quick look?", "Ha senso parlarne?"
- **Spintax su OGNI frase** — `{Buongiorno|Ciao|Salve}` è solo l'inizio
- **Plain text ONLY** — no HTML, no immagini, no loghi, no emoji
- **No link** nelle prime email; no open tracking, no click tracking (compromettono la deliverability)
- Firma completa con indirizzo fisico (CAN-SPAM)
- P.S. = social proof

### 5.4 Checklist 10 punti — ogni script deve passarne almeno 8

1. Email < 65 parole? 2. Offer validata/di valore reale? 3. Wording rilevante per l'industria? 4. Angolo unico? 5. Ogni frase in spintax? 6. Copy allineata al targeting della lista? 7. Facile da leggere? 8. Pattern disrupt? 9. Zero filler? 10. Personalizzazione meaningful (non "ho visto il tuo LinkedIn")?

### 5.5 Struttura per generare script con AI (3 tier × 3 lunghezze)

| Tier | Parole | Struttura |
|------|--------|-----------|
| Simple | ~30 | hook + offer + CTA |
| Niche-aware | ~45 | hook + social proof + offer + CTA |
| Hyper-specific | ~60 | personalized hook + proof bridge + value prop + offer + CTA |

Elementi (almeno 3 per script): Personalized Hook (8-12 parole) · Social Proof Bridge (15-20) · Value Proposition (10-15) · Front-End Offer (8-12) · Soft CTA (5-8).
Variabili Clay-merge-safe: `{{first_name}}`, `{{company_name}}`, `{{recent_news}}`, `{{tech_stack}}`, `{{hiring_signal}}`, `{{competitor_touch}}`, `{{peer_company}}`.

### 5.6 Sequenza esempio completa (italiano, con spintax — adattare offer e proof)

Esempio reale calibrato su offer "gestione canale Amazon per brand italiani" (file completo: `sequenze/sequenza-esempio-v1.md`). Sostituire offer, proof e case study con i propri.

**Email 1 — Day 0 (Free Work / Results)**
```
{Buongiorno|Ciao} {{first_name}},

{Ho notato|Ho visto} che {{company_name}} {{trigger_personalizzato}}.

Noi {gestiamo|seguiamo} il canale Amazon per brand italiani come {{proof_clienti}} —
dal lancio alla gestione completa delle campagne.

Se vi interessa {esplorare|valutare} Amazon come canale di acquisizione
per {{company_name}}, {saresti aperto a|avrebbe senso} parlarne 15 minuti?

{{firma}}

P.S. Gestiamo l'intero processo — dal catalogo all'ottimizzazione
delle campagne — senza impegno iniziale.
```

**Email 2 — Day 3 (Data-Driven, angolo nuovo)**
```
{{first_name}},

{Un dato rapido|Un numero}: i brand italiani del {{categoria}} su Amazon
{crescono|fanno} in media {{dato_segmento}} nel primo anno con gestione professionale.

Per {{company_name}} {potrebbe significare|vorrebbe dire} un canale di acquisizione
completamente gestito da noi.

{Vale 15 minuti|Ha senso un confronto rapido} per capire se torna?
```

**Email 3 — Day 7 (Case study + offer gratuita)**
```
{{first_name}},

{Un caso concreto|Ti porto un esempio}: {{case_study_rilevante}}.

Per brand come {{company_name}} nel {{categoria}}, Amazon vale spesso
il 15-25% del fatturato online nel primo anno — senza cannibalizzare gli altri canali.

Se vuoi, {preparo|posso preparare} un'analisi gratuita del potenziale
di {{company_name}} su Amazon.
```

**Email 4 — Day 12 (Social proof forte)** — angolo: cosa ha ottenuto un peer diretto ({{peer_company}}), una frase, stessa CTA soft.

**Email 5 — Day 18-21 (Breakup)**
```
{{first_name}},

Non voglio {essere insistente|insistere} — se {{tema_offer}} non è una priorità
per {{company_name}} {in questo momento|ora}, capisco perfettamente.

Se in futuro {dovesse interessarvi|cambiasse qualcosa}, resto disponibile.
```

Regole sequenza: **ogni email un angolo NUOVO** (mai ripetere), tutte nello stesso thread, 4-5 email totali. **Il 58% delle risposte arriva dalla email 1, il 42% dai follow-up** — fermarsi alla prima lascia sul tavolo metà delle risposte.

---

## 6 · FASE 4 — Sequenzialità e regole di invio

| Step | Timing | Angolo |
|------|--------|--------|
| Email 1 | Day 0 | Hook personalizzato + offer + CTA binaria |
| Email 2 | Day 2-3 | Angolo diverso, nuovo proof point |
| Email 3 | Day 5-7 | Risorsa di valore o data insight |
| Email 4 | Day 10-14 | Social proof forte / case study |
| Email 5 | Day 18-21 | Breakup |

Regole di invio:
- Finestra **8:00-18:00 fuso del destinatario** · **mai weekend** (B2B)
- Max 25-30 invii/giorno per mailbox · delay random tra invii
- **Auto-pause su positive reply** attivo (mai follow-up a chi ha risposto)
- **Subsequence di nurture** per i non-responder: non abbandonare la lista, riciclarla dopo 60-90 giorni con offer/angolo diverso

---

## 7 · FASE 5 — Lancio e gestione

### 7.1 Pre-flight (tutte le caselle, nessuna esclusa)

- [ ] Domini con 30-60gg di età, SPF/DKIM/DMARC verificati `pass`
- [ ] Warmup completato (21-28gg) + inbox placement test > 80%
- [ ] Lista verificata bulk, bounce atteso < 2%, catch-all flaggati
- [ ] Dedup fatta (email + dominio), segmenti definiti
- [ ] Script: checklist 8/10 passata, spintax su ogni frase
- [ ] Sequenza caricata, auto-pause attivo, sending limits configurati
- [ ] Master inbox operativa, template di risposta pronti

### 7.2 Reply management

1. **Master inbox** — tutte le risposte di tutti gli account in un punto (Smartlead/Instantly built-in)
2. **Classificazione entro 30 minuti** in 4 categorie: `interested` / `objection` / `wrong timing` / `referral`
3. **Rispondere in minuti, non ore** — la velocità di risposta può raddoppiare i meeting
4. Template pre-costruiti per rispondere in <10 minuti
5. **Sales asset strategy:** creare un asset attorno all'offer, mandarlo agli interested, poi chiamare tutti quelli che l'hanno ricevuto
6. Target: **30%+ dei reply interessati → meeting**

### 7.3 Metriche e kill-switch

| Metrica | Target | Red flag | Kill switch |
|---------|--------|----------|-------------|
| Open rate | 25-45% | <20% | — |
| Reply rate | 5-10%+ | <3% | — |
| **Bounce rate** | <2% | >3% | **PAUSA immediata** |
| **Spam complaint** | <0,1% | >0,1% | **PAUSA immediata** |
| Inbox placement | >80% | <80% | Investiga |
| Meeting conversion | 30%+ | <15% | — |

Monitoring: giornaliero (bounce, soft fail, spam) · settimanale (placement test, blocklist) · mensile (Google Postmaster / Microsoft SNDS) · trimestrale (rotazione mailbox underperforming).

### 7.4 Iterazione

A/B test su subject e primo paragrafo, **per segmento**. Quando un segmento non performa: prima la lista, poi l'offer, poi la deliverability, ultima la copy (§0).

---

## 8 · COSTI

Prezzi verificati giugno 2026, arrotondati. Tre tagli di scala dalla tabella §2.

### 8.1 Costo dei componenti

| Componente | Prezzo | Note |
|------------|--------|------|
| Dominio .com (Porkbun) | ~$11/anno | WHOIS privacy inclusa |
| Mailbox Google Workspace Business Starter | $7/utente/mese (annuale; $8,40 flessibile) | Reseller autorizzati arrivano a sconti forti |
| Smartlead Base / Pro / Unlimited Smart | $39 / $94 / $174/mese | **Mailbox illimitate e warmup inclusi** in tutti i piani |
| Instantly (alternativa) Growth / Hypergrowth | ~$38 / ~$78/mese (annuale) | Warmup incluso; moduli lead DB e CRM a parte |
| Apollo.io Free / Basic / Professional | $0 / $49 / $79/mese (annuale) | Credits mensili, NON cumulabili |
| Clay Launch / Growth | $185 / $495/mese | 2.500 / 6.000 data credits; cumulabili fino a 2× (pricing marzo 2026) |
| MillionVerifier | $37/10k · ~$129-189/100k | One-off, crediti senza scadenza |
| Sales Navigator | ~$100/mese (indicativo) | Solo se serve targeting fine LinkedIn |
| Dehashed / LeakCheck | ~$20/mese (indicativo) | Discovery email per dominio via breach data |
| Reacher self-hosted | $0 (server ~$5-10/mese) | Verifica SMTP illimitata |
| CrossLinked, theHarvester, holehe, Sherlock, h8mail, emailGuesser | $0 | Open source |
| Hunter.io / Tomba.io free tier | $0 | 25 ricerche/mese ciascuno |
| GlockApps placement test | free tier / ~$59/mese | Settimanale a scala |

### 8.2 Budget per taglio di scala

**TIER PILOT — ~100 email/giorno (~2.200/mese)**
5 domini · 14 mailbox (7+7 riserva)

| Voce | Mensile |
|------|--------:|
| Google Workspace 14 × $7 | $98 |
| Smartlead Base | $39 |
| Apollo Basic | $49 |
| Verifica (MillionVerifier, ammortizzato) | ~$10 |
| **Totale ricorrente** | **~$195/mese** |
| Una tantum: 5 domini | ~$55/anno |

**TIER GROWTH — ~500 email/giorno (~11.000/mese)**
23 domini · 68 mailbox (34+34)

| Voce | Mensile |
|------|--------:|
| Google Workspace 68 × $7 | $476 |
| Smartlead Pro | $94 |
| Apollo Professional | $79 |
| Verifica ~15-20k/mese | ~$50 |
| Dehashed + extra discovery | ~$25 |
| **Totale ricorrente** | **~$725/mese** (~$66 per 1.000 email inviate) |
| Una tantum: 23 domini | ~$255/anno |
| Opzionale: Clay Launch | +$185 |

**TIER SCALE — ~2.000 email/giorno (~44.000/mese)**
90 domini · 268 mailbox (134+134)

| Voce | Mensile |
|------|--------:|
| Google Workspace 268 × $7 | $1.876 |
| Smartlead Unlimited Smart | $174 |
| Clay Growth (waterfall a scala) | $495 |
| Apollo Professional | $79 |
| Verifica ~60k/mese | ~$110 |
| GlockApps + monitoring | ~$60 |
| **Totale ricorrente** | **~$2.800/mese** (~$64 per 1.000 email inviate) |
| Una tantum: 90 domini | ~$1.000/anno |

**Dove si ottimizza a scala:** la voce dominante è sempre **le mailbox** (~65-70% del totale). Le leve: (1) reseller Google Workspace con sconto, (2) provider di mailbox dedicate per cold email a $2-4/mailbox (incluse le SmartServers nei piani alti Smartlead) — trade-off di deliverability da testare con placement test prima di migrare volumi, Google resta il gold standard; (3) sostituire i credits paid con la waterfall open source (§4.4) — costa tempo macchina invece di dollari.

**Cosa NON tagliare mai:** warmup, verifica pre-invio, riserva mailbox. Sono l'assicurazione: il costo di un dominio bruciato è ricominciare da zero con 60-90 giorni di attesa.

### 8.3 Stack minimo per partire (decisione già presa)

> Porkbun (.com) + Google Workspace + **Smartlead** (sending+warmup+master inbox) + **Apollo free/Basic** (lista) + **waterfall open source** (discovery) + **MillionVerifier** (verifica bulk) + **Reacher** se i volumi di verifica crescono.

---

## 9 · Struttura di questo repo

```
cold-email-system/
├── README.md                              ← questa guida (la mappa completa)
├── infrastruttura/
│   └── setup-checklist.md                 ← checklist domini/DNS/warmup da spuntare
├── sequenze/
│   └── sequenza-esempio-v1.md             ← sequenza completa con spintax e variabili
├── resources/
│   ├── coldemailchris-tweets.md           ← gli 8 tweet metodologici trascritti
│   ├── coldemailchris-youtube-corso.md    ← corso RevGrowth 9 moduli trascritto
│   ├── osint-tools-catalog.md             ← catalogo 100+ tool OSINT (star, lingua, URL)
│   ├── osint-full-link-dump.md            ← 373 link OSINT
│   └── links.md                           ← tutti i link: tweet, YouTube, repo, free API
└── scripts/
    ├── dedup_segment.py                   ← dedup + segmentazione CSV (zero dipendenze)
    ├── name_guard.py                      ← filtro nomi-spazzatura da OSINT
    ├── osint_enrich.py                    ← enrichment OSINT fonti free
    └── apollo_enrich.py                   ← enrichment Apollo API (env APOLLO_API_KEY)
```

---

## 10 · Riferimenti esatti

### @coldemailchris (Christian Plascencia, RevGrowth) — fonte metodologica

| # | Risorsa | URL |
|---|---------|-----|
| 1 | 10 Principles of Winning Scripts | https://x.com/coldemailchris/status/2053611305685107074 |
| 2 | Deliverability Protocol | https://x.com/coldemailchris/status/2053170063994171673 |
| 3 | B2B Content Tools | https://x.com/coldemailchris/status/2046694511028396448 |
| 4 | Free 2-Hour Course (10 moduli) | https://x.com/coldemailchris/status/2046654637131116547 |
| 5 | 2026 AI-Native Outbound Playbook | https://x.com/coldemailchris/status/2055456831905099837 |
| 6 | A-Z Guide Scale B2B (pinned) | https://x.com/coldemailchris/status/2000657580641935556 |
| 7 | Why the List IS the Campaign | https://x.com/coldemailchris/status/2054662503372845467 |
| 8 | AI Cold Email Copy Prompt (bonus) | https://x.com/coldemailchris/status/2054359491408273739 |
| — | Corso completo YouTube (9 moduli) | https://www.youtube.com/watch?v=AmnHLZG4TI8 |

Trascrizioni complete nel workspace: `email-marketing/resources/coldemailchris/` (tweet + corso YouTube).

### Materiale Madani correlato

| Risorsa | Path |
|---------|------|
| Skill canonical | `~/.claude/skills/cold-email-outreach/SKILL.md` |
| Risorse complete (18 sezioni) | `email-marketing/RISORSE-COMPLETE-EMAIL-MARKETING.md` |
| Catalogo OSINT curato (100+ tool) | `email-marketing/tools/osint-tools-catalog.md` |
| Link dump OSINT (373 link) | `email-marketing/tools/osint-full-link-dump.md` |
| Checklist infrastruttura | `email-marketing/infrastructure/setup-checklist.md` |

### Free API utili

Hunter.io (25/mese) · Tomba.io (25/mese) · EmailRep.io (illimitato) · People Data Labs (1.000 record/mese) · OpenCorporates · crt.sh

---

## 11 · Da NON fare (ognuna di queste brucia domini o campagne)

- Mai inviare senza warmup completo (21-28 giorni)
- Mai più di 25-30 email/giorno per mailbox
- Mai usare il dominio principale
- Mai comprare liste pronte
- Mai link, HTML, immagini o emoji nelle prime email
- Mai open/click tracking
- Mai "rispondi STOP" nel corpo
- Mai riutilizzare connessioni SMTP in verifica
- Mai inviare nel weekend (B2B)
- Mai ignorare bounce >3% o spam >0,1% — pausa immediata, sempre
- Mai citare brand clienti come proof senza autorizzazione scritta

---

## 12 · Timeline di lancio (countdown)

| Giorno | Azione |
|--------|--------|
| **G-60** | Compra domini, configura DNS (SPF/DKIM/DMARC), redirect 301 |
| **G-45** | Crea mailbox (nomi reali, foto, firma), collega a Smartlead |
| **G-30** | **Avvia warmup.** In parallelo: ICP, scraping aziende, contatti |
| **G-21** | Waterfall email discovery + verifica SMTP sui primi segmenti |
| **G-14** | Scrivi script (checklist 8/10), monta sequenze con spintax |
| **G-7** | Verifica bulk lista (MillionVerifier), dedup finale, segmenti freeze |
| **G-2** | Inbox placement test: >80% o non si lancia. DMARC ancora `p=none` OK |
| **G0** | Lancio con cold ramp: 5/giorno per mailbox, +1/giorno. Kill-switch attivi |
| **G+30** | Primo ciclo iterazione · valuta DMARC `p=quarantine` · rotazione mailbox |

---

_Guida compilata giugno 2026 · sistema Madani (dipartimento 4.1 Lead Generation) · metodologia @coldemailchris/RevGrowth + pipeline OSINT Madani validata su caso reale (1.000 prospect → 420 contatti verificati) · prezzi verificati giugno 2026, da ricontrollare al lancio._
