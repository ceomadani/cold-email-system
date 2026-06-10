# Changelog libreria template

Log cronologico delle promozioni a `standard`. Ogni riga registra: cosa è cambiato, su quale segmento, e **il numero che ha giustificato la decisione**. È il diario della standardizzazione — quando tra sei mesi qualcuno chiede "perché usiamo questa versione?", la risposta è qui.

Formato di una entry:
```
## [data] · <template> v<x.y> · <draft→testing | testing→standard | standard→retired>
- Segmento: <nome>
- Metrica: <numero che ha deciso> (es. reply rate 7.2% vs 4.1% dello standard precedente)
- Note: <cosa è cambiato e perché>
```

---

## 2026-06-10 · bootstrap libreria · v1.0

Creata la struttura iniziale. Stato di partenza, distillato dal caso applicato (offer gestione canale Amazon, batch casa/cosmetica) e dalla metodologia RevGrowth/@coldemailchris:

**Email — promossi a `standard` v1.0** (default di sequenza):
- `framework-2-free-work` → email 1 (offer diretta)
- `framework-5-data-driven` → email 2 (angolo dato)
- `framework-3-results` → email 3 (case study)
- `breakup` → chiusura (Day 18-21)

**Email — `draft` v1.0** (da testare prima di promuovere):
- `framework-1-lead-magnet`, `framework-4-pain-point`, `framework-6-market-intel`

**Reply — `standard` v1.0** (4 categorie + opt-out):
- `reply-interested`, `reply-objection`, `reply-wrong-timing`, `reply-referral`

**Follow-up — `standard` v1.0:**
- `subsequence-nurture` (riciclo 60-90gg)

Metrica di partenza: nessun A/B ancora. Gli `standard` v1.0 sono i default ragionati, non i vincitori di un test. Il primo ciclo di campagne genererà i numeri per le prime promozioni reali.

---

<!-- Le prossime entry vanno sopra questa riga, in ordine cronologico inverso (più recente in alto, sotto il titolo). -->
