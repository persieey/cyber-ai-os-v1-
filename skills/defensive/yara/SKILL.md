# Skill: YARA

## Rule Structure
```yara
rule RuleName {
    meta:
        description = "Detects malware X"
        author = "analyst"

    strings:
        $s1 = "malicious_string"
        $s2 = { 4D 5A 90 00 }  // hex bytes
        $r1 = /evil[0-9]+\.exe/ // regex

    condition:
        uint16(0) == 0x5A4D and   // MZ header
        filesize < 1MB and
        any of ($s*)
}
```

## Run YARA
```bash
# Scan file
yara rule.yar suspicious.exe

# Scan directory
yara -r rule.yar /path/to/scan/

# Scan process memory
yara rule.yar /proc/*/exe 2>/dev/null

# Multiple rules
yara rules/*.yar target/
```

## Common Conditions
```yara
filesize < 500KB
uint16(0) == 0x5A4D          // PE file (MZ)
uint32(0) == 0x464C457F      // ELF file
at entrypoint               // check at entry point
```

## Resources
- YARA rules: https://github.com/Yara-Rules/rules
- Malware bazaar: download samples + rules
