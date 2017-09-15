import zlib
import base64
import Crypto.PublicKey import RSA
import Crypto.Cipher import PKCS1_OAEP

private_key = "YOUR_PRIVATE_KEY"
rsakey = RSA.importKey(private_key)
rsakey = PKCS1_OAEP.new(rsakey)

chunk_size = 256
offset = 0
decrypted = ""
encrypted = "ENCODED_STRING"
encrypted = base64.b64decode(encrypted)

while offset < len(encrypted):
    decrypted += rsakey.decrypt(encrypted[offset:offset+chunk_size])
    offset += chunk_size

# decompress to original
plaintext = zlib.decompress(decrypted)

print plaintext