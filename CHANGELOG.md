# Changelog

## v1.1.0 — 2026-07-30
**Cybersecurity Department Complete**

### Added
- `malware-analysis` department: 3 roles, 1 workflow, 4 skills (strings/pestudio/ghidra/cuckoo)
- `cloud-security` department: 3 roles, 1 workflow, 4 skills (aws-cli/scout-suite/pacu/trivy)
- `mobile-security` department: 3 roles, 1 workflow, 5 skills (apktool/jadx/adb/frida/objection)
- Skills: pwntools, python-exploit, hashcat
- Commands: `/ir`, `/hunt`, `/harden`, `/malware`
- Knowledge base: crypto-patterns, rev-patterns, forensics-patterns, ir-playbooks, threat-hunting-hypotheses, common-families
- `tools/` automation scripts: 11 scripts across recon/ctf/exploitation/utils/reporting

### Changed
- CLAUDE.md: v1.1.0, all 7 departments documented
- Coordinator: routing rules + classifier updated for new departments
- Codebase: zero broken references (full audit pass)

---

## v1.0.0 — 2026-07-30
**Full Architecture Complete**

### Added
- `defensive-security` department: 4 roles (soc-analyst, incident-responder, threat-hunter, hardening-specialist)
- Skills: splunk, elastic, wireshark, zeek, volatility, yara
- `skills/network/dns/SKILL.md`
- Templates: `ctf-writeup.md`, `pentest-report.md`

### Changed
- All 3 Department Agents: role table paths fixed to full project-root paths
- CLAUDE.md: v1.0.0

---

## v0.3.0 — 2026-07-30
**Sprint 12 — Architecture Refactor Complete**

### Added
- Department Agent architecture: Coordinator → Dept Agent → Role → Skill
- `offensive-security` Department Agent v2: 8 roles, 5 workflows
- `learning` Department Agent v2: 3 roles
- `reporting` Department Agent v2: 2 roles
- Skills reorganized into categories: network/, web/, exploitation/, scripting/
- `department/coordinator/manifest.yaml` v2.0.0

### Removed
- 21 legacy flat agents (Sprint 11) → replaced by Department Agents
- Old flat skill folders: nmap/, gobuster/, sqlmap/, ffuf/, john/

---

## v0.2.0 — Sprint 11
**21 Flat Agents**
- lab-manager, recon, enumeration, web-pentest, linux-privesc, windows-ad
- reverse-engineering, report, learning-coach, knowledge-manager
- coding, tool-expert, research, malware-analysis, digital-forensics
- cloud-security, mobile-security, exploit-dev, crypto, osint, bug-bounty

---

## v0.1.0 — Sprint 10
**Foundation**
- CLAUDE.md Coordinator
- department/coordinator/ (TASK_CLASSIFIER, MODES, ROUTING_RULES, CHECKLIST)
- workspace/ structure
- knowledge/ structure
- Templates, session schema
