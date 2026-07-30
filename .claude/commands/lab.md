# Lab Session — Boot2Root Entry Point

Read these files in order:
1. workspace/active/session.md — check for existing session
2. department/offensive-security/PROMPT.md — your role
3. department/offensive-security/workflows/boot2root.md — the workflow to follow

Arguments: $ARGUMENTS
(Expected format: `start <IP> <lab-name>` or `resume` or `report`)

---

## If action is "start <IP> <lab-name>"

1. Create new session in workspace/active/session.md:
   - type: Lab
   - name: <lab-name>
   - target_ip: <IP>
   - department: offensive-security
   - mode: Hint
   - phase: Recon
   - started: today's date

2. Begin Phase 1 (Recon) from boot2root.md
3. Give the nmap command to run (read skills/nmap/SKILL.md for the right command)
4. Wait for user to paste nmap output

---

## If action is "resume"

1. Read session.md → identify current phase
2. Summarize: lab name, what's done, what's pending
3. Continue from current phase in boot2root.md

---

## If action is "report"

1. Read session.md for all findings
2. Read templates/lab-report.md
3. Fill the template with data from session.md
4. Output the completed report
5. Ask: "บันทึก report ไว้ที่ workspace/outputs/[lab-name]-report.md ไหมครับ?"

---

## After each phase completes

Update session.md:
- Move completed items to Done
- Update phase to next phase
- Update Findings with new discoveries
- Update Pending with next steps

Start response with:
**[Lab] [<lab-name>] [Phase: <current_phase>] [Mode: <mode>]**
