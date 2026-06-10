# Libreria template — email, follow-up, risposte

Questa è la libreria viva del sistema. Non è un set fisso: **cresce e si standardizza nel tempo** man mano che i dati provano cosa funziona. Un template nasce `draft`, va in `testing` su un segmento, e diventa `standard` solo quando batte l'alternativa sui numeri.

## Struttura

```
templates/
├── _CONVENZIONI.md          ← LA LEGGE: status lifecycle, variabili, spintax, naming
├── _CHANGELOG.md            ← log delle promozioni a standard (con il numero che le giustifica)
├── email/                   ← i 6 framework + breakup
│   ├── framework-1-lead-magnet.md
│   ├── framework-2-free-work.md      (standard · email 1)
│   ├── framework-3-results.md        (standard · email 3)
│   ├── framework-4-pain-point.md
│   ├── framework-5-data-driven.md    (standard · email 2)
│   ├── framework-6-market-intel.md
│   └── breakup.md                    (standard · chiusura)
├── follow-up/
│   └── subsequence-nurture.md        (riciclo non-responder, 60-90gg)
└── reply/                   ← le 4 categorie di reply management
    ├── _README.md
    ├── reply-interested.md
    ├── reply-objection.md
    ├── reply-wrong-timing.md
    └── reply-referral.md
```

## Come si lavora con la libreria

1. **Parti dagli `standard`.** Per la email 1 → framework 2; email 2 → framework 5; email 3 → framework 3; email 4 → framework 4; chiusura → breakup. Sono i default provati.
2. **Compila le variabili** dal registry (`_CONVENZIONI.md` §3) — l'enrichment (`scripts/`) le riempie.
3. **Vuoi migliorare un template?** Crea la variante con suffisso lettera (`framework-2-free-work-b.md`, status `testing`), A/B test su un segmento a parità di lista.
4. **La variante vince?** Promuovila a `standard`, manda la vecchia in `retired`, scrivi la riga nel `_CHANGELOG.md` col numero che l'ha giustificata.

## Provenienza

Cosa di questa libreria è preso dalle risorse RevGrowth/@coldemailchris e cosa è composizione/aggiunta: vedi `../PROVENANCE.md` (mappa riga-per-riga). In breve: framework, regole copy, sequenzialità, checklist e categorie di risposta sono **sorgente**; il testo italiano dei template è **applicazione** della loro struttura; lo status lifecycle è **aggiunta**.

## Perché questo sistema

Senza, dopo sei mesi hai venti versioni di ogni email e nessuno sa quale usare. Con lo status lifecycle, in ogni momento c'è **un solo `standard` per slot**, e la storia di come ci si è arrivati è nel changelog. È la stessa disciplina dell'iterazione per segmento della guida (§9.4): si cambia lo standard solo coi dati, mai a sensazione.

## Mappa verso la guida

| Cartella | Sezione guida |
|----------|---------------|
| `email/` | §7 (script + 6 framework) |
| `follow-up/` | §8 (sequenzialità + subsequence) |
| `reply/` | §9.2 (reply management) |
| `../prompts/` | §7.6 (generazione script con AI) |
