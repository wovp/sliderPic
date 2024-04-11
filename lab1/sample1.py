from Cryptodome.Cipher import AES
import binascii

key = b'huo2359860700000'
msg = b'0000000000000000'
cip = b'a884fb6414102347f1ffc1e16126fcd4'
aes = AES.new(key, AES.MODE_ECB)
encrypted_text = aes.encrypt(msg)
cipher = binascii.b2a_hex(encrypted_text)
if cip == cipher:
	print("Passed")
else:
	print("Failed")