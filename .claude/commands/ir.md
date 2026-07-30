# Incident Response Entry Point

Read these files in order:
1. `workspace/active/session.md` — check for existing IR session
2. `department/defensive-security/workflows/incident-response.md` — IR workflow
3. `department/defensive-security/roles/incident-responder.md` — your role

Arguments: $ARGUMENTS
(Expected: `start <incident-type> <hostname>` | `resume` | `report`)

---

## If action is "start <incident-type> <hostname>"

Incident types: ransomware | breach | intrusion | phishing | malware | ddos

1. Create session in `workspace/active/session.md`:
   - type: Incident Response
   - incident_type: <type>
   - hostname: <hostname>
   - department: defensive-security
   - phase: Identification
   - started: today's date
   - severity: [Critical/High/Medium/Low]

2. Load `department/defensive-security/workflows/incident-response.md`
3. Begin Phase 1: Identification
4. Ask: "มีข้อมูลเพิ่มเติมไหม? (alerts, logs, screenshots)"

---

## If action is "resume"
1. Read session.md → current phase + incident type
2. Summarize: what's done, what's pending
3. Continue from current phase

---

## If action is "report"
1. Read session.md → all findings
2. Read `templates/pentest-report.md` → adapt for IR
3. Generate: Timeline | Root Cause | Impact | Remediation | Lessons Learned
4. Ask: "บันทึก report ไว้ที่ workspace/outputs/<hostname>-ir-report.md ไหม?"

---

Start response with:
**[IR] [<incident-type>] [Host: <hostname>] [Phase: <phase>] [Severity: <severity>]**
