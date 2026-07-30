# Skill: Zeek (Network Security Monitor)

## Log Files
| File | เนื้อหา |
|------|---------|
| `conn.log` | TCP/UDP connections (src, dst, bytes, duration) |
| `dns.log` | DNS queries + responses |
| `http.log` | HTTP requests (method, host, uri, user-agent) |
| `ssl.log` | TLS connections (cert info) |
| `files.log` | files transferred over network |
| `weird.log` | anomalies detected by Zeek |

## zeek-cut (Query Logs)
```bash
# Top talkers
zeek-cut id.orig_h id.resp_h bytes < conn.log | sort -k3 -rn | head

# DNS queries
zeek-cut query < dns.log | sort | uniq -c | sort -rn

# HTTP user agents
zeek-cut user_agent < http.log | sort | uniq -c | sort -rn

# Long connections (potential C2 beaconing)
zeek-cut id.orig_h id.resp_h duration < conn.log | awk '$3 > 3600'
```

## Threat Detection Patterns
```bash
# DNS exfiltration — long subdomains
zeek-cut query < dns.log | awk 'length($1) > 50'

# Beaconing — same dest repeated
zeek-cut id.orig_h id.resp_h < conn.log | sort | uniq -c | sort -rn | head

# Non-standard port for HTTP
zeek-cut id.resp_p method < http.log | grep -v "^80\|^8080\|^443"
```
