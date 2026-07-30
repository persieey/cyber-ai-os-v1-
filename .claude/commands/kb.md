# Knowledge Base Manager

Action: $ARGUMENTS

## If action is "search <keyword>" or empty
Read knowledge/ctf/index.md and knowledge/techniques/ (if exists)
Find entries relevant to the keyword
Return matching entries with file paths

## If action is "add ctf <name>"
Create knowledge/ctf/<name>.md using this template:
```
# Pattern: <name>
**Source:** <CTF name> | <date>
**Category:** Web / Pwn / Rev / Crypto / Forensics / OSINT
**Difficulty:** Easy / Medium / Hard

## Summary
## Trigger Signs
## Attack
## Tools Used
```
Then add a row to knowledge/ctf/index.md

## If action is "add writeup <name>"
Create knowledge/writeups/<name>.md from workspace/active/session.md data
Use the template from templates/lab-report.md

## If action is "show"
List all entries in knowledge/ by category with file paths

Start response with:
**[Knowledge Base] [Action: <action>]**
