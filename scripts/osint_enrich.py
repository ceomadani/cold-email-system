#!/usr/bin/env python3
"""
OSINT Enrichment Pipeline — cold email personalization
Enriches Apollo contacts with publicly available data for cold email personalization.

Sources (all free):
1. Apollo org data → revenue, growth, keywords, founded year, social URLs
2. Company website → about, products, description
3. Amazon.it search → already selling on Amazon? how many products?
4. LinkedIn company page → about section, tagline
5. Google → recent news/context

Usage:
  python osint_enrich.py run          # enrich all companies (website + amazon)
  python osint_enrich.py run 50       # enrich first 50
  python osint_enrich.py linkedin     # enrich LinkedIn for all cached companies
  python osint_enrich.py linkedin 50  # enrich LinkedIn for first 50 uncached
  python osint_enrich.py status       # show progress
  python osint_enrich.py export       # export enriched CSV for cold email
"""

import json
import sys
import time
import re
import csv
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent
APOLLO_ENRICHED = BASE_DIR / "apollo_enriched.json"
OSINT_CACHE = BASE_DIR / "osint_cache.json"
FINAL_CSV = BASE_DIR / "cold_email_ready.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
}

KEEP_INDUSTRIES = {
    "health, wellness & fitness", "cosmetics", "apparel & fashion",
    "luxury goods & jewelry", "retail", "food production", "food & beverages",
    "consumer goods", "consumer services", "consumer electronics",
    "sporting goods", "alternative medicine", "arts & crafts",
    "pharmaceuticals", "textiles", "design", "chemicals",
}


def load_cache():
    if OSINT_CACHE.exists():
        with open(OSINT_CACHE) as f:
            return json.load(f)
    return {}


def save_cache(data):
    with open(OSINT_CACHE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def scrape_website(domain):
    """Scrape company homepage for about text, product info, description."""
    result = {"scraped": False, "description": "", "products_hint": "", "about": ""}

    for proto in ["https://", "http://"]:
        try:
            r = requests.get(f"{proto}{domain}", headers=HEADERS, timeout=10, allow_redirects=True)
            if r.status_code != 200:
                continue

            soup = BeautifulSoup(r.text, "html.parser")

            # Meta description
            meta = soup.find("meta", attrs={"name": "description"})
            if meta and meta.get("content"):
                result["description"] = meta["content"].strip()[:500]

            # OG description fallback
            if not result["description"]:
                og = soup.find("meta", attrs={"property": "og:description"})
                if og and og.get("content"):
                    result["description"] = og["content"].strip()[:500]

            # Title
            title = soup.find("title")
            if title:
                result["title"] = title.get_text().strip()[:200]

            # Look for about/chi-siamo text
            about_keywords = ["about", "chi-siamo", "chi siamo", "azienda", "company", "storia", "about-us"]
            for link in soup.find_all("a", href=True):
                href = link["href"].lower()
                text = link.get_text().lower().strip()
                if any(kw in href or kw in text for kw in about_keywords):
                    about_url = link["href"]
                    if about_url.startswith("/"):
                        about_url = f"{proto}{domain}{about_url}"
                    elif not about_url.startswith("http"):
                        about_url = f"{proto}{domain}/{about_url}"
                    try:
                        r2 = requests.get(about_url, headers=HEADERS, timeout=8)
                        if r2.status_code == 200:
                            soup2 = BeautifulSoup(r2.text, "html.parser")
                            for tag in soup2.find_all(["script", "style", "nav", "footer", "header"]):
                                tag.decompose()
                            text = soup2.get_text(separator=" ", strip=True)
                            text = re.sub(r"\s+", " ", text)[:1000]
                            result["about"] = text
                    except Exception:
                        pass
                    break

            # Product categories hint
            product_keywords = ["prodotti", "products", "shop", "catalogo", "catalogue", "collections", "linee"]
            nav_text = ""
            for nav in soup.find_all(["nav", "ul"]):
                nav_text += " " + nav.get_text(separator=" ", strip=True).lower()

            found_products = []
            for kw in ["skincare", "haircare", "hair care", "makeup", "fragranze", "fragrances",
                        "body care", "integratori", "supplements", "beauty", "cosmesi",
                        "cura del corpo", "cura dei capelli", "profumi", "trattamenti"]:
                if kw in nav_text or kw in r.text.lower()[:5000]:
                    found_products.append(kw)

            if found_products:
                result["products_hint"] = ", ".join(found_products[:5])

            result["scraped"] = True
            return result

        except Exception:
            continue

    return result


def check_amazon(brand_name):
    """Check if brand is already selling on Amazon.it."""
    result = {"on_amazon": False, "amazon_products": 0, "amazon_hint": ""}

    query = quote_plus(brand_name)
    try:
        r = requests.get(
            f"https://www.amazon.it/s?k={query}",
            headers={
                **HEADERS,
                "Accept": "text/html,application/xhtml+xml",
            },
            timeout=12,
        )
        if r.status_code != 200:
            return result

        soup = BeautifulSoup(r.text, "html.parser")

        # Count results
        result_count = soup.find("span", {"data-component-type": "s-result-info-bar"})
        if result_count:
            text = result_count.get_text()
            numbers = re.findall(r"[\d.]+", text.replace(".", ""))
            if numbers:
                count = int(numbers[-1])
                result["amazon_products"] = count
                result["on_amazon"] = count > 0

        # Check first few product titles for brand match
        brand_lower = brand_name.lower().split()[0]  # first word of brand
        titles = soup.find_all("span", class_="a-text-normal")
        brand_matches = sum(1 for t in titles[:10] if brand_lower in t.get_text().lower())

        if brand_matches >= 2:
            result["on_amazon"] = True
            result["amazon_hint"] = f"{brand_matches}/10 top results match brand"
        elif result["amazon_products"] > 0:
            result["amazon_hint"] = "results found but may not be exact brand match"

    except Exception:
        pass

    return result


def scrape_linkedin_company(linkedin_url):
    """Scrape public LinkedIn company page for about, tagline, specialties."""
    result = {"scraped": False, "about": "", "tagline": "", "specialties": "", "followers": ""}

    if not linkedin_url:
        return result

    url = linkedin_url.rstrip("/") + "/about/"
    try:
        r = requests.get(url, headers={
            **HEADERS,
            "Accept": "text/html,application/xhtml+xml",
        }, timeout=10, allow_redirects=True)

        if r.status_code != 200:
            return result

        soup = BeautifulSoup(r.text, "html.parser")

        # LinkedIn public pages have meta tags with company info
        og_desc = soup.find("meta", attrs={"property": "og:description"})
        if og_desc and og_desc.get("content"):
            result["about"] = og_desc["content"].strip()[:800]
            result["scraped"] = True

        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title and og_title.get("content"):
            result["tagline"] = og_title["content"].strip()[:200]

        # Try to find specialties/description in page text
        page_text = soup.get_text(separator=" ", strip=True)

        # Extract follower count if visible
        follower_match = re.search(r"([\d,.]+)\s*(?:follower|seguac)", page_text, re.I)
        if follower_match:
            result["followers"] = follower_match.group(1)

    except Exception:
        pass

    return result


def search_linkedin_posts(company_name):
    """Search Google for recent LinkedIn posts about the company."""
    result = {"posts": [], "has_posts": False}

    query = quote_plus(f'site:linkedin.com/posts "{company_name}"')
    try:
        r = requests.get(
            f"https://www.google.com/search?q={query}&num=5&hl=it",
            headers=HEADERS,
            timeout=10,
        )
        if r.status_code != 200:
            return result

        soup = BeautifulSoup(r.text, "html.parser")

        for g in soup.find_all("div", class_="g"):
            title_el = g.find("h3")
            snippet_el = g.find("div", class_="VwiC3b") or g.find("span", class_="aCOpRe")
            if title_el:
                post = {
                    "title": title_el.get_text().strip()[:200],
                    "snippet": snippet_el.get_text().strip()[:300] if snippet_el else "",
                }
                result["posts"].append(post)

        result["has_posts"] = len(result["posts"]) > 0

    except Exception:
        pass

    return result


def get_companies():
    """Load Apollo enriched data and group by company with full org data."""
    with open(APOLLO_ENRICHED) as f:
        state = json.load(f)

    companies = {}
    for p in state["enriched"]:
        email = p.get("email", "")
        if not email or p.get("email_status") != "verified":
            continue

        org = p.get("organization", {}) or {}
        company = org.get("name", "")
        industry = (org.get("industry", "") or "").lower()

        if not company or (industry and industry not in KEEP_INDUSTRIES):
            continue

        if company not in companies:
            companies[company] = {
                "domain": org.get("primary_domain", ""),
                "industry": org.get("industry", ""),
                "employees": org.get("estimated_num_employees", 0),
                "country": org.get("country", ""),
                "city": p.get("city", ""),
                "linkedin_url": org.get("linkedin_url", ""),
                "twitter_url": org.get("twitter_url", ""),
                "facebook_url": org.get("facebook_url", ""),
                "founded_year": org.get("founded_year", ""),
                "revenue": org.get("organization_revenue_printed", ""),
                "keywords": org.get("keywords", []),
                "growth_6m": org.get("organization_headcount_six_month_growth", ""),
                "growth_12m": org.get("organization_headcount_twelve_month_growth", ""),
                "contacts": [],
            }

        companies[company]["contacts"].append({
            "first_name": p.get("first_name", ""),
            "last_name": p.get("last_name", ""),
            "email": email,
            "title": p.get("title", ""),
            "linkedin_url": p.get("linkedin_url", ""),
            "seniority": p.get("seniority", ""),
        })

    return companies


def do_run(limit=None):
    companies = get_companies()
    cache = load_cache()

    remaining = {k: v for k, v in companies.items() if k not in cache}
    if limit:
        remaining = dict(list(remaining.items())[:limit])

    print(f"\n{'='*60}")
    print(f"  OSINT ENRICHMENT — Cold Email Pipeline")
    print(f"{'='*60}")
    print(f"  Total companies:     {len(companies)}")
    print(f"  Already enriched:    {len(cache)}")
    print(f"  This batch:          {len(remaining)}")
    print(f"{'='*60}\n")

    for i, (company, info) in enumerate(remaining.items()):
        domain = info["domain"]
        print(f"  [{i+1}/{len(remaining)}] {company:35s}", end="", flush=True)

        enrichment = {
            "company": company,
            "domain": domain,
            "industry": info["industry"],
            "employees": info["employees"],
            "enriched_at": datetime.now().isoformat(),
        }

        # 1. Website scrape
        if domain:
            site = scrape_website(domain)
            enrichment["website"] = site
            has_site = "site" if site["scraped"] else "no-site"
        else:
            enrichment["website"] = {"scraped": False}
            has_site = "no-domain"

        # 2. Amazon check
        amazon = check_amazon(company.split(" ")[0] if len(company.split()) > 2 else company)
        enrichment["amazon"] = amazon
        has_amazon = f"AMZ:{amazon['amazon_products']}" if amazon["on_amazon"] else "no-AMZ"

        print(f" → {has_site} | {has_amazon}")

        cache[company] = enrichment
        if (i + 1) % 10 == 0:
            save_cache(cache)

        time.sleep(1.5)

    save_cache(cache)

    # Stats
    scraped = sum(1 for v in cache.values() if v.get("website", {}).get("scraped"))
    on_amazon = sum(1 for v in cache.values() if v.get("amazon", {}).get("on_amazon"))
    with_desc = sum(1 for v in cache.values() if v.get("website", {}).get("description"))
    with_products = sum(1 for v in cache.values() if v.get("website", {}).get("products_hint"))

    print(f"\n{'='*60}")
    print(f"  RESULTS")
    print(f"{'='*60}")
    print(f"  Companies enriched:    {len(cache)}")
    print(f"  Website scraped OK:    {scraped}")
    print(f"  With description:      {with_desc}")
    print(f"  With product hints:    {with_products}")
    print(f"  Already on Amazon.it:  {on_amazon}")
    print(f"{'='*60}\n")


def do_linkedin(limit=None):
    """Enrich cached companies with LinkedIn company page + posts."""
    companies = get_companies()
    cache = load_cache()

    # Only enrich companies already in cache (from website+amazon pass)
    to_enrich = {k: v for k, v in companies.items()
                 if k in cache and "linkedin" not in cache[k]}
    if limit:
        to_enrich = dict(list(to_enrich.items())[:limit])

    print(f"\n{'='*60}")
    print(f"  LINKEDIN ENRICHMENT — Company Pages + Posts")
    print(f"{'='*60}")
    print(f"  Companies in cache:     {len(cache)}")
    print(f"  Already LinkedIn-done:  {sum(1 for v in cache.values() if 'linkedin' in v)}")
    print(f"  This batch:             {len(to_enrich)}")
    print(f"{'='*60}\n")

    for i, (company, info) in enumerate(to_enrich.items()):
        li_url = info.get("linkedin_url", "")
        print(f"  [{i+1}/{len(to_enrich)}] {company:35s}", end="", flush=True)

        # 1. Scrape LinkedIn company page
        li_data = scrape_linkedin_company(li_url)
        has_li = "LI-ok" if li_data["scraped"] else "no-LI"

        # 2. Search for LinkedIn posts (rate limit: do only every 3rd to avoid Google block)
        posts_data = {"posts": [], "has_posts": False}
        if (i + 1) % 3 == 0:
            posts_data = search_linkedin_posts(company)
            has_posts = f"posts:{len(posts_data['posts'])}" if posts_data["has_posts"] else "no-posts"
        else:
            has_posts = "skip-posts"

        cache[company]["linkedin"] = li_data
        cache[company]["linkedin_posts"] = posts_data

        print(f" → {has_li} | {has_posts}")

        if (i + 1) % 10 == 0:
            save_cache(cache)

        time.sleep(2)

    save_cache(cache)

    li_ok = sum(1 for v in cache.values() if v.get("linkedin", {}).get("scraped"))
    with_posts = sum(1 for v in cache.values() if v.get("linkedin_posts", {}).get("has_posts"))
    print(f"\n  LinkedIn scraped: {li_ok}")
    print(f"  With posts found: {with_posts}")


def do_status():
    cache = load_cache()
    companies = get_companies()

    print(f"\n  Total companies: {len(companies)}")
    print(f"  OSINT enriched:  {len(cache)}")

    if cache:
        scraped = sum(1 for v in cache.values() if v.get("website", {}).get("scraped"))
        on_amazon = sum(1 for v in cache.values() if v.get("amazon", {}).get("on_amazon"))
        with_desc = sum(1 for v in cache.values() if v.get("website", {}).get("description"))
        li_ok = sum(1 for v in cache.values() if v.get("linkedin", {}).get("scraped"))
        with_posts = sum(1 for v in cache.values() if v.get("linkedin_posts", {}).get("has_posts"))
        print(f"  Website OK:      {scraped}")
        print(f"  On Amazon:       {on_amazon}")
        print(f"  With desc:       {with_desc}")
        print(f"  LinkedIn OK:     {li_ok}")
        print(f"  With LI posts:   {with_posts}")


def do_export():
    """Export enriched contacts ready for cold email."""
    cache = load_cache()
    companies = get_companies()

    if not cache:
        print("Run enrichment first.")
        return

    def title_score(title):
        t = (title or "").lower()
        if re.search(r"export", t): return 100
        if re.search(r"e-?commerce", t): return 95
        if re.search(r"international|estero", t): return 90
        if re.search(r"commercial|commerciale|sales director", t): return 80
        if re.search(r"marketing|brand|digital", t): return 70
        if re.search(r"ceo|amministratore|managing director", t): return 60
        if re.search(r"founder|fondatore|owner|titolare", t): return 55
        return 10

    rows = []
    for company, info in companies.items():
        osint = cache.get(company, {})
        website = osint.get("website", {})
        amazon = osint.get("amazon", {})
        linkedin = osint.get("linkedin", {})
        li_posts = osint.get("linkedin_posts", {})

        # Pick best contact per company
        best = max(info["contacts"], key=lambda c: title_score(c["title"]))

        # Build personalization line
        personalization_parts = []
        if website.get("description"):
            personalization_parts.append(website["description"][:200])
        if website.get("products_hint"):
            personalization_parts.append(f"Products: {website['products_hint']}")
        if amazon.get("on_amazon"):
            personalization_parts.append(f"Already on Amazon.it ({amazon['amazon_products']} products)")
        else:
            personalization_parts.append("Not yet on Amazon.it")
        if linkedin.get("about"):
            personalization_parts.append(f"LI: {linkedin['about'][:150]}")
        if li_posts.get("posts"):
            latest = li_posts["posts"][0].get("snippet", "")[:100]
            if latest:
                personalization_parts.append(f"Recent post: {latest}")

        # Keywords from Apollo
        keywords = ", ".join(info.get("keywords", [])[:5]) if info.get("keywords") else ""

        rows.append({
            "first_name": best["first_name"],
            "last_name": best["last_name"],
            "email": best["email"],
            "title": best["title"],
            "person_linkedin": best.get("linkedin_url", ""),
            "company_name": company,
            "company_domain": info["domain"],
            "company_industry": info["industry"],
            "company_employees": info["employees"],
            "company_city": info.get("city", ""),
            "founded_year": info.get("founded_year", ""),
            "revenue": info.get("revenue", ""),
            "growth_6m": info.get("growth_6m", ""),
            "keywords": keywords,
            "company_linkedin": info.get("linkedin_url", ""),
            "company_twitter": info.get("twitter_url", ""),
            "company_description": website.get("description", ""),
            "linkedin_about": linkedin.get("about", ""),
            "linkedin_followers": linkedin.get("followers", ""),
            "product_categories": website.get("products_hint", ""),
            "on_amazon": "YES" if amazon.get("on_amazon") else "NO",
            "amazon_products": amazon.get("amazon_products", 0),
            "recent_li_post": li_posts["posts"][0].get("snippet", "")[:200] if li_posts.get("posts") else "",
            "personalization": " | ".join(personalization_parts),
        })

    # Sort: on Amazon first (hotter leads), then by title relevance
    rows.sort(key=lambda x: (0 if x["on_amazon"] == "YES" else 1, -title_score(x["title"])))

    fields = list(rows[0].keys()) if rows else []
    with open(FINAL_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    on_amz = sum(1 for r in rows if r["on_amazon"] == "YES")
    with_desc = sum(1 for r in rows if r["company_description"])
    print(f"\nExported {len(rows)} contacts (1 per company) to {FINAL_CSV}")
    print(f"  Already on Amazon: {on_amz}")
    print(f"  With description:  {with_desc}")
    print(f"  With products:     {sum(1 for r in rows if r['product_categories'])}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if cmd == "run":
        do_run(limit)
    elif cmd == "linkedin":
        do_linkedin(limit)
    elif cmd == "status":
        do_status()
    elif cmd == "export":
        do_export()
    else:
        print(__doc__)
