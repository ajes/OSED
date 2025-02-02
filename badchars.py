badchars = "badchars = (\n"
for i in range(0x00, 0x100, 16):
    badchars += "\tb\"" + "".join([f"\\x{hex(j)[2:].zfill(2)}" for j in range(i, i + 16)]) + "\"\n"
badchars += ")"
print(badchars)

