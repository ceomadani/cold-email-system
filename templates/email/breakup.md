---
id: breakup
tipo: email
framework:
status: standard
versione: 1.0
segmento: generico
lingua: it
ultimo_aggiornamento: 2026-06-10
metrica: "chiusura sequenza, sblocca quota significativa di risposte 'in realtà sì'"
---

# Breakup — Email di chiusura sequenza (Day 18-21)

**Quando usarlo:** è l'ultima email della sequenza. Sempre la stessa funzione, indipendente dal segmento.

**Logica (perché funziona, §7.7 guida):** togliere la disponibilità attiva la loss aversion ("ultima chiamata") e insieme dimostra che non sei lo spammer che insisterà per sempre. È l'email che sblocca più risposte "in realtà sì, parliamone" di quanto ci si aspetti.

## Subject (1-3 parole, spintax)
`chiudo qui` · `ultima` · `{company_name}`

## Body
```
{{first_name}},

Non voglio {essere insistente|insistere} — se {{tema_offer}} non è una priorità
per {{company_name}} {in questo momento|ora}, capisco perfettamente.

Se in futuro {dovesse interessarvi|cambiasse qualcosa}, resto disponibile.

{{firma}}
```

## Variabili richieste
`{{first_name}}`, `{{company_name}}`, `{{tema_offer}}`, `{{firma}}`

## Esempio compilato
> Marco,
>
> Non voglio essere insistente — se Amazon non è una priorità per Brand Esempio in questo momento, capisco perfettamente.
>
> Se in futuro dovesse interessarvi, resto disponibile.
>
> [firma]

## Note
Tono genuino, mai passivo-aggressivo. Il "capisco perfettamente" deve suonare vero. Dopo questa email il contatto va nella subsequence di nurture (ricontatto a 60-90 giorni, vedi `follow-up/subsequence-nurture.md`).
