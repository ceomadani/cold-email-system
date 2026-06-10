# Cold Email Infrastructure — Setup Checklist

## Pre-Launch (4-6 settimane prima)

### Settimana 1: Domini
- [ ] Scegliere 4-8 variazioni dominio (es. `trymadani.com`, `getmadani.com`, `madani.io`)
- [ ] Registrare domini (Cloudflare, Namecheap, Google Domains)
- [ ] Verificare che non siano in blacklist (MXToolbox)

### Settimana 2: DNS + Mailbox
- [ ] Configurare SPF per ogni dominio
- [ ] Configurare DKIM (2048-bit) per ogni dominio
- [ ] Configurare DMARC (`p=none` iniziale)
- [ ] Creare 2-3 mailbox per dominio con nomi reali
- [ ] Aggiungere foto profilo + firma a ogni mailbox
- [ ] Verificare headers con test email (SPF=pass, DKIM=pass, DMARC=pass)

### Settimana 3-4: Warmup
- [ ] Connettere tutte le mailbox a piattaforma warmup
- [ ] Settare volume: 5-10/giorno, ramp graduale
- [ ] Monitorare reply rate warmup (target: 30-50%)
- [ ] NON inviare email di produzione durante warmup

### Settimana 5: Verifica
- [ ] Inbox placement test per ogni mailbox (GlockApps)
- [ ] Blocklist check per ogni dominio
- [ ] Reputation check (Google Postmaster Tools se Gmail, Microsoft SNDS se Outlook)
- [ ] Se tutto OK → pronto per produzione

## Produzione

### Sending
- [ ] Configurare inbox rotation nella piattaforma
- [ ] Max 25-30 invii/giorno per mailbox
- [ ] Send window: 8:00-18:00 fuso destinatario
- [ ] NO weekend per B2B
- [ ] Spintax attivo in tutti i template
- [ ] Auto-pause su positive reply attivo

### Monitoring Quotidiano
- [ ] Bounce rate < 2% (STOP se > 3%)
- [ ] Spam complaints < 0.1% (STOP se > 0.1%)
- [ ] Open rate stabile (flag se drop improvviso)

### Suppression List
- [ ] Mantenere lista opt-out aggiornata
- [ ] Importare bounce hard come suppression
- [ ] MAI re-contattare chi ha chiesto di non essere contattato

## Tool Stack Consigliato

| Layer | Tool | Costo |
|-------|------|-------|
| Sending | Smartlead.ai / Instantly.ai | $30-100/mese |
| Verification | Millionverifier / Zerobounce | Pay-per-use |
| Warmup | Integrato in Smartlead / Mailreach | Incluso o $10-25/mese |
| Enrichment | Clay / Apollo / pipeline_v4.py custom | Varia |
| Inbox Placement | GlockApps | $60/mese |
| Reputation | Google Postmaster / Microsoft SNDS | Gratis |

## DNS Records Template

### SPF (Google Workspace)
```
Type: TXT
Name: @
Value: v=spf1 include:_spf.google.com ~all
```

### SPF (Microsoft 365)
```
Type: TXT
Name: @
Value: v=spf1 include:spf.protection.outlook.com ~all
```

### DMARC (Starter)
```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=none; rua=mailto:dmarc@tuodominio.com; pct=100; aspf=r; adkim=r;
```

### DMARC (After 4-6 weeks)
```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@tuodominio.com; pct=100; aspf=r; adkim=r;
```
