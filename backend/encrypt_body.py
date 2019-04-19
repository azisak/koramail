from rypyth.Modes import *
from rypyth.Feistel import *

def encrypt_message(message, key):
    m = Modes(message, key)
    encrypted = m.cbc_encrypt()

    return encrypted

def decrypt_message(encrypted, key):
    m = Modes(encrypted, key)
    decrypted = m.cbc_decrypt()

    return decrypted