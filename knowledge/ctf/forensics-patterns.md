# CTF Forensics Patterns

## File Analysis (Always First)
```bash
file suspicious
exiftool suspicious          # metadata
strings suspicious | head -50
binwalk suspicious           # embedded files
xxd suspicious | head -20    # hex dump
```

## Image Forensics

### Steganography
```bash
steghide extract -sf image.jpg    # extract hidden file (may need password)
stegoveritas image.jpg            # auto-detect stego
zsteg image.png                   # LSB stego in PNG
strings image.png | grep flag
exiftool image.jpg | grep -i comment
```

### LSB Manual (PNG)
```python
from PIL import Image
img = Image.open("image.png")
pixels = list(img.getdata())
bits = [px[0] & 1 for px in pixels]  # LSB of red channel
# Convert bits to bytes → string
```

### Image in Image
```bash
# Compare two images
compare img1.png img2.png diff.png
# Stacking: XOR two images
```

## PCAP Analysis
```bash
wireshark capture.pcap        # GUI
tcpdump -r capture.pcap -n    # CLI

# Extract files from pcap
binwalk capture.pcap
foremost -i capture.pcap -o output/

# tshark (CLI wireshark)
tshark -r capture.pcap -Y "http" -T fields -e http.request.uri
tshark -r capture.pcap -Y "ftp-data" -z follow,tcp,ascii,0
```

## Disk / Memory

### Disk (FTK Imager / Autopsy)
```bash
# Mount image
sudo mount -o loop,ro disk.img /mnt/disk

# Deleted files
foremost -i disk.img -o recovered/
photorec disk.img

# File system
fsstat disk.img
fls -r disk.img  # file listing
icat disk.img <inode>  # read by inode
```

### Memory (Volatility)
```bash
vol.py -f mem.dmp imageinfo
vol.py -f mem.dmp pslist
vol.py -f mem.dmp filescan | grep flag
vol.py -f mem.dmp dumpfiles -Q 0x<addr> -D output/
vol.py -f mem.dmp clipboard  # Windows clipboard
vol.py -f mem.dmp screenshot -D output/
```

## Office / PDF / Archives
```bash
# Office macros
olevba malicious.docx
oletools malicious.xlsm

# PDF
pdf-parser.py suspicious.pdf
pdfextract suspicious.pdf

# Password-protected zip
john --wordlist=rockyou.txt hash.txt  # after zip2john
fcrackzip -u -D -p rockyou.txt archive.zip
```

## Common Flag Locations
- Image EXIF comment
- File appended after EOF (`strings file | tail`)
- Hidden in white pixels (LSB)
- Inside zip inside image (`binwalk`)
- PCAP HTTP response body
- Memory: clipboard, process memory, screenshot
