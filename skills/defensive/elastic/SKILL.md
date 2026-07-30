# Skill: Elastic / ELK Stack

## Components
- **Elasticsearch** — storage + search
- **Logstash** — ingest + parse
- **Kibana** — visualize
- **Beats** — lightweight shippers (Filebeat, Winlogbeat, Packetbeat)

## KQL (Kibana Query Language)
```kql
event.code: 4625                          -- failed login
process.name: "powershell.exe"
source.ip: 192.168.1.0/24
event.category: "authentication" and event.outcome: "failure"
NOT destination.port: 443
```

## Elasticsearch Query DSL
```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "event.code": "4625" } },
        { "range": { "@timestamp": { "gte": "now-24h" } } }
      ]
    }
  },
  "aggs": {
    "by_ip": { "terms": { "field": "source.ip" } }
  }
}
```

## Common Detections
```kql
# Brute force
event.code: 4625 | stats count by source.ip | where count > 20

# Mimikatz
process.command_line: *sekurlsa* or *lsadump*

# PowerShell encoded command
process.command_line: *-enc* and process.name: powershell.exe
```
