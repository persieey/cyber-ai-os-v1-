# Threat Hunting Entry Point

Read these files in order:
1. `workspace/active/session.md` — check for existing hunt session
2. `department/defensive-security/workflows/threat-hunting.md` — hunting workflow
3. `department/defensive-security/roles/threat-hunter.md` — your role

Arguments: $ARGUMENTS
(Expected: `start <hypothesis>` | `ioc <indicator>` | `mitre <technique-id>` | `resume` | `report`)

---

## If action is "start <hypothesis>"
1. Create session in `workspace/active/session.md`:
   - type: Threat Hunt
   - hypothesis: <hypothesis>
   - department: defensive-security
   - phase: Data Collection
   - started: today's date

2. Load hunting workflow
3. Identify data sources needed for this hypothesis
4. Provide initial queries (Splunk/KQL/zeek-cut based on available data)

---

## If action is "ioc <indicator>"
1. Identify IOC type: IP / domain / hash / file path / registry key
2. Generate search queries for common data sources:
   - Splunk / ELK
   - Zeek logs
   - Windows Event Logs
3. Ask: "มี data source ไหนที่ search ได้?"

---

## If action is "mitre <technique-id>"
1. Look up technique (e.g., T1059, T1078)
2. Describe what artifacts this technique leaves
3. Generate hunting queries targeting those artifacts

---

## If action is "resume"
Read session.md → continue from current phase

---

## If action is "report"
Generate Hunt Report:
- Hypothesis | Data Sources | Queries Used | Findings | Verdict | New Detections

Start response with:
**[Threat Hunt] [Hypothesis: <short>] [Phase: <phase>]**
