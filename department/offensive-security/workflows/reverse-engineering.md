# Reverse Engineering CTF Workflow

## Purpose
แนวทางทำ Reverse Engineering CTF challenge อย่างมีระบบ ตั้งแต่ static analysis จนถึงหา flag หรือ bypass protection

## Phases

---

### Phase 1: Identify Binary
**Goal:** เข้าใจ binary ที่ได้มา

```bash
file <binary>              # ELF/PE/script/etc.
checksec --file=<binary>   # protections: PIE, NX, ASLR, Canary
strings <binary>           # readable strings → หา hardcoded values
strings <binary> | grep -E "flag|CTF|pass|key|correct|wrong"
```

Summary ที่ต้องรู้:
- Architecture: x86 / x86-64 / ARM
- Protections: NX? Canary? PIE?
- ภาษา/compiler: C, C++, Go, Rust

Done when: รู้ว่า binary ทำอะไร เชิงกว้าง

---

### Phase 2: Static Analysis
**Goal:** อ่าน logic ของ program โดยไม่ต้องรัน

#### Quick Wins
```bash
strings <binary> | head -50      # hardcoded strings
ltrace ./<binary> <<< "test"     # library calls (strcmp ?)
strace ./<binary> <<< "test"     # system calls
```

#### objdump
```bash
objdump -d <binary> | grep -A 30 "<main>"
objdump -d <binary> | grep -B 5 "cmp\|je\|jne\|jl"
```

#### Ghidra (เมื่อต้องการ decompile)
```
1. New Project → Import File
2. Auto Analyze → OK
3. Functions → main() → Decompiler
4. สิ่งที่ต้องหา:
   - strcmp(), strncmp() → password check
   - XOR loop → encryption
   - Magic number comparison
   - Flag construction logic
```

Done when: เข้าใจ logic หลักของ program

---

### Phase 3: Dynamic Analysis
**Goal:** รัน binary และสังเกต behavior จริง

```bash
gdb <binary>
run                    # รันปกติ
break main             # หยุดที่ main
next (n)               # step over
step (s)               # step into
info registers         # ดู register values
x/s <address>          # ดู string ที่ address
```

**Pattern ที่มักพบใน CTF Rev:**

```
strcmp กับ input:
→ ltrace ./<binary> → เห็น: strcmp("input", "correct_answer")
→ ใช้ correct_answer เป็น input

XOR decryption:
→ Ghidra เห็น loop XOR
→ เขียน Python ถอดรหัส

Password ใน binary:
→ strings <binary> | grep -v "^[A-Z_]" | grep -E ".{6,}"
→ ลอง string ที่ยาวกว่า 6 ตัวอักษร

Flag constructed:
→ เห็น flag ถูกสร้างจากหลาย parts
→ trace ค่าแต่ละส่วน
```

Done when: ได้ flag หรือ input ที่ถูกต้อง

---

### Phase 4: Common Bypasses

#### Packed Binary
```bash
# ตรวจ packing
file <binary>   # บอกว่า "UPX compressed"
# Unpack
upx -d <binary>
```

#### Anti-debugging
```python
# ใน gdb: เปลี่ยน return value ของ ptrace
(gdb) catch syscall ptrace
(gdb) commands
> set $rax = 0
> continue
> end
```

#### License/Serial Check
```bash
# หา comparison ใน disassembly
objdump -d <binary> | grep -B 10 "call.*strcmp"
# Patch je → jne (หรือกลับกัน)
```

---

### Phase 5: Documentation
1. อัพเดต `workspace/active/session.md` → Findings, Done
2. บันทึก technique ใน `/kb add ctf <technique>`
3. รัน Report Agent

---

## Quick Reference

```
Phase 1  file + checksec + strings
Phase 2  ltrace + strace → Ghidra/objdump
Phase 3  gdb → trace execution
Phase 4  unpack + patch (ถ้าจำเป็น)
Phase 5  บันทึก → writeup
```

## CTF Rev Patterns

| สัญญาณ | Technique |
|--------|-----------|
| `ltrace` เห็น strcmp | copy argument เป็น input |
| XOR loop ใน Ghidra | เขียน Python XOR key |
| `file` บอก UPX | `upx -d <binary>` |
| Magic bytes comparison | หาค่าใน Ghidra |
| Multiple flag parts | trace แต่ละส่วน |
