from rypyth.Function import *
import random

class Feistel:
    def __init__(self, binary_plain, binary_key):
        if len(binary_key) != 64: raise Exception()
        self.binary_plain = binary_plain
        self.binary_key = binary_key

        self.REPETITION = 16
    
    def encrypt(self):
        lrblock = [] #tuple of left right block
        result = []
        resultbits = ''
        resultascii = ''
        lrblock.append(split_string_into_list_of_length_n(self.binary_plain,64))   

        for i in lrblock:
            for j in range(self.REPETITION):
                if j != 0:
                    random.seed(self.REPETITION-j)
                    key_feistel = ''.join(random.sample(self.binary_key,len(self.binary_key)))
                else:
                    l = i[0]
                    r = i[1]
                    key_feistel = self.binary_key
                temp = bin(int(Function(r,key_feistel).run(),2) ^ int(l,2))[2:].zfill(64)
                l = r
                r = temp  
            result.append(l)
            result.append(r)
        
        for i in result:
            resultbits += i
        resultascii = change_bits_to_ascii(resultbits)
        return resultascii

    def decrypt(self):
        lrblock = [] #tuple of left right block
        result = []
        resultascii = ''
        lrblock.append(split_string_into_list_of_length_n(self.binary_plain,64))
        
        for i in lrblock:
            l = i[0]
            r = i[1]
            for j in range(self.REPETITION-1,-1,-1):
                if j != 0:
                    random.seed(self.REPETITION-j)
                    key_feistel = ''.join(random.sample(self.binary_key,len(self.binary_key)))
                else:
                    key_feistel = self.binary_key
                temp = bin(int(Function(l,key_feistel).run(),2) ^ int(r,2))[2:].zfill(64)
                r = l
                l = temp
            result.append(l)
            result.append(r)
        for i in result:
            resultascii += i
        return resultascii

if __name__ == "__main__":
    plain  = "abcdefghijklmnopq"
    key = "abcdefgh"
    bplain = pkcs5_padding(change_ascii_to_bits(plain))
    bkey = change_ascii_to_bits(key)
    # parameter encrypt dan decrypt udh bentuk bits dan kebagi dalam block2 @64bit
    a = ""
    for i in bplain:
        f = Feistel(i,bkey)
        a += f.encrypt()
    print('hasil encrypt : ', a)
    ablock = split_string_into_list_of_length_n(change_ascii_to_bits(a),128)
    b = ""
    for i in ablock:
        f = Feistel(i,bkey)
        b += f.decrypt()
    b = last_byte_check(b)
    print('hasil decrypt : ', b)
