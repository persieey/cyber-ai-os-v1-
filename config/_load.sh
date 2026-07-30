#!/bin/bash
# config/_load.sh — Source this file to load config/tools.yaml into shell vars
# Usage: source config/_load.sh

CONFIG="$(dirname "$0")/../config/tools.yaml"
[ ! -f "$CONFIG" ] && CONFIG="config/tools.yaml"

if command -v python3 &>/dev/null; then
  eval "$(python3 - "$CONFIG" <<'PYEOF'
import sys, yaml

try:
    c = yaml.safe_load(open(sys.argv[1]))
    print(f'LHOST="{c.get("lhost", "10.10.14.1")}"')
    print(f'LPORT="{c.get("lport", 4444)}"')
    print(f'INTERFACE="{c.get("interface", "tun0")}"')
    wl = c.get("wordlists", {})
    print(f'WL_PASSWORD="{wl.get("password", "/usr/share/wordlists/rockyou.txt")}"')
    print(f'WL_DIRECTORY="{wl.get("directory", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt")}"')
    print(f'WL_DNS="{wl.get("dns", "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt")}"')
    ws = c.get("workspace", {})
    print(f'WS_ACTIVE="{ws.get("active", "workspace/active")}"')
    print(f'WS_OUTPUTS="{ws.get("outputs", "workspace/outputs")}"')
except Exception as e:
    # Fallback defaults
    print('LHOST="10.10.14.1"')
    print('LPORT="4444"')
    print('INTERFACE="tun0"')
    print('WL_PASSWORD="/usr/share/wordlists/rockyou.txt"')
    print('WL_DIRECTORY="/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"')
    print('WL_DNS="/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"')
    print('WS_ACTIVE="workspace/active"')
    print('WS_OUTPUTS="workspace/outputs"')
PYEOF
)"
else
  # No Python — use grep fallback for top-level keys
  _cfg_get() { grep "^$1:" "$CONFIG" 2>/dev/null | cut -d: -f2- | tr -d ' "'; }
  LHOST=$(_cfg_get lhost)
  LPORT=$(_cfg_get lport)
  INTERFACE=$(_cfg_get interface)
  WL_PASSWORD="/usr/share/wordlists/rockyou.txt"
  WL_DIRECTORY="/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
  WL_DNS="/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
  WS_ACTIVE="workspace/active"
  WS_OUTPUTS="workspace/outputs"
fi

export LHOST LPORT INTERFACE WL_PASSWORD WL_DIRECTORY WL_DNS WS_ACTIVE WS_OUTPUTS
