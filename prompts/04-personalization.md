---
id: 04-personalization
status: standard
versione: 1.0
ultimo_aggiornamento: 2026-06-10
---

# Prompt 04 — Personalizzazione (la riga {{trigger}})

**Scopo:** generare la prima riga personalizzata `{{trigger}}` da dati di enrichment, su scala. È la differenza tra personalizzazione vera e "ho visto il tuo LinkedIn" (§7.5 guida).

**Quando:** dopo aver enrichito i contatti (`osint_enrich.py`), prima dell'invio. Si lancia per-contatto o in batch.

---

## PROMPT (copia-incolla)

```
Sei un esperto di personalizzazione per cold email B2B.
Devi scrivere UNA riga di aggancio ({{trigger}}) per ogni contatto,
basata su dati reali. Deve dimostrare che hai guardato DAVVERO —
non essere applicabile a chiunque.

DATI DEL CONTATTO:
- Azienda: [company_name]
- Sito/about: [estratto]
- Presenza Amazon/marketplace: [dato osint_enrich]
- News recenti: [recent_news]
- Categoria: [categoria]
- Competitor: [peer]

REGOLE:
- 8-15 parole, una riga sola.
- Deve essere SPECIFICA di questo contatto (un dato, un fatto, un gap reale).
- NO "ho visto il tuo profilo LinkedIn", NO "complimenti per il vostro lavoro",
  NO frasi che valgono per qualsiasi azienda.
- Si incastra dopo "Ho notato che {{company_name}}..." → quindi è la
  continuazione naturale di quella frase.
- Tono neutro, fattuale. Niente adulazione.
- Se i dati NON bastano per una riga davvero specifica, scrivi "INSUFFICIENTE"
  invece di inventare. Quel contatto si arricchisce a mano o si salta.

OUTPUT: solo la riga {{trigger}}, oppure "INSUFFICIENTE".
```

---

## Esempi
- ✅ "ha appena lanciato la linea skincare ma non ha listing su Amazon"
- ✅ "ha 4 best-seller assenti dal marketplace dove 12 competitor sono presenti"
- ❌ "è un brand di grande qualità nel suo settore" (vale per chiunque)
- ❌ "ho visto che siete molto attivi online" (finta personalizzazione)

## Note
Il fallback "INSUFFICIENTE" è cruciale: meglio saltare un contatto che mandargli una finta personalizzazione che lo insospettisce. La personalizzazione finta è peggio di nessuna personalizzazione.
