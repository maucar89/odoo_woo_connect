
DMatrix = [[0,1,2,3,4,5,6,7,8,9],
           [1,2,3,4,0,6,7,8,9,5],
           [2,3,4,0,1,7,8,9,5,6],
           [3,4,0,1,2,8,9,5,6,7],
           [4,0,1,2,3,9,5,6,7,8],
           [5,9,8,7,6,0,4,3,2,1],
           [6,5,9,8,7,1,0,4,3,2],
           [7,6,5,9,8,2,1,0,4,3],
           [8,7,6,5,9,3,2,1,0,4],
           [9,8,7,6,5,4,3,2,1,0]]

PMatrix = [[0,1,2,3,4,5,6,7,8,9],
           [1,5,7,6,2,8,3,0,9,4],
           [5,8,0,3,7,9,6,1,4,2],
           [8,9,1,6,0,4,3,5,2,7],
           [9,4,5,3,1,2,6,8,7,0],
           [4,2,8,6,5,7,3,9,0,1],
           [2,7,9,3,8,0,6,4,1,5],
           [7,0,4,6,9,1,3,2,5,8]]

InvMatrix = [0,4,3,2,1,5,6,7,8,9]

def d(j, k):
    return DMatrix[j][k]

def p(pos, num):
    return PMatrix[pos % 8][num]

def inv(j):
    return InvMatrix[j]

def calcsum(number):
    i = c = 0
    for n in reversed(str(number)):
        c = d(c, p(i+1, int(n)))
        i += 1
    return inv(c)

def checksum(number):
    i = c = 0
    for n in reversed(str(number)):
        c = d(c, p(i, int(n)))
        i += 1
    return c

def verify(number):
    return checksum(number) == 0

def encode(number, times=1):
    n = str(number)
    digits = []
    for i in range(times):
        # get verhoeff number
        d = str(calcsum(n))
        # add to stack
        digits.append(d)
        # append to number
        n += d

    return ''.join(digits)



