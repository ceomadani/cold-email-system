#!/usr/bin/env python3
"""
dedup_segment.py — Deduplica e segmenta una lista contatti per cold email.

Prende un CSV di contatti, deduplica per EMAIL e per DOMINIO
aziendale (1 azienda = 1 account attivo alla volta), segmenta per settore/ruolo,
e separa i duplicati in un file a parte per ispezione.

Nessuna dipendenza esterna: solo standard library Python 3.
Funziona offline. Nessun dato lascia la macchina.

USO:
    python3 dedup_segment.py contatti.csv

INPUT atteso (CSV con header, colonne minime):
    email,first_name,company,domain,role,industry,size

    - email      : indirizzo (chiave di dedup primaria)
    - company    : nome azienda
    - domain     : dominio aziendale (se vuoto, viene derivato dall'email)
    - role        : ruolo (es. "decision maker", "commerce manager", "CEO")
    - industry   : settore (casa, pet, cosmetica, integratori, ...)
    - size        : fatturato/headcount (opzionale, per filtro 10M+)

OUTPUT (nella stessa cartella del file di input):
    <input>__clean.csv      → 1 riga per azienda, deduplicata, con colonna "segment"
    <input>__duplicates.csv → le righe scartate (duplicati email o dominio)
    stdout                  → riepilogo conteggi

NOTA: non verifica le email (vedi step 5 della pipeline, sez. 02b). Questo script
fa SOLO dedup + segmentazione. La verifica SMTP è un passo separato.
"""

import csv
import sys
import os
from collections import OrderedDict


def domain_from_email(email: str) -> str:
    email = (email or "").strip().lower()
    return email.split("@", 1)[1] if "@" in email else ""


def norm(s: str) -> str:
    return (s or "").strip().lower()


def make_segment(row: dict) -> str:
    """Costruisce l'etichetta di segmento: <industry>|<role-bucket>."""
    industry = norm(row.get("industry")) or "altro"
    role = norm(row.get("role"))
    if any(k in role for k in ("ceo", "founder", "fondatore", "owner", "titolare",
                                "direttore", "decision")):
        bucket = "decision-maker"
    elif any(k in role for k in ("commerce", "ecommerce", "e-commerce", "marketplace",
                                  "amazon", "marketing", "sales", "vendite")):
        bucket = "commerce"
    else:
        bucket = "altro-ruolo"
    return f"{industry}|{bucket}"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"ERRORE: file non trovato: {path}")
        sys.exit(1)

    base, _ = os.path.splitext(path)
    out_clean = base + "__clean.csv"
    out_dupes = base + "__duplicates.csv"

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    if "email" not in fieldnames:
        print("ERRORE: il CSV deve avere almeno una colonna 'email'.")
        sys.exit(1)

    seen_emails = set()
    seen_domains = set()
    clean = OrderedDict()   # email -> row
    duplicates = []

    for row in rows:
        email = norm(row.get("email"))
        if not email or "@" not in email:
            row["_reason"] = "email mancante/invalida"
            duplicates.append(row)
            continue

        domain = norm(row.get("domain")) or domain_from_email(email)
        row["domain"] = domain

        if email in seen_emails:
            row["_reason"] = "duplicato email"
            duplicates.append(row)
            continue
        if domain and domain in seen_domains:
            row["_reason"] = f"stessa azienda gia presente ({domain})"
            duplicates.append(row)
            continue

        seen_emails.add(email)
        if domain:
            seen_domains.add(domain)
        row["segment"] = make_segment(row)
        clean[email] = row

    # scrivi clean
    clean_fields = list(fieldnames)
    if "domain" not in clean_fields:
        clean_fields.append("domain")
    if "segment" not in clean_fields:
        clean_fields.append("segment")
    with open(out_clean, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=clean_fields, extrasaction="ignore")
        w.writeheader()
        for r in clean.values():
            w.writerow(r)

    # scrivi duplicates
    dup_fields = list(fieldnames) + ["domain", "_reason"]
    dup_fields = list(dict.fromkeys(dup_fields))
    with open(out_dupes, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=dup_fields, extrasaction="ignore")
        w.writeheader()
        for r in duplicates:
            w.writerow(r)

    # riepilogo
    seg_counts = {}
    for r in clean.values():
        seg_counts[r["segment"]] = seg_counts.get(r["segment"], 0) + 1

    print(f"Input            : {len(rows)} righe")
    print(f"Puliti (unici)   : {len(clean)}  → {out_clean}")
    print(f"Duplicati/scarti : {len(duplicates)}  → {out_dupes}")
    print("\nSegmenti (industry|ruolo):")
    for seg, n in sorted(seg_counts.items(), key=lambda x: -x[1]):
        print(f"  {seg:30s} {n}")


if __name__ == "__main__":
    main()
