# Cold Email su Scala — Guida Operativa Completa

> Il modus operandi Madani per costruire da zero un'infrastruttura di cold email outreach su scala: scraping e arricchimento liste (tool a pagamento e open source), infrastruttura domini/mailbox, script email esatti, sequenzialità, gestione risposte, costi reali.
>
> Questa guida è self-contained: si prende, si mette in un repo GitHub, e si lancia. Metodologia: Christian Plascencia (@coldemailchris, RevGrowth/Pipeline.tech — $70M+ pipeline, 10M+ email, 1.100+ campagne in 47 verticali) + pipeline OSINT custom Madani (provata su 1.000 brand italiani → 904 decision maker → 420 contatti verificati).

---

## 0 · Come leggere questa guida

Ogni sezione segue lo stesso schema: **prima la teoria** (perché la regola esiste), **poi la pratica** (cosa fare, esattamente), **poi il ponte** (come questa sezione si aggancia alla successiva). Il cold email non è una lista di trucchi indipendenti: è **un sistema unico** in cui ogni pezzo alimenta gli altri. Se capisci le correlazioni, sai improvvisare quando qualcosa non torna. Se applichi le regole a memoria senza capirle, alla prima anomalia rompi qualcosa.

Le tre correlazioni fondamentali, che ritroverai ovunque:

1. **La qualità della lista determina la deliverability.** Una lista sporca produce bounce; i bounce distruggono la reputazione del dominio; senza reputazione nessuna email arriva — nemmeno quelle scritte bene.
2. **La deliverability determina se la copy esiste.** La migliore email del mondo, in spam, ha reply rate zero. Prima si costruisce il "diritto di consegna", poi si ottimizza il messaggio.
3. **Ogni metrica è un segnale che torna indietro.** Aperture, risposte, bounce e segnalazioni spam non misurano solo la campagna: **insegnano ai provider chi sei**. Una campagna mal gestita oggi peggiora la consegna di quella di domani.

---

## 1 · Il principio che governa tutto

> **"Outbound is an Offers & Targeting game, not a Copywriting game."**

**La teoria.** Una risposta positiva nasce dall'incrocio di tre condizioni: la persona giusta (decide su quel problema), il momento utile (il problema è attivo), un'offerta con valore percepito superiore alle alternative nella sua inbox. La copy può solo *amplificare* questo incrocio — non può crearlo. Per questo una copy mediocre su una lista perfetta produce meeting, mentre una copy brillante su una lista sbagliata produce zero: stai descrivendo benissimo una cosa che al destinatario non serve. **"Shit lead lists = shit campaign."**

C'è anche un secondo effetto, meno ovvio: i provider misurano l'engagement. Se scrivi alle persone sbagliate, nessuno apre e nessuno risponde → il provider impara che le tue email non interessano → ti declassa → anche le campagne future, su liste buone, partiranno penalizzate. **Una lista sbagliata non spreca solo questa campagna: ipoteca le prossime.**

**La pratica.** Quando i numeri non vanno, si diagnostica in quest'ordine — dal fattore con più leva a quello con meno:

1. **Lista** — è l'ICP giusto? Le email sono verificate? (§6)
2. **Offer** — il frontend offer ha valore reale percepito, o è "15 minuti per conoscerci"? (§7.1)
3. **Deliverability** — i domini sono in salute? Bounce sotto il 2%? Placement sopra l'80%? (§5, §9)
4. **Copy** — ultimo posto dove cercare il problema, non il primo. (§7)

L'errore tipico è il contrario: si riscrive la copy dieci volte mentre il vero problema è che si sta scrivendo ai CEO quando il decisore è il responsabile e-commerce (successo davvero nel caso applicato di questa guida — vedi §6.1).

**Il ponte →** se la lista è la campagna e l'engagement allena i filtri, la prima cosa da capire è *come ragionano i filtri*. È la sezione 2, e da lì discendono tutte le regole di infrastruttura.

---

## 2 · La teoria di fondo: come i filtri decidono se la tua email arriva

Tutto il protocollo di infrastruttura (§5) deriva da come Gmail e Microsoft assegnano la reputazione. Capito questo, ogni regola smette di essere arbitraria.

Il provider del destinatario valuta ogni email su due piani:

**Piano 1 — Chi la manda (reputazione del mittente).** Una specie di credit score per dominio + mailbox, costruito su:

| Segnale | Cosa misura | Regola che ne deriva |
|---------|-------------|---------------------|
| **Autenticazione** (SPF/DKIM/DMARC) | Il mittente è chi dice di essere? | DNS configurato e verificato `pass` prima di qualsiasi invio (§5.2) |
| **Età del dominio** | I domini freschi sono il pattern tipico dello spammer | Comprare i domini 30-60 giorni prima dell'uso (§5.1) |
| **Bounce rate** | Stai scrivendo a indirizzi inesistenti = lista comprata o sporca | Verifica SMTP di tutto, bounce < 2% (§6.5) |
| **Spam complaint** | I destinatari ti segnalano | Targeting giusto + opt-out facile, complaint < 0,1% (§9.3) |
| **Engagement** | Le tue email vengono aperte, lette, risposte? | Warmup prima, liste qualificate poi (§5.4, §6) |
| **Pattern di volume** | Picchi improvvisi = comportamento da bot | Ramp graduale, mai salti di volume (§5.4) |

**Piano 2 — Cosa contiene (analisi del messaggio).** Classificatori di contenuto che cercano i pattern del bulk mail:

| Pattern sospetto | Perché lo è | Regola che ne deriva |
|------------------|-------------|---------------------|
| Centinaia di email identiche | Fingerprint del bulk sending | Spintax su ogni frase: ogni email è leggermente diversa (§7.3) |
| HTML pesante, immagini, bottoni | Pattern delle promo/newsletter | Plain text only (§7.3) |
| Link nel body | Vettore phishing + ogni link è un redirect tracciabile | No link nelle prime email (§7.3) |
| Tracking pixel | Segnale di mass-mailing | No open/click tracking (§7.3) |

Tre conseguenze strategiche da fissare:

1. **La reputazione si costruisce lentamente e si distrugge in fretta.** Settimane per salire, un pomeriggio di bounce per bruciarla. E un dominio bruciato non si "ripara": si sostituisce, ricominciando da zero con 60-90 giorni di attesa. Per questo esistono i kill-switch (§9.3): fermarsi presto costa poco, recuperare è impossibile.
2. **La reputazione è per-dominio.** Per questo non si usa MAI il dominio principale: i domini secondari sono un firewall. Se uno si brucia, l'azienda non perde la propria email operativa.
3. **La quota di fiducia è per-mailbox.** Ogni casella può inviare poco senza insospettire (10-30/giorno). La scala non si ottiene alzando il volume per casella — si ottiene **in orizzontale**, moltiplicando le caselle. Da qui tutta la matematica della sezione 4.

**Il ponte →** ora che sai che la scala è orizzontale, puoi dimensionare il sistema: quanti domini e quante mailbox servono per il volume che vuoi.

---

## 3 · Architettura end-to-end

```
ICP definito
  → FASE 2: Lista (scraping aziende → contatti → email discovery → verifica)
  → FASE 1: Infrastruttura (domini → DNS → mailbox → warmup 21-28gg)   ← SI AVVIA PER PRIMA
  → FASE 3: Script (6 framework, <65 parole, spintax totale)
  → FASE 4: Sequenza (4-5 email, Day 0/3/7/12/18, angolo nuovo ogni volta)
  → FASE 5: Lancio (master inbox → reply in minuti → meeting → iterazione)
```

L'ordine di **avvio** non è l'ordine logico, ed è un punto che chi parte sbaglia quasi sempre. L'infrastruttura va comprata e messa in warmup **il giorno 1**, perché ha un tempo incomprimibile: 30-60 giorni di domain age + 21-28 giorni di warmup prima della prima email vera. La lista e gli script invece non hanno attese fisiche — si costruiscono in parallelo, *mentre* i domini maturano. Chi inverte l'ordine si ritrova con la lista pronta e due mesi di attesa davanti; chi lo rispetta arriva al giorno del lancio con tutto convergente (timeline completa in §14).

---

## 4 · La matematica della scala (perché servono TANTI domini e TANTE email)

**La teoria.** Dalla sezione 2: la quota di fiducia è per-mailbox e la reputazione è per-dominio. Quindi i vincoli sotto non sono "best practice" — sono i parametri fisici del sistema. Violarli significa attivare i segnali di volume e bounce che i filtri usano per identificare lo spam:

| Vincolo | Valore | Da quale segnale deriva (§2) |
|---------|--------|------------------------------|
| Invii per mailbox/giorno (steady) | **10-20** (max 25-30 assoluto) | Pattern di volume per-casella |
| Mailbox per dominio | **2-3** | La reputazione è condivisa a livello dominio: più caselle = più rischio concentrato |
| Ratio sending : warmup reserve | **1:1** | Le mailbox degradano; una riserva già warmata rimpiazza senza buchi di capacità |
| Domain age pre-uso | **30-60 giorni** | Segnale età dominio |
| Warmup | **21-28 giorni** | Costruzione storia di engagement |
| Giorni di invio (B2B) | **~22/mese** | Mai weekend: aperture basse → engagement medio peggiora |

Sulla riserva 1:1 vale la pena spendere una riga di teoria: le mailbox si bruciano e si disconnettono — è fisiologico, non un incidente. Senza riserva, ogni casella persa è un buco di capacità che dura i 21-28 giorni necessari a warmarne una nuova. La riserva è **magazzino di reputazione già pronta**: la rotazione mensile (sostituire le degradate, mettere le nuove in warmup) mantiene il flusso costante. È lo stesso principio delle scorte in logistica.

**La pratica.** Calcolo con 15 email/giorno per mailbox (steady prudente) e 3 mailbox per dominio:

| Target invii/giorno | Mailbox sending | + Riserva warmup (1:1) | Mailbox totali | Domini | Email/mese (~22gg) |
|--------------------:|----------------:|-----------------------:|---------------:|-------:|-------------------:|
| 100 | 7 | 7 | 14 | 5 | ~2.200 |
| 250 | 17 | 17 | 34 | 12 | ~5.500 |
| 500 | 34 | 34 | 68 | 23 | ~11.000 |
| 1.000 | 67 | 67 | 134 | 45 | ~22.000 |
| 2.000 | 134 | 134 | 268 | 90 | ~44.000 |

Reference di produzione reale (RevGrowth): **168 sending domains, 3.000+ email account, ~1.800 email/giorno, 1 master inbox, 60+ account per campagna.**

Nota per chi parte: in fase pilota (≤150/giorno) la riserva 1:1 può scendere al 50% per contenere i costi — a quel volume perdere una casella è gestibile. A regime il protocollo 1:1 è quello che tiene la campagna viva.

**Il ponte →** i numeri dicono *quanto* comprare. La sezione 5 dice *come* montarlo, pezzo per pezzo, nell'ordine giusto.

---

## 5 · FASE 1 — Infrastruttura

### 5.1 Domini

**Perché domini dedicati:** è il firewall di §2 — se la reputazione di un dominio secondario si brucia, il dominio aziendale (e l'email operativa di tutti) resta intatto. **Perché solo `.com`:** i TLD economici (.xyz, .top) e quelli "tech" (.io, .co) sono statisticamente più usati dagli spammer, e i filtri lo sanno — partono penalizzati. **Perché il redirect:** un destinatario (o un filtro) che visita il dominio deve trovare un'azienda reale, non una pagina vuota — è un check di legittimità.

Operativamente:

- **Registrar:** Porkbun (o Cloudflare) — ~$11/anno, WHOIS privacy inclusa
- **Pattern naming:** variazioni del brand — `trybrand.com`, `getbrand.com`, `hellobrand.com`, `brandhq.com`
- Comprare **30-60 giorni prima** dell'uso (domain age, §2)
- Verificare che il dominio non sia in blacklist **prima** di comprarlo (MXToolbox — i domini "usati" possono avere precedenti)
- Redirect 301 di ogni dominio secondario → sito principale

### 5.2 DNS — record esatti

**Perché:** SPF, DKIM e DMARC sono i tre protocolli con cui il destinatario verifica che l'email venga davvero da te. Senza, sei indistinguibile da uno spoofer — e i provider ormai **rifiutano** il bulk non autenticato a prescindere dal contenuto. È il prerequisito, non un'ottimizzazione.

**SPF** — dichiara quali server possono inviare per il tuo dominio:
```
Type: TXT · Name: @
v=spf1 include:_spf.google.com ~all
```
`~all` (soft fail) e NON `-all` (hard fail): con l'hard fail un errore di configurazione butta le tue email invece di flaggarle — non vuoi che il tuo primo errore DNS sia fatale.

**DKIM** — firma crittografica del contenuto: chiave **2048-bit** generata da Google Admin Console. Poi mandare un'email di test e verificare `DKIM=pass` negli header.

**DMARC** — dice al destinatario cosa fare se SPF/DKIM falliscono:
```
Type: TXT · Name: _dmarc
v=DMARC1; p=none; rua=mailto:dmarc@TUODOMINIO.com; pct=100; aspf=r; adkim=r;
```
Si parte con `p=none` (solo monitoraggio: ricevi i report senza rischiare di bloccarti da solo) e dopo 4-6 settimane di report puliti si passa a `p=quarantine`. La progressione esiste perché DMARC enforcement con un errore di setup = auto-sabotaggio.

### 5.3 Mailbox

**Perché Google > Microsoft:** deliverability verso Gmail e verso la maggior parte dei filtri B2B costantemente migliore — è la scelta di default del protocollo RevGrowth ("Google over Microsoft, every time"). **Perché nomi reali:** `info@` e `sales@` sono gli indirizzi del mass-mailing — i filtri li penalizzano e gli umani non rispondono a un reparto. Il cold email funziona quando sembra (ed è) una persona che scrive a una persona. Per la stessa ragione: foto profilo e firma completa — sono segnali di legittimità sia per i filtri sia per chi controlla chi gli ha scritto.

- Google Workspace, 2-3 mailbox per dominio
- Nomi di persone reali del team (`mario.rossi@`)
- Foto profilo + firma completa con indirizzo fisico (requisito CAN-SPAM) per ciascuna
- Rotazione mensile: le caselle disconnesse/degradate si sostituiscono con la riserva, senza eccezioni

### 5.4 Warmup (NON NEGOZIABILE)

**Perché funziona:** la rete di warmup (caselle reali collegate alla piattaforma) si scambia email che vengono aperte, risposte, spostate in primary, segnate "non è spam". Per il provider è indistinguibile da engagement genuino: in 3-4 settimane la mailbox accumula la storia di un mittente "che la gente vuole leggere". Stai letteralmente **fabbricando il track record** che i filtri richiedono. Saltarlo significa presentarsi ai filtri come un mittente nato ieri che spara volume — il profilo esatto dello spammer.

**Perché il ramp graduale:** un salto di volume è il segnale-bot di §2. Sempre +1/giorno, mai raddoppi.

| Parametro | Valore |
|-----------|--------|
| Durata | 21-28 giorni minimo |
| Ramp | start 5/giorno, +1/giorno fino a 20 |
| Cold ramp post-warmup | le email VERE ripartono da 5/giorno, +1/giorno |
| Steady state | 10/giorno per inbox (20 se le campagne performano) |
| Warmup ongoing | in perpetuo, 20-30% della capacità, in parallelo alla produzione |
| Target nella rete di warmup | 30-50% reply rate |
| Verifica finale | inbox placement test (GlockApps / MXToolbox) — >80% in inbox o non si lancia |

Attenzione al dettaglio che molti mancano: finito il warmup **non si parte a regime pieno**. Le email di produzione sono un pattern nuovo per quella casella — anche loro fanno il ramp 5/giorno +1. E il warmup non si spegne mai: continua in sottofondo per tutta la vita della casella, a mantenere il rapporto segnali-positivi/volume.

**Verifica con email di test prima del warmup:** header `SPF=pass`, `DKIM=pass`, `DMARC=pass`. Un errore DNS scoperto dopo 3 settimane di warmup = 3 settimane buttate.

### 5.5 Piano settimanale di setup

| Settimana | Attività |
|-----------|----------|
| 1 | Scegli 4-8+ variazioni dominio · registra · check blacklist MXToolbox |
| 2 | SPF + DKIM + DMARC per ogni dominio · crea mailbox (nomi reali, foto, firma) · test header `pass` |
| 3-4 | Tutte le mailbox in warmup · ramp 5→20 · monitoraggio reply rate warmup (30-50%) · **zero email di produzione** |
| 5 | Placement test per mailbox (>80%) · blocklist check · Google Postmaster attivo · se tutto OK → pronto |

**Il ponte →** mentre i domini maturano hai 4-6 settimane libere. È esattamente il tempo che serve per costruire la cosa che conta di più: la lista.

---

## 6 · FASE 2 — Lista: scraping e arricchimento su scala

### 6.1 Definire l'ICP prima di scrapare

**Perché prima:** ogni filtro che applichi a monte (settore, fatturato minimo, geografia) moltiplica la resa di tutto quello che viene dopo — enrichment, copy, reply rate. E c'è la domanda che vale più di tutte: **chi firma davvero?** Non chi è famoso in azienda, ma chi possiede il problema che risolvi.

Caso reale da questa pipeline: per un'agenzia di gestione canale Amazon, il primo batch targetizzava CEO e fondatori — 904 contatti, lista tecnicamente perfetta. **Respinta dal cliente**: il decisore vero per quell'offer è il *responsabile e-commerce*, non il CEO. Secondo batch rifatto sul ruolo giusto: 420 contatti utilizzabili. Stessa pipeline, stessa qualità di esecuzione — l'unica variabile era la definizione del decisore, e ha invalidato metà del lavoro. L'ICP si valida col cliente/owner dell'offer **prima** di lanciare lo scraping, non dopo.

### 6.2 Trovare le aziende

Due strategie complementari: i **database** (Apollo, Sales Navigator) danno volume e filtri immediati a costo di credits; le **fonti aperte** (registri, ricerca neurale, directory di settore) danno aziende che nei database non ci sono o sono stantie — a costo di tempo macchina. Su mercati locali come l'Italia le fonti aperte pesano di più, perché la copertura dei database USA-centrici è incompleta.

| Fonte | Tipo | Cosa dà |
|-------|------|---------|
| Apollo.io | Paid (free tier) | Database aziende+contatti, filtri fatturato/settore/dipendenti |
| LinkedIn Sales Navigator | Paid | Filtri fini su aziende e ruoli |
| Clay | Paid | Aggregatore multi-fonte + waterfall |
| Crunchbase / BrandNav / Storeleads | Paid | Funding, brand e-commerce, store online |
| Exa (neural search) | API | Ricerca semantica: "brand italiani di cosmetica con e-commerce proprio" |
| OpenCorporates / registri camerali | Free | Dati societari ufficiali (fatturato, sede) |
| Apify / Zenrows + scraper custom | Paid economico | Directory di settore, marketplace, espositori fiere |

In Apollo: criteri specifici + **filtri di esclusione** per keyword (tagliano i falsi positivi prima che costino credits). Ruoli target standard: Owner, Founder, C-Suite, VP, Head, Director — poi raffinati con la lezione di §6.1.

### 6.3 Trovare i contatti (nomi + ruoli)

| Tool | Tipo | Cosa fa |
|------|------|---------|
| Apollo.io | Paid | Nome+ruolo+email in un colpo (a credits) |
| **CrossLinked** | Open source | Nomi employee da LinkedIn via Google/Bing — senza credenziali LinkedIn |
| **theHarvester** | Open source | Email pubbliche indicizzate su 30+ fonti per dominio |
| Dehashed / LeakCheck | Paid economico | `@dominio.com` → tutte le email associate nei breach data → si correla nome→ruolo via LinkedIn |
| Exa + news/press | API | CEO/fondatori citati nella stampa di settore |
| **Sherlock** / **holehe** | Open source | Profili social e registrazioni piattaforme (per personalizzazione) |

Il pattern Dehashed merita una spiegazione perché è il più contro-intuitivo: i breach data contengono miliardi di indirizzi email reali. Cercando per dominio ottieni *le email che esistono davvero* in quell'azienda — incluso il formato che usano. Da lì si risale al nome, e dal nome al ruolo via LinkedIn. È discovery, non verifica: l'email trovata va comunque verificata (§6.5).

### 6.4 Email discovery — la waterfall Madani (modus operandi esatto)

**La teoria della cascata:** ogni fonte ha un costo, una copertura e un'accuratezza diversi. Se usi solo la fonte costosa, paghi anche per le email che la fonte gratuita avrebbe trovato. Se usi solo quella gratuita, perdi copertura. La cascata ordina le fonti **dalla più economica alla più costosa e si ferma alla prima conferma** — minimizzando il costo per email verificata. È lo stesso principio del waterfall enrichment di Clay, implementato con tool open source:

```
Dominio noto
  → [1] Scraping sito aziendale (/contatti, /chi-siamo, /team)
  → [2] LinkedIn via search engine (CrossLinked, Exa)
  → [3] News/press per CEO e fondatori
  → [4] Pattern generation: nome.cognome@dominio (copre la maggioranza dei casi italiani)
        + permutazioni: n.cognome@, nome@, cognome@, nomecognome@
  → [5] SMTP RCPT TO verification (porta 25, vedi 6.5)
  → [6] holehe — conferma secondaria su domini catch-all
  → [7] Free API: Hunter.io (25/mese), Tomba.io (25/mese), EmailRep.io
  → [8] Confidence scoring composito 0-100 per ogni email
```

Lo step 4 è il moltiplicatore: le aziende italiane usano in stragrande maggioranza `nome.cognome@dominio`. Se hai nome e dominio (step 1-3), puoi *generare* l'email candidata e verificarla allo step 5 — gratis — invece di comprarla. Lo scoring allo step 8 esiste perché non tutte le conferme valgono uguale: un'email trovata sul sito + verificata SMTP vale 100; un pattern generato su dominio catch-all vale molto meno, e la copy/sequenza ne deve tenere conto (i segmenti a confidence bassa si testano con volumi piccoli).

Equivalente "tutto a pagamento": waterfall in **Clay** (find work email → backup provider → merge → verify → master email). Stesso concetto, più costoso, zero codice.

### 6.5 Verifica — MAI saltare

**La teoria.** Il bounce rate è il segnale più velenoso di §2: scrivere a indirizzi inesistenti è la firma della lista comprata. Sopra il 3% i provider ti declassano in giorni. La verifica pre-invio è l'assicurazione più economica dell'intero sistema.

- **SMTP RCPT TO** — il trucco: ti connetti al mail server del destinatario e *inizi* una consegna (`RCPT TO:<email>`) senza mai completarla. Il server risponde `250` (la casella esiste) o `550` (non esiste) — hai la verità senza inviare nulla. Una connessione fresca per ogni email: i server flaggano chi testa indirizzi in raffica sulla stessa connessione.
- **Catch-all detection** — il limite strutturale del metodo: alcuni domini accettano QUALSIASI indirizzo (`asdf123@dominio` → `250`). Su questi il segnale SMTP vale zero. Si rilevano testando prima un'email palesemente finta: se passa, il dominio è catch-all → si flagga `catch-all` (non `verified`) e si conferma per altre vie — holehe (l'email è registrata su piattaforme reali = la usa un umano), scraping del sito, LinkedIn.
- **Verifica bulk pre-invio:** MillionVerifier o Zerobounce su TUTTA la lista prima del lancio, sempre — anche su email "già verificate" mesi fa: le caselle muoiono (persone che cambiano azienda). Mai esportare in piattaforma una lista non verificata.
- **Spam trap:** nei dataset comprati ci sono indirizzi-esca creati apposta per identificare gli spammer — scriverci equivale a un'autodenuncia istantanea ai blocklist provider. È la ragione definitiva per cui **le liste non si comprano**: solo email scoperte e verificate da te.
- **User-Agent nello scraping:** `curl/8.7.1` (non `Python-urllib`) per evitare i ban Cloudflare.
- **Tool self-hosted:** **Reacher** (Rust, Docker) — verifica SMTP + catch-all illimitata senza costi per credit. Conviene appena i volumi superano i ~20k/mese.

### 6.6 Pulizia: dedup, segmentazione, scoring

**Perché la dedup è per email E per dominio:** due persone della stessa azienda contattate da due sequenze diverse si parlano — e l'effetto è "questi ci stanno bombardando". Un'azienda = un thread attivo alla volta. (La dedup incrociata tra liste di fonti diverse è anche il primo problema concreto che emerge appena due pipeline si sovrappongono — successo nel caso applicato, risolto con lo script in repo.)

- **Deduplica** per email E per dominio → `scripts/dedup_segment.py`
- **Name guard:** l'OSINT estrae inevitabilmente spazzatura — titoli scambiati per nomi ("Amministratore Delegato"), nomi aziendali, parole comuni. Il filtro: blocklist 200+ parole, min 2 / max 5 parole, ogni parola con maiuscola iniziale → `scripts/name_guard.py`
- **Segmentare** per ruolo / settore / dimensione — la copy si scrive *per segmento* (§7), non per la lista intera
- **Marcare lo stato:** mai contattato / contattato / risposto / meeting — e mantenere la **suppression list** (opt-out + hard bounce): chi ha chiesto di uscire non si ricontatta MAI, per legge e per reputazione
- I ~100 account più importanti del segmento si arricchiscono **a mano**: su quelli la personalizzazione profonda ripaga

Script inclusi nel repo (`scripts/`):

- `dedup_segment.py` — deduplica + segmenta un CSV di contatti (zero dipendenze, gira offline)
- `name_guard.py` — filtra i nomi-spazzatura estratti via OSINT (zero dipendenze)
- `osint_enrich.py` — enrichment OSINT da fonti free: sito aziendale, Amazon, LinkedIn, Google news
- `apollo_enrich.py` — enrichment via Apollo API (richiede `export APOLLO_API_KEY=...`)

**Il ponte →** la lista dice A CHI scrivi e — tramite l'enrichment — ti dà anche il materiale grezzo della personalizzazione: i trigger, le news, i dati. La sezione 7 li trasforma in email.

---

## 7 · FASE 3 — Gli script email (esatti)

### 7.1 La psicologia prima dei template

Il destinatario è un decisore con l'inbox piena che processa le email in due secondi, in tre domande: *è per me? cosa vuole? mi costa qualcosa rispondere?* Tutta la struttura che segue serve a far passare queste tre domande:

- **Brevità (<65 parole):** email tra 50 e 125 parole ottengono ~2,4× le risposte rispetto a 200+. Non perché la gente sia pigra: perché la brevità *segnala rispetto del tempo* e si legge per intero su mobile.
- **Prima frase sul destinatario:** se la prima riga parla di te, hai risposto "non è per me" alla domanda 1. Il problema prima della soluzione: la rilevanza si dimostra mostrando di conoscere il suo contesto, non elencando i tuoi servizi.
- **CTA binaria e soft** ("Ha senso parlarne?"): rispondere "sì" a una domanda costa meno che "trovare 30 minuti per una demo". Si abbassa il costo della risposta, non l'ambizione del funnel.
- **P.S. con social proof:** il P.S. è la riga più letta dopo l'oggetto — ci va la prova, non un saluto.
- **Il frontend offer è la variabile più pesante** (è il "Offers game" di §1): una componente del servizio gratis o fortemente scontata, un free trial, un'analisi fatta su misura. "15 minuti per conoscerci" non è un'offer — è una richiesta di tempo senza contropartita.

### 7.2 I 6 framework (@coldemailchris)

Sei modi diversi di costruire la stessa cosa: valore percepito nei primi due secondi. Si sceglie in base a cosa hai *davvero* in mano — l'asset, il case study, il dato:

| # | Framework | Struttura | Quando usarlo |
|---|-----------|-----------|---------------|
| 1 | **Lead Magnet** | "Created {Lead Magnet} for {COMPANY}" + social proof + interest CTA | Hai un asset di valore già pronto da regalare |
| 2 | **Free Work / Intro Offer** | "Interested in {Free Work} for {COMPANY}?" + P.S. social proof | Puoi permetterti lavoro gratis/scontato come acquisizione |
| 3 | **Results-Focused** | "Interested in {Dream Result × Mechanism × Timeframe}?" + guarantee | Hai case study con numeri veri |
| 4 | **Pain Point** | Pain evidenziato → soluzione mirata + P.S. social proof | Conosci il problema specifico del segmento |
| 5 | **Data-Driven Insight** | Dato scrapabile che mostra un weak point → soluzione | Puoi mostrare al prospect un dato che non ha |
| 6 | **Market Intelligence** | Insight di mercato unico + free work su quell'insight | Hai intelligence proprietaria del settore |

I framework 5 e 6 sono i più potenti quando l'enrichment è buono — usano i dati raccolti in §6 come leva ("ho guardato il vostro catalogo: 12 competitor della categoria sono su Amazon, voi no").

### 7.3 Il template più performante (verbatim)

```
{{first_name}} - if we {{Offering Service FREE/discount}}
for {{company_name}} to {{achieve result}} - would you be interested?

{{Signature}}

P.S. {{Social Proof}}
```

Sembra troppo semplice per funzionare — funziona *perché* è semplice: una domanda binaria con un'offer concreta dentro, zero attrito. Ma SOLO SE (1) il frontend offer è eccellente e (2) c'è social proof solido fuori dalla cold email. È la dimostrazione pratica di §1: il template vincente non ha copy — ha un'offerta.

### 7.4 Regole copy non negoziabili

Ognuna deriva o dai filtri (§2) o dalla psicologia (§7.1):

- Subject: **1-3 parole**, no punteggiatura, in spintax — un collega ti scrive "fattura marzo", non "Opportunità imperdibile per la vostra azienda!"
- Body: **sotto 65-70 parole** (bande target: 30 / 45 / 60)
- Prima frase interamente sul destinatario; problema PRIMA della soluzione
- CTA soft/value-based: "Worth a quick look?", "Ha senso parlarne?"
- **Spintax su OGNI frase** — `{Buongiorno|Ciao|Salve}` è solo l'inizio: ogni frase deve avere varianti, così nessuna coppia di email inviate è identica (anti-fingerprint, §2)
- **Plain text ONLY** — no HTML, no immagini, no loghi, no emoji (anti-classificatore promo, §2)
- **No link** nelle prime email; no open tracking, no click tracking (§2)
- Firma completa con indirizzo fisico (CAN-SPAM)
- P.S. = social proof

### 7.5 Checklist 10 punti — ogni script deve passarne almeno 8

1. Email < 65 parole? 2. Offer validata/di valore reale? 3. Wording rilevante per l'industria? 4. Angolo unico? 5. Ogni frase in spintax? 6. Copy allineata al targeting della lista? 7. Facile da leggere? 8. Pattern disrupt? 9. Zero filler? 10. Personalizzazione meaningful (non "ho visto il tuo LinkedIn")?

Sul punto 10, la regola pratica: la personalizzazione vera è un dato che **non potresti avere senza aver guardato davvero** — il listing Amazon assente, il lancio di prodotto della settimana scorsa, il competitor che domina la categoria. "Ho visto il tuo profilo LinkedIn" è personalizzazione finta: lo dice anche il bot, e il destinatario lo sa.

### 7.6 Struttura per generare script con AI (3 tier × 3 lunghezze)

La profondità di personalizzazione si paga (in enrichment e in tempo), quindi si calibra sul valore del segmento: tier semplice per la coda lunga, hyper-specific per i ~100 account che contano.

| Tier | Parole | Struttura |
|------|--------|-----------|
| Simple | ~30 | hook + offer + CTA |
| Niche-aware | ~45 | hook + social proof + offer + CTA |
| Hyper-specific | ~60 | personalized hook + proof bridge + value prop + offer + CTA |

Elementi (almeno 3 per script): Personalized Hook (8-12 parole) · Social Proof Bridge (15-20) · Value Proposition (10-15) · Front-End Offer (8-12) · Soft CTA (5-8).
Variabili Clay-merge-safe: `{{first_name}}`, `{{company_name}}`, `{{recent_news}}`, `{{tech_stack}}`, `{{hiring_signal}}`, `{{competitor_touch}}`, `{{peer_company}}`.

### 7.7 Sequenza esempio completa (italiano, con spintax — adattare offer e proof)

Esempio reale calibrato su offer "gestione canale Amazon per brand italiani" (file completo: `sequenze/sequenza-esempio-v1.md`). Sostituire offer, proof e case study con i propri. Nota come ogni email usa un framework diverso di §7.2 — è questo che rende la sequenza una *progressione* e non una ripetizione.

**Email 1 — Day 0 (framework 2, Free Work / Results)** — il primo contatto porta subito l'offer:
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

**Email 2 — Day 3 (framework 5, Data-Driven)** — angolo nuovo: non "ti sollecito", ma un dato che lui non ha:
```
{{first_name}},

{Un dato rapido|Un numero}: i brand italiani del {{categoria}} su Amazon
{crescono|fanno} in media {{dato_segmento}} nel primo anno con gestione professionale.

Per {{company_name}} {potrebbe significare|vorrebbe dire} un canale di acquisizione
completamente gestito da noi.

{Vale 15 minuti|Ha senso un confronto rapido} per capire se torna?
```

**Email 3 — Day 7 (framework 3, Results + offer gratuita)** — il case study concreto, più un'offer che abbassa ancora l'attrito:
```
{{first_name}},

{Un caso concreto|Ti porto un esempio}: {{case_study_rilevante}}.

Per brand come {{company_name}} nel {{categoria}}, Amazon vale spesso
il 15-25% del fatturato online nel primo anno — senza cannibalizzare gli altri canali.

Se vuoi, {preparo|posso preparare} un'analisi gratuita del potenziale
di {{company_name}} su Amazon.
```

**Email 4 — Day 12 (framework 4, social proof forte)** — cosa ha ottenuto un peer diretto ({{peer_company}}): una frase, stessa CTA soft. Il peer del suo stesso settore vale più di un case study generico — l'identificazione fa metà del lavoro.

**Email 5 — Day 18-21 (Breakup)** — chiusura elegante:
```
{{first_name}},

Non voglio {essere insistente|insistere} — se {{tema_offer}} non è una priorità
per {{company_name}} {in questo momento|ora}, capisco perfettamente.

Se in futuro {dovesse interessarvi|cambiasse qualcosa}, resto disponibile.
```
Il breakup funziona per un motivo preciso: togliere la disponibilità attiva la loss aversion ("ultima chiamata") e insieme dimostra che non sei lo spammer che insisterà per sempre — è l'email che sblocca più risposte "in realtà sì, parliamone" di quanto ci si aspetti.

### 7.8 La libreria che si standardizza nel tempo

Gli script qui sopra non sono un set fisso da copiare una volta: sono il punto di partenza di una **libreria viva** che migliora ad ogni campagna. È la differenza tra "ho un template" e "ho un sistema che converge sul template migliore".

Il meccanismo è uno status lifecycle per ogni template (email, follow-up, risposta) e per ogni prompt AI:

| Status | Significato |
|--------|-------------|
| `draft` | Scritto, mai testato |
| `testing` | In A/B su un segmento, volume limitato |
| `standard` | Ha vinto il test — è il default per quello slot |
| `retired` | Superato da una versione migliore |

La regola che rende il tutto un sistema e non una cartella di bozze: **lo standard si cambia solo coi dati, mai a sensazione.** Quando una variante batte lo standard su un segmento (reply rate, a parità di lista e infrastruttura), si promuove la nuova a `standard`, la vecchia va in `retired`, e si scrive una riga nel changelog **con il numero che ha giustificato la decisione**. È la stessa disciplina dell'iterazione per segmento (§9.4), applicata agli asset.

Tre pezzi tengono insieme la libreria nel tempo:

- **Registry delle variabili** — un set chiuso di variabili Clay-merge-safe (`{{first_name}}`, `{{company_name}}`, `{{trigger}}`, …). Se ne serve una nuova, si aggiunge al registry *prima* di usarla, così il merge non si rompe mai per una variabile orfana.
- **Banca dello spintax** — frammenti riusabili (`{Buongiorno|Ciao|Salve}`, `{Ha senso|Vale la pena}`…), perché lo spintax deve stare su ogni frase (§7.4) e riscriverlo ogni volta è spreco.
- **Changelog** — il diario delle promozioni: tra sei mesi, alla domanda "perché usiamo questa versione?", la risposta è scritta.

Nel repo (§11) questo vive in `templates/` (i 6 framework + breakup + le 4 risposte + nurture, ognuno col suo frontmatter di status) e `prompts/` (la pipeline AI: ICP → offer → script → personalizzazione → classificazione risposte). La legge della libreria è `templates/_CONVENZIONI.md`.

**Il ponte →** le email ci sono. Ma una email sola — anche perfetta — lascia sul tavolo quasi metà dei risultati. I numeri nella sezione 8.

---

## 8 · FASE 4 — Sequenzialità e regole di invio

**La teoria.** **Il 58% delle risposte arriva dalla email 1, il 42% dai follow-up.** Chi si ferma alla prima email paga il costo pieno della lista e dell'infrastruttura e incassa poco più di metà del risultato possibile. Ma il follow-up che funziona NON è un sollecito ("hai visto la mia email?" = rumore): ogni step porta **un angolo nuovo** — un dato, un caso, una prospettiva diversa. La teoria è semplice: non sai *quale* leva muove quel decisore (il dato? il peer? la paura di restare indietro?), quindi la sequenza le prova tutte, una per email. Stesso thread, così il contesto si accumula e la quarta email si legge col beneficio delle prime tre.

| Step | Timing | Angolo |
|------|--------|--------|
| Email 1 | Day 0 | Hook personalizzato + offer + CTA binaria |
| Email 2 | Day 2-3 | Angolo diverso, nuovo proof point |
| Email 3 | Day 5-7 | Risorsa di valore o data insight |
| Email 4 | Day 10-14 | Social proof forte / case study |
| Email 5 | Day 18-21 | Breakup |

Il timing si allarga progressivamente (2-3 giorni → 5-7 → 10-14): pressione percepita decrescente mentre la sequenza avanza — l'opposto del nagging.

Regole di invio:

- Finestra **8:00-18:00 fuso del destinatario** · **mai weekend** (B2B): email lette = engagement; email sepolte sotto la pila del lunedì = silenzio che pesa sulla reputazione
- Max 25-30 invii/giorno per mailbox · delay random tra invii (il ritmo umano non è un metronomo)
- **Auto-pause su positive reply** — obbligatorio: il follow-up automatico a chi ha già risposto è il singolo errore più costoso in credibilità
- **Subsequence di nurture** per i non-responder: la lista non si butta — si ricicla dopo 60-90 giorni con offer/angolo diverso. Il "no" di marzo è spesso un "non ora": il costo di riprovarci è zero, la lista l'hai già pagata

**Il ponte →** la sequenza genera risposte. Da qui in poi il collo di bottiglia cambia natura: non più consegnare email, ma **convertire risposte in meeting** — ed è una questione di minuti, non di giorni.

---

## 9 · FASE 5 — Lancio e gestione

### 9.1 Pre-flight (tutte le caselle, nessuna esclusa)

Ogni voce copre un modo specifico di bruciare il sistema al lancio:

- Domini con 30-60gg di età, SPF/DKIM/DMARC verificati `pass`
- Warmup completato (21-28gg) + inbox placement test > 80%
- Lista verificata bulk, bounce atteso < 2%, catch-all flaggati
- Dedup fatta (email + dominio), segmenti definiti, suppression list attiva
- Script: checklist 8/10 passata, spintax su ogni frase
- Sequenza caricata, auto-pause attivo, sending limits configurati
- Master inbox operativa, template di risposta pronti

### 9.2 Reply management

**La teoria della velocità:** chi risponde a una cold email è *in quel momento* nel suo picco di interesse — ha il problema in mente, ha la tua email davanti. Ogni ora che passa, il contesto evapora: arriva la riunione, l'urgenza, il weekend. Rispondere in minuti invece che in ore **può raddoppiare i meeting** dalla stessa quantità di reply. È il moltiplicatore più economico dell'intero sistema: non richiede più domini, più lista, più copy — solo organizzazione.

1. **Master inbox** — tutte le risposte di tutti gli account in un punto (Smartlead/Instantly built-in). Con 60+ caselle per campagna, senza master inbox le risposte si perdono fisicamente
2. **Classificazione entro 30 minuti** in 4 categorie: `interested` / `objection` / `wrong timing` / `referral` — ogni categoria ha la sua azione: interested → proposta slot subito; objection → template di gestione; wrong timing → subsequence con reminder; referral → nuova sequenza sulla persona giusta
3. **Rispondere in minuti, non ore** — template pre-costruiti per stare sotto i 10 minuti
4. **Sales asset strategy:** creare un asset attorno all'offer (analisi, report, demo), mandarlo agli interested, poi chiamare tutti quelli che l'hanno ricevuto — l'asset dà la ragione legittima per la chiamata
5. Target: **30%+ dei reply interessati → meeting**

### 9.3 Metriche e kill-switch

**La teoria:** le metriche hanno due funzioni diverse, non confonderle. Bounce e spam complaint sono **allarmi di reputazione** (§2): quando scattano non stai "performando male" — ti stai facendo male in modo permanente, e ogni email in più aggrava il danno. Per questo il kill-switch è automatico e senza appello. Open/reply/meeting sono invece **metriche di ottimizzazione**: si leggono nel tempo, per segmento, e guidano l'iterazione.

| Metrica | Target | Red flag | Kill switch |
|---------|--------|----------|-------------|
| Open rate | 25-45% | <20% | — |
| Reply rate | 5-10%+ | <3% | — |
| **Bounce rate** | <2% | >3% | **PAUSA immediata** |
| **Spam complaint** | <0,1% | >0,1% | **PAUSA immediata** |
| Inbox placement | >80% | <80% | Investiga |
| Meeting conversion | 30%+ | <15% | — |

Monitoring: giornaliero (bounce, soft fail, spam) · settimanale (placement test, blocklist) · mensile (Google Postmaster / Microsoft SNDS) · trimestrale (rotazione mailbox underperforming).

### 9.4 Iterazione

A/B test su subject e primo paragrafo, **per segmento** — un test sulla lista intera mischia segnali di segmenti diversi e non impari niente. E quando un segmento non performa, si torna alla diagnosi di §1, nell'ordine: prima la lista, poi l'offer, poi la deliverability, ultima la copy. Il sistema è un loop: le metriche di questa campagna sono l'input della prossima.

**Il ponte →** il sistema è completo. Restano due domande pratiche: quanto costa (sezione 10) e dove sta il materiale (sezione 11).

---

## 10 · COSTI

Prezzi verificati giugno 2026, arrotondati. Tre tagli di scala dalla tabella §4.

**La struttura del costo, prima dei numeri:** la voce dominante è sempre **le mailbox** (~65-70% del totale a regime) — conseguenza diretta della scala orizzontale di §2: il volume si compra a caselle, non a banda. I software (sending, enrichment, verifica) crescono a gradini molto più lenti. Implicazione: l'ottimizzazione dei costi si fa sulle mailbox, e mai tagliando le assicurazioni (warmup, verifica, riserva).

### 10.1 Costo dei componenti

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

### 10.2 Budget per taglio di scala

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

**Dove si ottimizza a scala:** (1) reseller Google Workspace con sconto, (2) provider di mailbox dedicate per cold email a $2-4/mailbox (incluse le SmartServers nei piani alti Smartlead) — trade-off di deliverability da testare con placement test prima di migrare volumi, Google resta il gold standard; (3) sostituire i credits paid con la waterfall open source (§6.4) — costa tempo macchina invece di dollari.

**Cosa NON tagliare mai:** warmup, verifica pre-invio, riserva mailbox. Sono l'assicurazione: il costo di un dominio bruciato è ricominciare da zero con 60-90 giorni di attesa (§2) — nessun risparmio mensile lo ripaga.

### 10.3 Stack minimo per partire (decisione già presa)

> Porkbun (.com) + Google Workspace + **Smartlead** (sending+warmup+master inbox) + **Apollo free/Basic** (lista) + **waterfall open source** (discovery) + **MillionVerifier** (verifica bulk) + **Reacher** se i volumi di verifica crescono.

---

## 11 · Il repo GitHub

**`github.com/ceomadani/cold-email-system`** — questa guida è il README; tutto il materiale operativo è incluso:

```
cold-email-system/
├── README.md                              ← questa guida (la mappa completa)
├── infrastruttura/
│   └── setup-checklist.md                 ← checklist domini/DNS/warmup da spuntare
├── templates/                             ← LIBRERIA VIVA (§7.8) — versionata per status
│   ├── _CONVENZIONI.md                    ← la legge: status, variabili, spintax, naming
│   ├── _CHANGELOG.md                      ← diario delle promozioni a standard
│   ├── email/                             ← i 6 framework + breakup (ognuno col suo status)
│   ├── follow-up/                         ← subsequence di nurture (riciclo 60-90gg)
│   └── reply/                             ← le 4 categorie di reply management + opt-out
├── prompts/                               ← pipeline AI versionata
│   ├── 01-icp-research.md                 ← ICP + decisore
│   ├── 02-offer-creation.md               ← frontend offer
│   ├── 03-script-generation.md           ← script 3 tier × 3 lunghezze (specs RevGrowth)
│   ├── 04-personalization.md             ← riga {{trigger}} da enrichment
│   ├── 05-reply-classification.md        ← classifica risposte → bozza
│   └── _CHANGELOG.md
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

Il `.gitignore` esclude CSV/JSON (liste e PII non si committano mai) e credenziali.

---

## 12 · Riferimenti esatti

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

Trascrizioni complete in `resources/`.

### Materiale Madani correlato

| Risorsa | Path |
|---------|------|
| **Repo GitHub deployabile** | `github.com/ceomadani/cold-email-system` |
| Skill canonical | `~/.claude/skills/cold-email-outreach/SKILL.md` |
| Risorse complete (18 sezioni) | `email-marketing/RISORSE-COMPLETE-EMAIL-MARKETING.md` |
| Catalogo OSINT curato (100+ tool) | `email-marketing/tools/osint-tools-catalog.md` |
| Link dump OSINT (373 link) | `email-marketing/tools/osint-full-link-dump.md` |
| Checklist infrastruttura | `email-marketing/infrastructure/setup-checklist.md` |

### Free API utili

Hunter.io (25/mese) · Tomba.io (25/mese) · EmailRep.io (illimitato) · People Data Labs (1.000 record/mese) · OpenCorporates · crt.sh

---

## 13 · Da NON fare (e perché — ognuna brucia domini o campagne)

- **Mai inviare senza warmup completo** (21-28 giorni) — mittente senza storia + volume = profilo esatto dello spammer (§5.4)
- **Mai più di 25-30 email/giorno per mailbox** — oltre la quota di fiducia scatta il pattern di volume (§2)
- **Mai usare il dominio principale** — è il firewall: se brucia un secondario, l'azienda continua a esistere (§5.1)
- **Mai comprare liste pronte** — bounce alti + spam trap = autodenuncia ai blocklist (§6.5)
- **Mai link, HTML, immagini o emoji nelle prime email** — pattern del bulk per i classificatori (§2)
- **Mai open/click tracking** — i pixel/redirect sono segnali di mass-mailing (§2)
- **Mai "rispondi STOP" nel corpo** — è linguaggio da spammer; chi vuole uscire lo scrive da solo
- **Mai riutilizzare connessioni SMTP in verifica** — i mail server bannano chi testa indirizzi in raffica (§6.5)
- **Mai inviare nel weekend (B2B)** — email sepolte = engagement a picco (§8)
- **Mai ignorare bounce >3% o spam >0,1%** — il danno di reputazione è permanente, la pausa è gratis (§9.3)
- **Mai citare brand clienti come proof senza autorizzazione scritta** — il danno legale/commerciale supera qualsiasi beneficio di copy

---

## 14 · Timeline di lancio (countdown)

La timeline incrocia i due binari di §3: l'infrastruttura (che ha tempi fisici incomprimibili) e la lista (che si costruisce in parallelo). Ogni riga dipende dalla precedente.

| Giorno | Azione |
|--------|--------|
| **G-60** | Compra domini, configura DNS (SPF/DKIM/DMARC), redirect 301 — da qui parte il timer della domain age |
| **G-45** | Crea mailbox (nomi reali, foto, firma), collega a Smartlead, test header `pass` |
| **G-30** | **Avvia warmup.** In parallelo: ICP validato con l'owner dell'offer, scraping aziende, contatti |
| **G-21** | Waterfall email discovery + verifica SMTP sui primi segmenti |
| **G-14** | Scrivi script (checklist 8/10), monta sequenze con spintax |
| **G-7** | Verifica bulk lista (MillionVerifier), dedup finale, segmenti freeze |
| **G-2** | Inbox placement test: >80% o non si lancia. DMARC ancora `p=none` OK |
| **G0** | Lancio con cold ramp: 5/giorno per mailbox, +1/giorno. Kill-switch attivi |
| **G+30** | Primo ciclo iterazione per segmento · valuta DMARC `p=quarantine` · rotazione mailbox |

---

_Guida compilata giugno 2026 · sistema Madani (dipartimento 4.1 Lead Generation) · metodologia @coldemailchris/RevGrowth + pipeline OSINT Madani validata su caso reale (1.000 prospect → 420 contatti verificati) · prezzi verificati giugno 2026, da ricontrollare al lancio._
