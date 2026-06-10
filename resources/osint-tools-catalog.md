# OSINT & Cold Email Tools Catalog (May 2026)

## Email Verification

| Tool | Stars | Language | Cosa fa | URL |
|------|-------|----------|---------|-----|
| **Reacher** | 8,707 | Rust | Full-stack verification senza inviare email. Syntax + DNS + SMTP + catch-all + disposable. Self-hostable Docker. | https://github.com/reacherhq/check-if-email-exists |
| **AfterShip/email-verifier** | 1,565 | Go | Libreria Go: syntax, MX, SMTP, disposable, free email, role-based, catch-all | https://github.com/AfterShip/email-verifier |
| **Trumail** | 1,050 | Go | Validation/verification come client library + API + Docker | https://github.com/trumail/trumail |
| **validate-emails** | 94 | Python | Waterfall verifier — cascade through multiple commercial APIs | https://github.com/centminmod/validate-emails |

## Email Discovery

| Tool | Stars | Language | Cosa fa | URL |
|------|-------|----------|---------|-----|
| **theHarvester** | 16,216 | Python | OSINT standard. 30+ fonti (Google, Bing, PGP, Shodan, crt.sh) | https://github.com/laramies/theHarvester |
| **EmailFinder** | 419 | Python | Business email da dominio via search engines | https://github.com/Josue87/EmailFinder |
| **emailGuesser** | 154 | Python | Permutazioni nome+dominio + validazione | https://github.com/WhiteHatInspector/emailGuesser |
| **Email-Permutator** | 32 | JS | Permutazioni + validazione vs O365, GitHub commits, HIBP | https://github.com/emeth-/Email-Permutator |

## Email OSINT

| Tool | Stars | Language | Cosa fa | URL |
|------|-------|----------|---------|-----|
| **holehe** | 10,947 | Python | Check email su 120+ piattaforme (password reset abuse) | https://github.com/megadose/holehe |
| **h8mail** | 4,983 | Python | Breach hunting + linked email discovery | https://github.com/khast3x/h8mail |
| **Buster** | 1,309 | Python | Recon: permutazione + verification + enrichment | https://github.com/sham00n/buster |

## LinkedIn Scraping (senza API)

| Tool | Stars | Language | Cosa fa | URL |
|------|-------|----------|---------|-----|
| **linkedin_scraper** | 4,123 | Python | Scraping profili + company pages (Selenium) | https://github.com/joeyism/linkedin_scraper |
| **linkedin2username** | 1,690 | Python | Genera username lists da employee LinkedIn | https://github.com/initstring/linkedin2username |
| **CrossLinked** | 1,531 | Python | Enumeration via search engines (NO LinkedIn creds) | https://github.com/m8sec/CrossLinked |
| **ScrapedIn** | 1,219 | Python | Scraping LinkedIn senza API | https://github.com/dchrastil/ScrapedIn |

## Social/Username OSINT

| Tool | Stars | Language | Cosa fa | URL |
|------|-------|----------|---------|-----|
| **Sherlock** | 83,376 | Python | Username su 300+ social networks | https://github.com/sherlock-project/sherlock |

## Mail Server Self-Hosted

| Tool | Stars | Language | Cosa fa | URL |
|------|-------|----------|---------|-----|
| **Docker-Mailserver** | 18,233 | Shell | Full mail server in Docker (SMTP+IMAP+SPF/DKIM/DMARC) | https://github.com/docker-mailserver/docker-mailserver |
| **BillionMail** | 14,780 | Go | Mail server + newsletter + email marketing. 8-min install | https://github.com/Billionmail/BillionMail |
| **Mautic** | 9,679 | PHP | Full marketing automation (CRM + campaigns + analytics) | https://github.com/mautic/mautic |
| **Mailu** | 7,209 | Python | Full mail server come Docker images | https://github.com/Mailu/Mailu |
| **Mox** | 5,682 | Go | Modern lean mail server, auto TLS | https://github.com/mjl-/mox |

## Sending & Sequences

| Tool | Stars | Language | Cosa fa | URL |
|------|-------|----------|---------|-----|
| **Listmonk** | 20,087 | Go | Newsletter/mailing list. Multi-SMTP, rate limiting, SQL segmentation | https://github.com/knadh/listmonk |
| **Email-automation** | 147 | JS | Cold email outreach — schedule, personalize, send | https://github.com/PaulleDemon/Email-automation |

## Warmup

| Tool | Stars | Language | Cosa fa | URL |
|------|-------|----------|---------|-----|
| **WKL-Sec/Warmer** | 89 | Python | Selenium warmup automatico tra account | https://github.com/WKL-Sec/Warmer |

## Enrichment AI

| Tool | Stars | Language | Cosa fa | URL |
|------|-------|----------|---------|-----|
| **Fire Enrich** | 1,178 | TS | AI agents per company data, funding, tech stack, leadership | https://github.com/firecrawl/fire-enrich |
| **OpenClay** | early | TS | Clay.com clone open-source con BYO API keys | https://github.com/rahuldotbiz/openclay |

## Monitoring

| Tool | Stars | Language | Cosa fa | URL |
|------|-------|----------|---------|-----|
| **parsedmarc** | 1,239 | Python | Parsing DMARC aggregate/forensic reports + Elasticsearch/Grafana | https://github.com/domainaware/parsedmarc |

---

## Clearnet OSINT Platforms & Services

### Breach & Leak Databases (clearnet)

| Piattaforma | URL | Note |
|-------------|-----|------|
| **Dehashed** | https://www.dehashed.com/ | Nour ha API key pagata. Cerca per dominio (@company.com) → trova email associate + password hash + nomi |
| **LeakCheck** | https://leakcheck.io/ | Breach lookup per email/username/dominio |
| **BreachDirectory** | https://breachdirectory.org/ | Free breach search |
| **WeLeakInfo** | https://weleakinfo.io/ | Aggregatore breach data |
| **LibraryOfLeaks** | https://search.libraryofleaks.org | Ricerca leak |
| **LeakRadar** | https://leakradar.io/ | Monitoring leak |
| **Leak-Lookup** | https://leak-lookup.com/ | Lookup per email/username |
| **Leaked.domains** | https://leaked.domains/ | Cerca per dominio |
| **OffshoreLeaks (ICIJ)** | https://offshoreleaks.icij.org/ | Panama/Paradise Papers — company ownership |
| **ScamSearch** | https://scamsearch.io/ | Scam/fraud database |
| **LeakIX** | https://leakix.net/ | Exposed services + data leaks |
| **HIBP** | https://haveibeenpwned.com | Check se email è in breach note |
| **CyberNews Leak Checker** | https://cybernews.com/personal-data-leak-check/ | Check personale |

### Email Discovery & Verification (clearnet)

| Piattaforma | URL | Note |
|-------------|-----|------|
| **Epieos** | https://epieos.com/ | Email → Google account, social, registrazioni |
| **Snov.io** | https://snov.io/email-finder | Email finder per dominio/nome |
| **Hunter.io** | https://hunter.io/email-verifier | 25 ricerche/mese free. Domain search + verifica |
| **Phonebook.cz** | https://phonebook.cz/ | Email + dominio + URL lookup |
| **EmailRep.io** | https://emailrep.io/ | Reputation score email |
| **osint.sh Email** | https://osint.sh/email/ | Email finder |
| **AnyMailFinder** | https://anymailfinder.com/ | Business email discovery |
| **FindEmail.io** | https://findemail.io/ | Email finder |
| **SimpleMail** | https://www.simplemail.dev/ | Email lookup |
| **Predicta Search** | https://predictasearch.com | Predictive email search |
| **Verify-Email** | https://verify-email.org/ | Verifica email |
| **Email Dossier** | https://centralops.net/co/emaildossier.aspx | Analisi completa email |
| **Email Format** | https://www.email-format.com/ | Pattern email per azienda |
| **Email Permutator** | http://metricsparrow.com/toolkit/email-permutator/ | Genera combinazioni nome+dominio |
| **Email Permutator+** | https://www.polished.app/email-permutator/ | Versione estesa |
| **Email Breach Analysis** | https://www.hotsheet.com/inoitsu/ | Analisi breach per email |
| **Reverse Whois** | https://osint.sh/reversewhois/ | Reverse WHOIS lookup |
| **Clearbit** | https://dashboard.clearbit.com/lookup | Company + person enrichment |
| **Reverse Contact** | https://www.reversecontact.com/ | Da LinkedIn profile → email |
| **Odin** | https://search.odin.io/ | Intelligence search |

### People Search (clearnet)

| Piattaforma | URL | Note |
|-------------|-----|------|
| **TruePeopleSearch** | https://www.truepeoplesearch.com/ | US-focused |
| **PeopleFinder** | https://www.peoplefinder.com/ | US-focused |
| **Yandex People** | https://yandex.ru/people | RU/EU |
| **FastPeopleSearch** | https://fastpeoplesearch.com/ | US |
| **Radaris** | https://radaris.com/ | People search |
| **AllPeople** | https://allpeople.com/ | Business people |
| **TruthFinder** | https://www.truthfinder.com/ | Background checks |
| **ZabaSearch** | https://www.zabasearch.com/ | Free people search |
| **ThatsThem** | https://thatsthem.com/reverse-phone-lookup | Reverse lookup |

### Username & Social OSINT (clearnet)

| Piattaforma | URL | Note |
|-------------|-----|------|
| **UserSearch** | https://usersearch.org/ | Username search |
| **IDCrawl** | https://www.idcrawl.com/username | Username search |
| **CheckUsernames** | https://checkusernames.com/ | Multi-platform check |
| **CheckUser** | https://checkuser.org/ | Username checker |
| **AnalyzeID** | https://analyzeid.com/username/ | Username analyzer |
| **InstantUsername** | https://instantusername.com/ | Instant availability |
| **Search4Faces** | https://search4faces.com/ | Reverse face search VK/OK |
| **OSINT Toolkit Email/Username** | https://one-plus.github.io/EmailUsername | Combined search |

### LinkedIn Intelligence (clearnet)

| Piattaforma | URL | Note |
|-------------|-----|------|
| **RecruitIn** | https://recruitin.net/ | Google X-ray per LinkedIn |
| **LinkedIn CSE** | https://cse.google.com/cse?cx=daaf18e804f81bed0 | Custom search engine LinkedIn |
| **OutX Profile Viewer** | https://www.outx.ai/all-tools/linkedin-profile-viewer | View senza login |
| **LinkedIn Email Reverse** | https://osint.support/chrome-extensions/2019/09/03/linkedin-email-reverse-lookup.html | Chrome ext |

### Company Intelligence (clearnet)

| Piattaforma | URL | Note |
|-------------|-----|------|
| **OpenCorporates** | https://opencorporates.com/ | Registry aziendale internazionale |
| **Startup Tracker** | https://startuptracker.io/home | Startup database |
| **CompanyResearcher (Exa)** | https://companyresearcher.exa.ai/ | AI company research |
| **BuiltWith** | https://builtwith.com/ | Tech stack aziende |
| **Wappalyzer** | https://www.wappalyzer.com/lookup/ | Tech stack detection |
| **crt.sh** | https://crt.sh | Certificate transparency (subdomain discovery) |

### Phone OSINT (clearnet)

| Piattaforma | URL | Note |
|-------------|-----|------|
| **Truecaller** | https://truecaller.com | Reverse phone lookup |
| **PhoneInfoga** | https://sundowndev.github.io/phoneinfoga/ | Phone number OSINT |
| **SpyDialer** | https://spydialer.com/default.aspx | Free reverse phone |
| **NumLookup** | https://www.numlookup.com/ | Phone lookup |
| **ValidNumber** | https://validnumber.com/ | Phone validation |
| **Carrier Lookup** | https://www.carrierlookup.com/ | Carrier identification |

### Dark Web / Tor (clearnet gateways)

| Piattaforma | URL | Note |
|-------------|-----|------|
| **Ahmia** | https://ahmia.fi/ | Search Tor Hidden Services |
| **OnionSearchEngine** | https://onionsearchengine.com/ | Tor search |
| **Tor2Web Gateway** | https://tor2web.onionsearchengine.com/ | Access .onion via clearnet |

### Master Lists & Reference

| Risorsa | URL | Note |
|---------|-----|------|
| **awesome-osint** | https://github.com/jivoi/awesome-osint | 26K stars, curated OSINT |
| **Email-Username-OSINT** | https://github.com/The-Osint-Toolbox/Email-Username-OSINT | 195+ scan vectors |
| **GIJN Deep Internet Research** | https://gijn.org/resource/introduction-investigative-journalism-deep-internet-research/ | Guida investigativa |
| **OSINT Search Engine (CSE)** | https://cse.google.com/cse/publicurl?cx=006290531980334157382:qcaf4enph7i | Google CSE per OSINT |
| **DorkSearch** | https://dorksearch.com/ | Google dork builder |

---

## Dehashed — API Key & Uso

Nour ha pagato Dehashed (API key nella sessione precedente). Uso principale per prospecting:
1. Cerca per dominio: `@company.com` → trova tutte le email associate
2. Una volta trovati i nomi → correla con ruoli via LinkedIn/Apollo
3. Pattern: dominio PE/VC → Dehashed → nomi → CrossLinked/LinkedIn → ruolo → email verificata

---

## Waterfall Architecture Consigliata (Open Source)

```
1. CrossLinked → nomi employee da LinkedIn via search engines
2. theHarvester → email pubbliche indicizzate per il dominio
3. emailGuesser → permutazioni nome+dominio
4. Reacher → verifica SMTP + catch-all detection
5. Fire Enrich → company intelligence (funding, tech stack, team)
6. holehe → registrazioni piattaforme
7. Sherlock → social accounts
8. h8mail → breach data + linked emails
→ OUTPUT: email verificata + company data + social profiles + segnali personalizzazione
```
