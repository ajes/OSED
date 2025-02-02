#!/usr/bin/env python3
"""
This script creates the default theme for WinDBG in the Windows Registry.
The generated registry file should be merged into the system registry.

Idea copied from: https://ltops9.wordpress.com/2014/08/29/customizing-and-sharing-windbgs-theme-how-to-heres-a-quick-note/

Usage:
    python theme_default.py <input_file>

Example:
    python theme_default.py dark-green-x64.wew
"""

import binascii
import sys

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python theme_default.py <input_file>")
    sys.exit(1)

fileName = sys.argv[1]

# Read the input file in binary mode
with open(fileName, 'rb') as f:
    content = f.read()

# Convert binary data to a hexadecimal string representation
data = binascii.hexlify(content).decode('ascii')

# Create the registry file
regFileName = fileName + '.reg'
with open(regFileName, 'w') as fileOut:
    fileOut.write('Windows Registry Editor Version 5.00\n\n')
    fileOut.write('[HKEY_CURRENT_USER\\Software\\Microsoft\\Windbg]\n\n')
    fileOut.write('[HKEY_CURRENT_USER\\Software\\Microsoft\\Windbg\\Workspaces]\n\n')
    fileOut.write('"Default"=hex:' + data[0] + data[1])
    x = 2
    while x < len(data):
        fileOut.write(',' + data[x] + data[x+1])
        x += 2

print("Registry file created:", regFileName)
print("To merge the registry file, double-click it or run the following command:")
print('  regedit /s "{}"'.format(regFileName))
