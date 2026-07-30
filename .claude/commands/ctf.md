# CTF Challenge Entry Point

Read these files in order:
1. workspace/active/session.md — check for existing session
2. department/offensive-security/PROMPT.md — your role
3. knowledge/ctf/index.md — scan for relevant patterns

Arguments: $ARGUMENTS
(Expected format: `start <challenge-name> <category>` | `resume` | `report`)

---

## If action is "start <challenge-name> <category>"

Categories: web | crypto | forensics | rev | pwn | osint | misc

1. Create new session in workspace/active/session.md:
   - type: CTF
   - name: <challenge-name>
   - department: offensive-security
   - mode: Hint
   - target: <URL or "binary" or "file">
   - category: <category>
   - phase: Analysis
   - started: today's date

2. Read the appropriate workflow based on category:
   - web       → department/offensive-security/workflows/web-exploitation.md
   - crypto    → department/offensive-security/workflows/cryptography.md
   - forensics → department/offensive-security/workflows/forensics.md
   - rev / pwn → department/offensive-security/workflows/reverse-engineering.md

3. Search knowledge/ctf/index.md for relevant patterns

4. Begin Phase 1 from the workflow
   - web: whatweb + gobuster
   - crypto: identify cipher type
   - forensics: file + exiftool + strings + binwalk
   - rev: file + checksec + strings

5. Ask: mode? Hint (default) / Guided / Walkthrough / Full Solution?

---

## If action is "resume"

1. Read session.md → identify current phase and category
2. Load appropriate workflow for the category
3. Summarize: challenge name, category, what's done, what's pending
4. Continue from current phase

---

## If action is "report"

1. Read session.md for all findings
2. Read templates/lab-report.md
3. Fill template with CTF-specific format
4. Output completed report
5. Ask: "บันทึก writeup ใน knowledge/writeups/<name>.md ไหม?"
6. Ask: "มี pattern ใหม่ที่ต้องเพิ่มใน /kb ไหม?"

---

## After each phase completes

Update session.md:
- Move completed items to Done
- Update phase to next phase
- Update Findings with discoveries
- Update Pending with next steps

Also: ถ้าพบ pattern ที่น่าจำ → แนะนำ "/kb add ctf <name>"

Start response with:
**[CTF] [<challenge-name>] [Category: <category>] [Phase: <current_phase>] [Mode: <mode>]**
