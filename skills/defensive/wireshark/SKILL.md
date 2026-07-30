# Skill: Wireshark / tcpdump

## Display Filters
```
http                          — HTTP traffic
dns                           — DNS queries
tcp.port == 443               — HTTPS
ip.addr == 192.168.1.1        — specific IP
tcp.flags.syn == 1            — SYN packets (port scan)
frame contains "password"     — keyword search
http.request.method == "POST" — POST requests
```

## tcpdump (CLI)
```bash
# Capture to file
sudo tcpdump -i eth0 -w capture.pcap

# Filter by host
sudo tcpdump -i eth0 host 10.10.10.1

# Filter by port
sudo tcpdump -i eth0 port 80

# Read pcap
tcpdump -r capture.pcap -n
```

## CTF / Blue Team Patterns
- SYN flood → `tcp.flags.syn==1 && tcp.flags.ack==0` จำนวนมาก
- DNS exfil → subdomains ยาวผิดปกติ
- Credentials in cleartext → `http contains "password"` หรือ FTP/Telnet
- Beaconing → request ไป C2 สม่ำเสมอทุก X วินาที
