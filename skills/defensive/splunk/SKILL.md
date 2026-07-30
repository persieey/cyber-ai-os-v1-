# Skill: Splunk

## Basic Search
```splunk
index=<index> sourcetype=<type> keyword
| fields src_ip, dest_ip, action
| stats count by src_ip
| sort -count
```

## Common Queries

**Failed login (Windows)**
```splunk
index=security EventCode=4625
| stats count by src_ip, Account_Name
| where count > 10
```

**Privilege escalation**
```splunk
index=security EventCode=4672
| stats count by Account_Name, Privileges
```

**Network connections**
```splunk
index=network dest_port=443 OR dest_port=80
| stats dc(dest_ip) as unique_dests by src_ip
| where unique_dests > 100
```

**Data exfiltration**
```splunk
index=proxy bytes_out > 10000000
| stats sum(bytes_out) as total by src_ip
| sort -total
```

## Time Functions
```splunk
earliest=-24h latest=now
earliest=-7d@d latest=@d
```
