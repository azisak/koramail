from rypyth.Modes import *
from rypyth.Feistel import *

def encrypt_message(message, key):
    m = Modes(message, key)
    encrypted = m.cbc_encrypt()
    temp = []
    for i in split_string_into_list_of_length_n(change_ascii_to_bits(encrypted),8):
        temp.append(int(i,2))
    encrypted = bytes(temp)

    return encrypted

def decrypt_message(encrypted, key):
    m = Modes(encrypted, key)
    decrypted = m.cbc_decrypt()

    return decrypted