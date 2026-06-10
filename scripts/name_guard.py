#!/usr/bin/env python3
"""
name_guard.py — Filtro anti-spazzatura per nomi estratti via OSINT.

Quando estrai nomi da scraping (CrossLinked, theHarvester, siti web), molti non
sono nomi di persona: sono titoli di ruolo, nomi azienda, parole comuni indicizzate
per errore. Questo script segna ogni nome come VALIDO o SCARTO con una motivazione.

Nessuna dipendenza esterna: solo standard library. Funziona offline.

USO:
    python3 name_guard.py "Cristina Rossi"
    python3 name_guard.py < lista_nomi.txt        # un nome per riga
    echo "Amministratore Delegato" | python3 name_guard.py

OUTPUT: <VALID|SKIP>  <nome>  [motivo se SKIP]
"""

import sys

# parole italiane comuni / ruoli / termini aziendali che NON sono nomi di persona
BLOCKLIST = {
    # ruoli
    "amministratore", "delegato", "direttore", "responsabile", "titolare",
    "fondatore", "presidente", "manager", "buyer", "commerciale", "vendite",
    "marketing", "export", "import", "ufficio", "reparto", "area", "settore",
    # entità aziendali
    "srl", "spa", "snc", "sas", "srls", "group", "gruppo", "company", "azienda",
    "industria", "industrie", "holding", "partners", "associati", "studio",
    # parole comuni / web
    "contatti", "chi", "siamo", "home", "privacy", "policy", "cookie", "team",
    "info", "sales", "support", "newsletter", "iscriviti", "accedi", "login",
    "prodotti", "servizi", "catalogo", "carrello", "ordine", "cerca", "menu",
    "italiano", "english", "leggi", "tutto", "scopri", "maggiori", "informazioni",
}


def is_valid_name(name: str):
    parts = [p for p in name.strip().split() if p]
    if len(parts) < 2:
        return False, "meno di 2 parole"
    if len(parts) > 5:
        return False, "troppe parole (probabile frase)"
    for p in parts:
        low = p.lower().strip(".,;:")
        if low in BLOCKLIST:
            return False, f"parola bloccata: '{p}'"
        if len(low) < 2:
            return False, f"parola troppo corta: '{p}'"
        if not p[0].isupper():
            return False, f"parola non maiuscola: '{p}'"
        if not any(c.isalpha() for c in p):
            return False, f"nessuna lettera: '{p}'"
    return True, ""


def process(name: str):
    name = name.strip()
    if not name:
        return
    ok, reason = is_valid_name(name)
    if ok:
        print(f"VALID  {name}")
    else:
        print(f"SKIP   {name}   [{reason}]")


def main():
    args = sys.argv[1:]
    if args:
        process(" ".join(args))
    else:
        for line in sys.stdin:
            process(line)


if __name__ == "__main__":
    main()
