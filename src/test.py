import sys


if False:
    print("no")
elif (c=(True)):
    print('blah')

if False:
    print("no")
elif (d=(True)):
    print(d)

    '''
def AND(abytes, bbytes):
    return bytes([a & b for a, b in zip(abytes[::-1], bbytes[::-1])][::-1])
def NAND(abytes, bbytes):
    return OR(NOT(abytes), NOT(bbytes))
def NAND2(abytes, bbytes):
    return NOT(AND(abytes, bbytes))
def OR(abytes, bbytes):
    return bytes([a | b for a, b in zip(abytes[::-1], bbytes[::-1])][::-1])
def NOR(abytes, bbytes):
    return NOT(OR(abytes, bbytes))
def XOR(abytes, bbytes):
    return bytes([a ^ b for a, b in zip(abytes[::-1], bbytes[::-1])][::-1])
def NOT(abytes):
    bbytes = bytes([255 for _ in range(len(abytes))])
    return bytes([a ^ b for a, b in zip(abytes[::-1], bbytes[::-1])][::-1])
def NOT2(abytes): # just XOR w/ mask full of 1's
    return XOR(abytes, bytes([255 for _ in range(len(abytes))]))
def PRINTBYTE(abytes):
    print(abytes[0])
def GETBYTES(abytes):
    for byte in abytes:
        yield byte

a=bytes((12,123,20, 30, 31))
b=bytes((55,32, 123,16,15))
for byte in GETBYTES(NOT(a)):
    print(byte)
for byte in GETBYTES(NOT2(a)):
    print(byte)
'''

##print(sys.getsizeof(b))
##print(b)
##for i in b:
##    print(i)
##
##b2=bytes((2,))
##
##for i in AND(b, b2):
##    print(i)
##for i in OR(b, b2):
##    print(i)
##b = XOR(b, b2)
##print(sys.getsizeof(b))
##for i in b:
##    print(i)

##for i in NOT(b):
##    print(i)


