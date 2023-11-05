import binascii

shex="0x1234"
bhex=binascii.unhexlify(shex[2:])

print(bhex.hex())
