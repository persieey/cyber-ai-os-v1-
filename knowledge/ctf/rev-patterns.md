# CTF Reverse Engineering Patterns

## First Steps (Always)
```bash
file binary
checksec --file=binary
strings binary | grep -E "flag|correct|wrong|password|key"
ltrace ./binary       # library calls
strace ./binary       # syscalls
```

## Common CTF Patterns

### strcmp / password check
```
ltrace → strcmp("input", "s3cr3t_p4ss")
→ copy second argument → flag
```

### XOR decode
```python
# Ghidra decompile → เห็น XOR loop
enc = [0x41, 0x42, ...]
key = 0x13
flag = bytes([b ^ key for b in enc])
```

### Base64 in binary
```bash
strings binary | grep -E "^[A-Za-z0-9+/]{20,}={0,2}$"
echo "SGVsbG8=" | base64 -d
```

### Anti-debug bypass
```bash
# ptrace check → patch binary
# gdb: set follow-fork-mode child
# strace → ดู ptrace(PTRACE_TRACEME)
# patch: nop out the check
```

### UPX packed
```bash
strings binary | grep UPX
upx -d binary -o unpacked
# แล้ว analyze unpacked
```

### Angr (symbolic execution)
```python
import angr
proj = angr.Project('./binary', auto_load_libs=False)
state = proj.factory.entry_state(args=['./binary'])
simgr = proj.factory.simgr(state)
simgr.explore(find=0x401234, avoid=0x401500)  # find=success, avoid=fail
print(simgr.found[0].posix.dumps(0))  # stdin that reaches success
```

### z3 (constraint solving)
```python
from z3 import *
x = Int('x')
s = Solver()
s.add(x * 3 + 7 == 22)
s.check()
print(s.model()[x])
```

## Useful Tools
| Tool | ใช้เมื่อ |
|------|---------|
| Ghidra | Decompile C |
| IDA Free | Professional disassembler |
| GDB + peda/pwndbg | Dynamic debug |
| ltrace/strace | Quick behavior check |
| angr | Path exploration |
| z3 | Constraint solving |
| pwntools | Interact with binary |
