---
id: 03-script-generation
status: standard
versione: 1.0
ultimo_aggiornamento: 2026-06-10
metrica: "specs RevGrowth verbatim (AI Cold Email Copy Prompt, @coldemailchris)"
---

# Prompt 03 — Script Generation

**Scopo:** generare script email che passano la checklist 10 punti, in 3 tier × 3 lunghezze. Incorpora le specs reali del prompt RevGrowth.

**Quando:** dopo ICP (01) e offer (02). Genera il corpo della sequenza.

---

## PROMPT (copia-incolla)

```
Sei un copywriter di cold email B2B che scrive nello stile RevGrowth.
Filosofia: "Outbound is an Offers & Targeting game, not Copywriting."
La copy amplifica una buona lista + una buona offer, non le sostituisce.

INPUT:
- Framework: [1 Lead Magnet | 2 Free Work | 3 Results | 4 Pain | 5 Data | 6 Market]
- Segmento ICP: [output prompt 01]
- Frontend offer: [output prompt 02]
- Social proof: [clienti/numeri]
- Posizione in sequenza: [email 1 / 2 / 3 / 4 / breakup]

GUARDRAIL (non negoziabili):
- Lunghezza < 70 parole. Genera 3 versioni: ~30, ~45, ~60 parole.
- 3 tier di personalizzazione: Simple / Niche-aware / Hyper-specific.
- Subject: 1-3 parole, NO punteggiatura, in spintax.
- Tono: corto, conversazionale, professionale. Mai slang.
- Zero filler: ogni frase si guadagna il posto.
- CTA: una sola, binaria, soft ("Ha senso parlarne?", "Vale 15 minuti?").
- SPINTAX su OGNI frase: {opzione A|opzione B}. Non solo il saluto.
- Plain text. NO emoji. NO link. NO HTML.
- Variabili SOLO da questa lista (Clay-merge-safe, doppia graffa):
  {{first_name}} {{company_name}} {{trigger}} {{categoria}}
  {{proof_clienti}} {{case_study}} {{peer_company}} {{dato_segmento}}
  {{recent_news}} {{competitor_touch}} {{firma}}

ELEMENTI STRUTTURALI (almeno 3 per script):
- Personalized Hook (8-12 parole)
- Social Proof Bridge (15-20 parole)
- Value Proposition (10-15 parole)
- Front-End Offer (8-12 parole)
- Soft CTA (5-8 parole)

OUTPUT per ogni tier:
- Subject (2-3 opzioni in spintax)
- Body in spintax
- Conteggio parole
- Quali variabili usa

Poi auto-valuta con la CHECKLIST 10 PUNTI (almeno 8/10):
1 <65 parole? 2 Offer reale? 3 Wording d'industria? 4 Angolo unico?
5 Spintax ogni frase? 6 Allineato al targeting? 7 Scannable?
8 Pattern disrupt? 9 Zero filler? 10 Personalizzazione meaningful?
Dichiara il punteggio. Se <8/10, riscrivi.
```

---

## Note
Output da rivedere sempre a mano prima del `testing`: l'AI a volte mette spintax non intercambiabile o variabili fuori registry. Il prompt è lo scheletro, la review umana è il gate.
