def rot(a, n):
    return ((a >> (64-(n%64))) + (a << (n%64))) % (1 << 64)

def load(b):
    sum = 0
    for i in range(8):
        sum += b[i] << (8*i)
    return sum

def store(a):
    l = list()
    for i in range(8):
        l.append((a >> (8*i)) % 256)
    return l

# permutation
def permutation(path):
    R = 1
    # 24 round because 1600
    for round in range(24):
        # θ
        C = list()
        for x in range(5):
            C.append(path[x][0] ^ path[x][1] ^ path[x][2] ^ path[x][3] ^ path[x][4])
        D = list()
        for x in range(5):
            D.append(C[(x+4)%5] ^ rot (C[(x+1)%5],1))
        temppath = list()
        for x in range(5):
            temp = list()
            for y in range(5):
                temp.append(path[x][y]^D[x])
            temppath.append(temp)
        path = temppath    

        # ρ and π
        (x, y) = (1, 0)
        current = path[x][y]
        for t in range(24):
            (x, y) = (y, (2*x+3*y)%5)
            (current, path[x][y]) = (path[x][y], rot(current, (t+1)*(t+2)//2))
            
        # χ
        for y in range(5):
            T = list()
            for x in range(5):
                T.append(path[x][y])
            for x in range(5):
                path[x][y] = T[x] ^((~T[(x+1)%5]) & T[(x+2)%5])

        # ι
        for j in range(7):
            R = ((R << 1) ^ ((R >> 7)*0x71)) % 256
            if (R & 2):
                path[0][0] = path[0][0] ^ (1 << ((1<<j)-1))
    return path

def keccak1600(s):
    temppath = list()
    for x in range(5):
        temp = list()
        for y in range(5):
            temp.append(load(s[8*(x+5*y):8*(x+5*y)+8]))
        temppath.append(temp)
    path = temppath

    path = permutation(path)
    s = bytearray(200)
    for x in range(5):
        for y in range(5):
            s[8*(x+5*y):8*(x+5*y)+8] = store(path[x][y])
    return s

def keccak(rate, capacity, input, delimitedSuffix, outputlen):
    output = bytearray()
    state = bytearray([0 for i in range(200)])
    ratebytes = rate//8 #rate every 8 bits ( 1 byte )

    blocksize = 0 

    if (((rate + capacity) != 1600) or ((rate % 8) != 0)):
        return

    inputoffset = 0

    # absorb phase
    while(inputoffset < len(input)):
        blocksize = min(len(input)-inputoffset, ratebytes)

        for i in range(blocksize):
            state[i] = state[i] ^ input[i+inputoffset]

        inputoffset = inputoffset + blocksize
        if (blocksize == ratebytes):
            state = keccak1600(state)
            blocksize = 0


    # padding
    state[blocksize] = state[blocksize] ^ delimitedSuffix
    if (((delimitedSuffix & 0x80) != 0) and (blocksize == (ratebytes-1))):
        state = keccak1600(state)
    state[ratebytes-1] = state[ratebytes-1] ^ 0x80

    state = keccak1600(state)

    # squeeze phase
    while(outputlen > 0):
        blocksize = min(outputlen, ratebytes)
        output = output + state[0:blocksize]
        outputlen = outputlen - blocksize
        if (outputlen > 0):
            state = keccak1600(state)  
    return output

def SHA3_512(input):
    return keccak(576, 1024, input, 0x06, 512//8)