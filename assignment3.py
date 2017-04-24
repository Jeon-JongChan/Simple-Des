from random import *
def sdes_genkey():
    key = []
    for i in range(0,9):
        key.append(randint(0,1))
    return key
def sdes_list_xor(block1,block2):
    result = []
    for i in range(0,len(block2)):
        result.append(block1[i]^block2[i])
    return result
def sdes_compute_function(rblock,roundkey):
    extend_block = sdes_extend(rblock)
    extend_block = sdes_list_xor(extend_block,roundkey)
    r_eblock = []
    l_eblock = []
    r_eblock.extend(extend_block[4:])
    l_eblock.extend(extend_block[0:4])
    r_eblock = sdes_sbox(r_eblock)
    l_eblock = sdes_sbox(l_eblock)
    result= []
    result.extend(l_eblock)
    result.extend(r_eblock)
    return result
def sdes_extend(bit):
    j = 0;
    extend_bit = []
    for i in range(0,8):
        if i > 2 and i < 7:
            if i % 2 == 0:
                extend_bit.append(bit[3])
            else:
                extend_bit.append(bit[2])
                j = 4
        else:
            extend_bit.append(bit[j])
            j += 1
        if j > len(bit) - 1:
            break
    return extend_bit

def sdes_sbox(div_bit):
    s0 = {'000':[1,1,1],'001':[1,1,0],'010':[1,0,1],'011':[0,0,0],'100':[0,1,1],'101':[0,1,0],'110':[1,0,0],'111':[0,0,1]}
    s1 = {'000':[0,0,1],'001':[1,0,1],'010':[1,1,1],'011':[1,1,0],'100':[0,1,0],'101':[0,1,1],'110':[0,0,0],'111':[1,0,0]}
    index = ''
    for i in div_bit[1:]:
        index += str(i)
    if div_bit[0] == 0:
        trans_bit = s0[index]
    else:
        trans_bit = s1[index]
    return trans_bit

def sdes_keyskedule(key,roundnum):
    roundkey = []
    n = roundnum
    for i in range(8):
        if n < 9:
            roundkey.append(key[n])
        else:
            n = 0
            roundkey.append(key[n])
        n += 1
    return roundkey

def sdes_encrypt(bit,key,roundlimit = 3):
    rblock = []
    lblock = []
    lblock.extend(bit[0:6])
    rblock.extend(bit[6:])
    for roundnum in range(1,roundlimit+1):
        roundkey = sdes_keyskedule(key,roundnum)
        fblock = sdes_compute_function(rblock,roundkey)
        result = sdes_list_xor(lblock,fblock)
        lblock = rblock[:]
        rblock = result[:]
    bit = lblock + rblock
    return bit
def sdes_decrypt(bit,key,roundlimit = 3):
    rblock = []
    lblock = []
    lblock.extend(bit[0:6])
    rblock.extend(bit[6:])
    while roundlimit > 0:
        roundkey = sdes_keyskedule(key,roundlimit)
        fblock = sdes_compute_function(lblock,roundkey)
        result = sdes_list_xor(rblock,fblock)
        rblock = lblock[:]
        lblock = result[:]
        roundlimit -= 1
    bit = lblock + rblock
    return bit
key = sdes_genkey()
bit = [0,1,1,0,1,1,1,1,1,0,0,0]
enc_bit = sdes_encrypt(bit,key)
print(enc_bit)
dec_bit = sdes_decrypt(enc_bit,key)
print(dec_bit)
