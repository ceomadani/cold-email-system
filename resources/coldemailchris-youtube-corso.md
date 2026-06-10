# Full Cold Email Course For 2026 — Christian Plascencia (@coldemailchris)

**Creator:** Christian Plascencia — Co-Founder of RevGrowth.ai
**URL:** https://www.youtube.com/watch?v=AmnHLZG4TI8
**Source:** Cross-referenced from course modules, LinkedIn, Smartlead case study, RevGrowth website

---

## Core Philosophy

**"Outbound is an Offers & Targeting game, not a Copywriting game."**

The level of value you offer in your frontend offer has a DIRECT correlation with the number of meetings you book. Success comes from delivering superior value compared to competitors in the prospect's inbox.

---

## Course Structure (9 Modules, 189 min)

| # | Module | Duration | Core Topic |
|---|--------|----------|------------|
| 1 | Entire Outbound Playbook Overview | 32 min | End-to-end system architecture |
| 2 | Essential Tools & Infrastructure | 10 min | Tech stack setup |
| 3 | Strategy Development via AI Prompting | 15 min | Using AI for ICP, offer, and messaging |
| 4 | Messaging / Script Writing | 54 min | Frameworks, spintax, sequences |
| 5 | Building 97%+ Qualified Lists | 17 min | Lead sourcing and verification |
| 6 | Creating Clay Tables | 38 min | Data enrichment workflows |
| 7 | Reply Management (30%+ Meeting Conversion) | 15 min | Inbox management, response protocols |
| 8 | Sales Process / Close Rate Optimization | 8 min | Converting cold leads to deals |

---

## 6 Cold Email Frameworks

1. **Lead Magnet Approach:** "Created {Lead Magnet} for {COMPANY}" + social proof + interest-based CTA
2. **Free Work / Intro Offer:** "Interested in {Free Work/Intro Offer} for {COMPANY}?" + social proof in P.S.
3. **Results-Focused:** "Interested in {Dream Result x Mechanism x Timeframe}?" + guarantee/risk reversal + discussion CTA
4. **Pain Point Solution:** Highlight "Relevant Pain Point" then offer targeted solution + social proof in P.S.
5. **Data-Driven Insight:** Use "Relevant Touchpoint" to identify weak points from scrapable data, then introduce solution
6. **Market Intelligence:** Combine "Relevant Touchpoint" with unique market insight, offer free work around that insight

### Best-Performing Template
```
{{first_name}} - if we {{Offering Valuable Service for FREE/massive discount}} 
for {{company_name}} to {{achieve result}} - would you be interested?

{{Signature}}

P.S. {{More Context/Social Proof}}
```

This ONLY works if you: (1) have a great Frontend Offer, and (2) have solid social proof / B2B funnel outside of the cold email.

### Frontend Offer Examples
- Free or discounted service components
- Free trial (e.g. 30 days)
- Full service free in exchange for testimonials
- Free partnership referrals leveraging your client network

---

## Infrastructure System (RevGrowth Production Setup)

### Tech Stack
| Layer | Tool | Purpose |
|-------|------|---------|
| Email Accounts | Outlook + Superwave | Mailbox provisioning at scale |
| Sending Platform | Smartlead.ai | Sending, rotation, master inbox, subsequences |
| Lead Scraping | Apollo.io or Clay | Company/contact discovery + enrichment |
| Data Enrichment | Clay Tables | Waterfall enrichment, GPT personalization |
| Email Verification | Millionverifier | Pre-send verification, bounce < 2% |
| Reply Routing | Smartlead Master Inbox + Slack + Airtable | Centralized reply management |
| Warmup | Smartlead built-in (or Mailreach/Warmy) | Sender reputation building |

### Scale Numbers
- 3,000+ email accounts managed through one master inbox
- 168 sending domains with auto-pause on bounce spikes
- ~1,800 emails/day in production
- 60+ email accounts per campaign
- 5M+ cold emails sent
- 1,000+ meetings booked
- $35M pipeline generated across 1,100+ campaigns in 47 verticals

---

## Domain & Deliverability Setup

### Step 1: Domain Strategy
- 4-8 dedicated cold email domains (brand variations, NEVER the primary domain)
- Buy 30-60 days before use for domain age advantage
- 2-3 mailboxes per domain
- Cap each mailbox at 25-30 sends/day

### Step 2: DNS Authentication

**SPF (Google Workspace):**
```
v=spf1 include:_spf.google.com ~all
```
**SPF (Microsoft 365):**
```
v=spf1 include:spf.protection.outlook.com ~all
```
Use `~all` (soft fail) not `-all` (hard fail).

**DKIM:** Generate via admin console. Verify with test email checking headers for `DKIM=pass`.

**DMARC (starter):**
```
v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com; pct=100; aspf=r; adkim=r;
```
Start `p=none` for 4-6 weeks before enforcing.

### Step 3: Mailbox Provisioning
- Real first/last names (Bob Smith, Sarah Chen)
- Realistic addresses (firstname@domain.com)
- Profile pictures + signatures for each
- NEVER "info@", "sales@", "rep1@"

### Step 4: Warmup Protocol
- **Duration:** 21-28 days minimum (NON-NEGOTIABLE)
- **Volume ramp:** 5-10/day → week 3 at 25-30/day
- **Target:** 30-50% reply rate within warmup network
- **Ongoing:** 10-15 warmup emails/day per mailbox indefinitely alongside production
- **Verification:** Inbox placement test (GlockApps, MXToolbox) at warmup end

### Step 5: Sending Configuration
- Inbox rotation across full mailbox pool
- 25-30 max per mailbox per day
- Spintax in all templates
- Reply detection + auto-pause on positive replies
- Send 8AM-6PM recipient local time only, avoid weekends for B2B
- Open tracking OK, click tracking may reduce deliverability

### Step 6: Monitoring Cadence
| Frequency | Action |
|-----------|--------|
| Daily | Check bounces, soft fails, spam complaints |
| Weekly | Inbox placement test, blocklist check |
| Monthly | Reputation scores (Google Postmaster, Microsoft SNDS) |
| Quarterly | Rotate underperforming mailboxes, add new ones |

### Kill-Switch Thresholds
- Bounce rate > 3%: PAUSE immediately
- Spam complaints > 0.1%: PAUSE immediately
- Inbox placement < 80%: investigate
- Sudden open rate drop: pause, investigate, restart lower volume

---

## Lead List Building

1. Build company list with specific criteria in Apollo
2. Apply keyword exclusion filters for qualification
3. Target job titles: Owner, Founder, C-Suite, VP, Head, Director + Sales, Marketing departments
4. Scrape with specialized tools (Magically Genius or Clay)
5. Verify with Millionverifier (NEVER bulk-export unverified)
6. Format personalization data with GPT for Sheets
7. Import clean, verified lists to sending platform
8. Avoid generic addresses (info@, contact@) — 30-40% bounce rates
9. Maintain suppression list for opt-outs

---

## Reply Management System

1. **Master Inbox:** All replies across all accounts funnel into one centralized inbox
2. **AI Classification:** Replies classified within 30 minutes: interested, objection, wrong timing, referral
3. **Response Speed:** Reply within minutes, not hours (doubled revenue through faster handling)
4. **Reply Templates:** Pre-built templates for <10 minute responses
5. **Meeting Conversion Target:** 30%+ of interested replies convert to meetings
6. **Sales Asset Strategy:** Create asset around offer, provide to interested leads, then call all who received it
7. **Formula:** Value First + Human Connection = Market Differentiation
8. **Subsequence Automation:** Prevent lead abandonment on non-responders

---

## Sequence Strategy

- **Optimal length:** 4-7 emails total
- 58% of all replies arrive on email 1
- Remaining 42% come from follow-ups
- Multi-touch sequences are NON-NEGOTIABLE
- Each follow-up introduces new context/angle, never repeats
- Spintax ({Hi|Hello|Hey}) to avoid bulk-send detection

### Timing
- Email 1: Day 0
- Email 2: Days 2-3
- Email 3: Days 5-7
- Email 4: Days 10-14
- Email 5: Days 18-21

---

## Email Copy Rules

- Subject line under 8 words
- Body under 80 words (50-125 optimal, 2.4x higher reply rates vs 200+)
- One sentence entirely about the recipient to open
- Lead with problem before solution
- Single binary CTA ("Does this make sense?", "Would you be interested?")
- Full signature with valid physical address (CAN-SPAM)
- P.S. line for social proof

---

## Performance Benchmarks

| Metric | Industry Average | Top Target |
|--------|-----------------|------------|
| Open Rate | 27.7% | 25-45% |
| Reply Rate | 3.43% | 5-10%+ |
| Bounce Rate | — | < 2% |
| Spam Complaint | — | < 0.1% |
| Meeting Conversion | — | 30%+ |
| Close Rate | < 15% poor | 25-35% very good |
| Emails to Deals | 0.215% | 1-5% |

---

## RevGrowth Client Results

| Client | Result |
|--------|--------|
| Zuper | $123K+ pipeline in 60 days, 66% reply-to-interested rate |
| UNIQ Supply | 485K emails, 22.45% positive reply rate, 1,987 qualified conversations |
| Aquaflex | $3.7M pipeline, 741 qualified opportunities |
| Lending Gurus | 6+ SQLs/day (up from 1), 100K+ monthly emails |
| Aggregate | $35M pipeline, 1,100+ campaigns, 47 verticals |
