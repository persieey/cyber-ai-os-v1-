# Skill: DNS Enumeration

## Tools
- `dig` — DNS query tool
- `nslookup` — simple DNS lookup
- `dnsrecon` — automated DNS enumeration
- `subfinder` — passive subdomain discovery

## Commands

**Basic lookup**
```bash
dig <domain> ANY
dig <domain> A
dig <domain> MX
nslookup <domain>
```

**Zone transfer (AXFR)**
```bash
dig axfr <domain> @<nameserver>
dnsrecon -d <domain> -t axfr
```

**Subdomain bruteforce**
```bash
dnsrecon -d <domain> -D /usr/share/wordlists/dnsmap.txt -t brt
subfinder -d <domain> -silent
```

## CTF Patterns
- Zone transfer เปิด → dump ทุก record ได้เลย
- Subdomain hidden → ชี้ไป internal service
- TXT record → มี flag หรือ credential บางครั้ง
