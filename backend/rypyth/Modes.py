from rypyth.Function import *
from rypyth.Feistel import *
import random

class Modes:
    def __init__(self, plain, key):
        self.plain = plain
        if len(key)>8:
            random.seed(key)
            self.key = ''.join(random.sample(key[:8],8))
        else:
            # key < 8 bytes
            padding = 8-len(key)
            random.seed(padding)
            temp_key=''
            while len(temp_key) < 8:
                temp_key = key + ''.join(random.sample(key,len(key)))
            self.key = temp_key[:8]
        self.bplain = change_ascii_to_bits(self.plain)
        self.bplain_encrypt = pkcs5_padding(self.bplain)
        self.bkey = change_ascii_to_bits(self.key)
    

    def ecb_encrypt(self):
        result = ''
        for i in self.bplain_encrypt:
            f = Feistel(i,self.bkey)
            result += f.encrypt()
        return result

    def ecb_decrypt(self):
        cipher_arr = split_string_into_list_of_length_n(self.bplain,128)
        result = ""
        for i in cipher_arr:
            f = Feistel(i, self.bkey)
            result += f.decrypt()
        result = last_byte_check(result)
        return result
    
    def cbc_encrypt(self):
        iv = 'rypythencryption'
        index = 0
        result = ''

        for i in self.bplain_encrypt:
            if index == 0:
                c = iv
            i = bin(int(i,2) ^ int(change_ascii_to_bits(c),2))[2:].zfill(128)
            f = Feistel(i,self.bkey)
            c = f.encrypt()
            result += c
            index += 1
        
        return result
    
    def cbc_decrypt(self):
        input_bcipher = split_string_into_list_of_length_n(self.bplain,128)
        iv = 'rypythencryption'
        index = 0
        result = ''

        for i in input_bcipher:
            f = Feistel(i,self.bkey)
            if index == 0:
                c = change_ascii_to_bits(iv)
            p = f.decrypt()
            p = bin(int(p,2) ^ int(c,2))[2:].zfill(128)
            c = i
            result += p
            index += 1

        result = last_byte_check(result)
        return result

    def cfb_encrypt(self):
        n = 1 #size of unit in bytes
        iv = 'rypythencryption'
        bitplain = ''
        for i in self.bplain_encrypt:
            bitplain += i
        bitplain = split_string_into_list_of_length_n(bitplain,(n*8))
        index = 0
        result = ''

        for i in bitplain:
            if index == 0:
                x = change_ascii_to_bits(iv)
            f = Feistel(x, self.bkey)
            c = bin(int(change_ascii_to_bits(f.encrypt()[0]),2) ^ int(i,2))[2:].zfill(n*8)
            result += c
            x = x[:(len(x)-(n*8))] + c
            index += 1
        
        result = change_bits_to_ascii(result)
        return result

    def cfb_decrypt(self):
        n = 1 #size of unit in bytes
        iv = 'rypythencryption'
        bitplain = ''
        # not using self.bplain because not using padding
        for i in self.bplain:
            bitplain += i
        bitplain = split_string_into_list_of_length_n(bitplain,(n*8))
        index = 0
        result = ''

        for i in bitplain:
            if index == 0:
                x = change_ascii_to_bits(iv)
            f = Feistel(x, self.bkey)
            c = bin(int(change_ascii_to_bits(f.encrypt()[0]),2) ^ int(i,2))[2:].zfill(n*8)
            result += c
            x = x[:(len(x)-(n*8))] + i
            index += 1

        result = last_byte_check(result)
        return result
    
    def ofb_encrypt(self):
        n = 1 #size of unit in bytes
        iv = 'rypythencryption'
        bitplain = ''
        for i in self.bplain_encrypt:
            bitplain += i
        bitplain = split_string_into_list_of_length_n(bitplain,(n*8))
        index = 0
        result = ''

        for i in bitplain:
            if index == 0:
                x = change_ascii_to_bits(iv)
            f = Feistel(x, self.bkey)
            m = change_ascii_to_bits(f.encrypt()[0])
            c = bin(int(m,2) ^ int(i,2))[2:].zfill(n*8)
            result += c
            x = x[:(len(x)-(n*8))] + m
            index += 1
        
        result = change_bits_to_ascii(result)
        return result

    def ofb_decrypt(self):
        n = 1 #size of unit in bytes
        iv = 'rypythencryption'
        bitplain = ''
        # not using self.bplain_encrypt because not using padding
        for i in self.bplain:
            bitplain += i
        bitplain = split_string_into_list_of_length_n(bitplain,(n*8))
        index = 0
        result = ''

        for i in bitplain:
            if index == 0:
                x = change_ascii_to_bits(iv)
            f = Feistel(x, self.bkey)
            m = change_ascii_to_bits(f.encrypt()[0])
            c = bin(int(m,2) ^ int(i,2))[2:].zfill(n*8)
            result += c
            x = x[:(len(x)-(n*8))] + m
            index += 1

        result = last_byte_check(result)
        return result

    def counter_encrypt(self):
        iv = 'rypythen'
        counter = int('1011000111110000101010101111111100000001000101011010111110001111',2)
        index = 0
        result = ''

        for i in self.bplain_encrypt:
            if index == 0:
                x = change_ascii_to_bits(iv) + bin(counter)[2:]
            f = Feistel(x, self.bkey)
            m = change_ascii_to_bits(f.encrypt())
            c = bin(int(m,2) ^ int(i,2))[2:].zfill(128)
            result += c
            x = change_ascii_to_bits(iv) + bin(counter + 3)[2:]
            index += 1
        
        result = change_bits_to_ascii(result)
        return result


    def counter_decrypt(self):
        iv = 'rypythen'
        counter = int('1011000111110000101010101111111100000001000101011010111110001111',2)
        index = 0
        result = ''
        bitplain = split_string_into_list_of_length_n(self.bplain, 128)

        for i in bitplain:
            if index == 0:
                x = change_ascii_to_bits(iv) + bin(counter)[2:]
            f = Feistel(x, self.bkey)
            m = change_ascii_to_bits(f.encrypt())
            c = bin(int(m,2) ^ int(i,2))[2:].zfill(128)
            result += c
            x = change_ascii_to_bits(iv) + bin(counter + 3)[2:]
            index += 1
        result = last_byte_check(result)
        return result