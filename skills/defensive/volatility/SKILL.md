# Skill: Volatility (Memory Forensics)

## Setup
```bash
# Volatility 3
python3 vol.py -f memory.dmp <plugin>

# Identify OS profile (Vol 2)
vol.py -f memory.dmp imageinfo
```

## Essential Plugins

**Process Analysis**
```bash
vol.py -f mem.dmp windows.pslist    # process list
vol.py -f mem.dmp windows.pstree   # process tree
vol.py -f mem.dmp windows.cmdline  # command line args
vol.py -f mem.dmp windows.dlllist  # DLLs per process
```

**Network**
```bash
vol.py -f mem.dmp windows.netscan  # active connections
```

**Malware Detection**
```bash
vol.py -f mem.dmp windows.malfind       # injected code
vol.py -f mem.dmp windows.hollowfind   # process hollowing
vol.py -f mem.dmp windows.vadinfo      # virtual address descriptors
```

**Dump**
```bash
vol.py -f mem.dmp windows.dumpfiles --pid <PID>  # dump process files
vol.py -f mem.dmp windows.memmap --dump --pid <PID>
```

## CTF Patterns
- `malfind` → process inject มักมี MZ header
- Suspicious parent → `cmd.exe` spawn จาก `word.exe`
- Hidden process → อยู่ใน `vadinfo` แต่ไม่อยู่ใน `pslist`
