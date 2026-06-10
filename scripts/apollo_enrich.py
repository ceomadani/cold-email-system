#!/usr/bin/env python3
"""
Apollo.io Bulk Enrichment — decision-maker per lista prospect
Enriches search results to reveal emails. 1 credit per person.
"""

import requests
import os
import json
import time
import csv
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
SEARCH_RESULTS = BASE_DIR / "apollo_search_results.json"
ENRICHED_FILE = BASE_DIR / "apollo_enriched.json"
FINAL_CSV = BASE_DIR / "apollo_decision_makers.csv"

API_KEY = os.environ.get("APOLLO_API_KEY", "")  # export APOLLO_API_KEY=...
BASE = "https://api.apollo.io/api/v1"
HEADERS = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "x-api-key": API_KEY,
}

MEGA_CORPS = {
    "Bvlgari", "Gucci", "DOLCE&GABBANA", "Giorgio Armani", "Prada Group",
    "Bottega Veneta", "Valentino", "Brunello Cucinelli", "FERRAGAMO",
    "Versace", "Fendi", "Hermès", "Louis Vuitton", "Chanel", "Dior",
    "LVMH", "Kering", "Richemont",
}


def load_enriched():
    if ENRICHED_FILE.exists():
        with open(ENRICHED_FILE) as f:
            return json.load(f)
    return {"enriched": [], "enriched_ids": [], "credits_used": 0, "last_updated": ""}


def save_enriched(data):
    data["last_updated"] = datetime.now().isoformat()
    with open(ENRICHED_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def enrich_all():
    with open(SEARCH_RESULTS) as f:
        search = json.load(f)

    all_people = search["people"]
    has_email = [p for p in all_people if p.get("has_email")]

    # Skip mega-corps
    candidates = []
    for p in has_email:
        org = p.get("organization", {}) or {}
        org_name = org.get("name", "")
        if org_name not in MEGA_CORPS:
            candidates.append(p)

    state = load_enriched()
    done_ids = set(state["enriched_ids"])
    remaining = [p for p in candidates if p["id"] not in done_ids]

    print(f"\n{'='*60}")
    print(f"  APOLLO.IO BULK ENRICHMENT")
    print(f"{'='*60}")
    print(f"  Total with email:    {len(has_email)}")
    print(f"  After mega-corp filter: {len(candidates)}")
    print(f"  Already enriched:    {len(done_ids)}")
    print(f"  This batch:          {len(remaining)}")
    print(f"  Credits used so far: {state['credits_used']}")
    print(f"{'='*60}\n")

    batch_size = 10
    batches_this_minute = 0
    minute_start = time.time()

    for i in range(0, len(remaining), batch_size):
        batch = remaining[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(remaining) + batch_size - 1) // batch_size

        # Rate limit: max 18 batches/minute to stay safe
        batches_this_minute += 1
        if batches_this_minute >= 18:
            elapsed = time.time() - minute_start
            if elapsed < 60:
                wait = 61 - elapsed
                print(f"  Rate limit pause: {wait:.0f}s...")
                time.sleep(wait)
            batches_this_minute = 0
            minute_start = time.time()

        ids = [p["id"] for p in batch]
        print(f"  [{batch_num}/{total_batches}] Enriching {len(ids)} contacts...", end="", flush=True)

        try:
            resp = requests.post(
                f"{BASE}/people/bulk_match",
                headers=HEADERS,
                json={
                    "details": [{"id": pid} for pid in ids],
                    "reveal_personal_emails": False,
                    "reveal_phone_number": False,
                },
                timeout=30,
            )

            if resp.status_code == 429:
                print(f" RATE LIMITED — waiting 60s")
                time.sleep(60)
                batches_this_minute = 0
                minute_start = time.time()
                # Retry
                resp = requests.post(
                    f"{BASE}/people/bulk_match",
                    headers=HEADERS,
                    json={
                        "details": [{"id": pid} for pid in ids],
                        "reveal_personal_emails": False,
                        "reveal_phone_number": False,
                    },
                    timeout=30,
                )

            if resp.status_code != 200:
                print(f" ERROR {resp.status_code}: {resp.text[:200]}")
                continue

            result = resp.json()
            matches = result.get("matches", [])
            credits = result.get("credits_consumed", 0)

            state["enriched"].extend(matches)
            state["enriched_ids"].extend(ids)
            state["credits_used"] += credits

            verified = sum(1 for m in matches if m.get("email_status") == "verified")
            print(f" -> {len(matches)} enriched, {verified} verified, {credits} credits (total: {state['credits_used']})")

            # Save every 5 batches
            if batch_num % 5 == 0:
                save_enriched(state)

            time.sleep(2)

        except Exception as e:
            print(f" ERROR: {e}")
            time.sleep(5)

    save_enriched(state)
    print(f"\n  DONE. Total enriched: {len(state['enriched'])}, Credits: {state['credits_used']}")
    print(f"  Saved to: {ENRICHED_FILE}")


def export_csv():
    state = load_enriched()
    enriched = state["enriched"]

    if not enriched:
        print("No enriched data. Run enrichment first.")
        return

    rows = []
    seen = set()
    for p in enriched:
        email = p.get("email", "")
        if not email or email in seen:
            continue
        seen.add(email)

        org = p.get("organization", {}) or {}
        rows.append({
            "first_name": p.get("first_name", ""),
            "last_name": p.get("last_name", ""),
            "title": p.get("title", ""),
            "email": email,
            "email_status": p.get("email_status", ""),
            "linkedin_url": p.get("linkedin_url", ""),
            "city": p.get("city", ""),
            "country": p.get("country", ""),
            "seniority": p.get("seniority", ""),
            "company_name": org.get("name", ""),
            "company_domain": org.get("primary_domain", org.get("website_url", "")),
            "company_industry": org.get("industry", ""),
            "company_employees": org.get("estimated_num_employees", ""),
            "company_country": org.get("country", ""),
        })

    rows.sort(key=lambda x: (x["company_name"], -len(x["title"])))

    fields = list(rows[0].keys()) if rows else []
    with open(FINAL_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    verified = sum(1 for r in rows if r["email_status"] == "verified")
    companies = len(set(r["company_name"] for r in rows))
    print(f"\nExported {len(rows)} contacts ({verified} verified) from {companies} companies to {FINAL_CSV}")


def status():
    state = load_enriched()
    enriched = state["enriched"]
    print(f"\n  Enriched contacts: {len(enriched)}")
    print(f"  Credits used: {state['credits_used']}")

    if enriched:
        verified = sum(1 for m in enriched if m.get("email_status") == "verified")
        companies = len(set((m.get("organization", {}) or {}).get("name", "") for m in enriched))
        print(f"  Verified emails: {verified}")
        print(f"  Unique companies: {companies}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "enrich":
        enrich_all()
    elif cmd == "export":
        export_csv()
    elif cmd == "status":
        status()
    else:
        print("Usage: python apollo_enrich.py [enrich|export|status]")
