# Changelog prompt AI

Log delle versioni dei prompt di generazione. Stessa logica del changelog template: si versiona un prompt quando produce output sistematicamente migliori (meno editing manuale, script che convertono di più).

Formato:
```
## [data] · <prompt> v<x.y>
- Cosa è cambiato nel prompt
- Perché (quale problema dell'output risolveva)
```

---

## 2026-06-10 · bootstrap pipeline · v1.0

Creata la pipeline di 5 prompt:
- `01-icp-research` — ICP + decisore (incorpora la lezione "il decisore non è sempre il CEO")
- `02-offer-creation` — frontend offer ad alto valore
- `03-script-generation` — script 3 tier × 3 lunghezze (specs RevGrowth verbatim + checklist 10 punti auto-valutata)
- `04-personalization` — riga `{{trigger}}` da enrichment, con fallback "INSUFFICIENTE"
- `05-reply-classification` — 4 categorie + opt-out, con bozza dal template

Tutti `standard` v1.0. Le guardrail copy (§7.4 guida) sono hardcoded in `03` e `04`.

---

<!-- Le prossime entry vanno sopra questa riga. -->
