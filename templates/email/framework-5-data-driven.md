---
id: framework-5-data-driven
tipo: email
framework: 5
status: standard
versione: 1.0
segmento: generico
lingua: it
ultimo_aggiornamento: 2026-06-10
metrica: "default per email 2 della sequenza (angolo nuovo dato), caso applicato"
---

# Framework 5 — Data-Driven Insight

**Quando usarlo:** hai un dato scrapabile che mostra un weak point del prospect (lo dà l'enrichment di §6). Il più potente come **email 2** — l'angolo nuovo dopo il primo contatto.

**Logica:** mostri al prospect qualcosa che lui non sa di sé, ricavato dai suoi stessi dati. È irresistibile perché è specifico e perché implica che tu hai già fatto un lavoro su di lui.

## Subject (1-3 parole, spintax)
`{numero} prodotti` · `dato {company_name}` · `{categoria} Amazon`

## Body
```
{{first_name}},

{Un dato rapido|Un numero}: {{competitor_touch}}.

Per {{company_name}} {potrebbe significare|vorrebbe dire} {{dato_segmento}},
completamente gestito da noi.

{Vale 15 minuti|Ha senso un confronto} per capire se torna?

{{firma}}
```

## Variabili richieste
`{{first_name}}`, `{{company_name}}`, `{{competitor_touch}}`, `{{dato_segmento}}`, `{{firma}}`

## Esempio compilato
> Marco,
>
> Un dato rapido: 12 competitor della vostra categoria sono già su Amazon con catalogo completo, Brand Esempio no.
>
> Per Brand Esempio potrebbe significare un nuovo canale di acquisizione, completamente gestito da noi.
>
> Vale 15 minuti per capire se torna?
>
> [firma]

## Note
Il dato deve essere verificabile e specifico — generato da `osint_enrich.py` (Amazon search, competitor presence). Un dato vago ("il mercato cresce") non è un insight, è rumore.
