import sys
import math
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue
import time

class Node:
    state = None
    parent = None
    depth = None

    def __init__(self, state):
        self.state = state

#hash table holding prime numbers(int)
table = {}
solvable = False
visited = None

def isPrime(n):
    if n == 1 or n == 0:
        return False
    if n % 2 == 0 and n > 2:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def getPossibleNext(current):
    currNum = current.state
    currDepth = current.depth 

    next_list = []
    length = len(str(currNum))

    global table
    
    #manipulate every digit
    for x in range(length, 0, -1):
        offset = math.pow(10, x - 1)
        
        currDigit = int(str(currNum)[length - x])

        tmpNum = currNum - (currDigit * offset)
        
        #for each digit, ten possible variations
        for y in range(0, 10):
           next = int(tmpNum + y * offset)
           
           if (next in table):
               if table[next] <= currDepth:
                   continue
            
           #discard the number starts with 0
           if len(str(next))==length:
               #check if the number is a prime
               if isPrime(next):
                   #add the number to list
                   tmpNode = Node(next)
                   tmpNode.parent = current
                   tmpNode.depth = current.depth + 1
                   table[next] = tmpNode.depth
                   next_list.append(tmpNode)

    return next_list

def IDFS(start, target):
    currDepth = None
    depthLimit = None

    global solvable
    global table
    global visited
    visited = 0

    for x in range(0,9):
        table = {}
        depthLimit = x
        stack = list()
        stack.append(start)
        while(len(stack) != 0):
            tmpNode = stack.pop()
            visited = visited + 1
        
            currDepth = tmpNode.depth
        
            if (tmpNode.state == target):
                solvable = True
                return tmpNode

            if (currDepth == depthLimit):
                continue
        
            tmpList = getPossibleNext(tmpNode)
        
            for x in tmpList:
                if (x.state == target):
                    solvable = True
                    return x
                stack.append(x)
    sys.stdout.write("UNSOLVABLE")
        

def main():
    global table
    global solvable
    for line in sys.stdin:
        solvable = False
        table = {}
        primes = str(line).split()
        startPrime = int(primes[0])
        endPrime = int(primes[1])

        if (not isPrime(startPrime) or not isPrime(endPrime)):
            print("The two input number should be prime numbers!")
            continue

        root = Node(startPrime)
        root.depth = 0
        table[startPrime] = 1
#startTime = time.clock()
        result = IDFS(root, endPrime)
#print("--- %.5f seconds ---" % (time.clock() - startTime))
#print('visited nodes: ', visited)     
        if (solvable):
            stack = list()
            while (result != None):
                stack.append(result.state)
                result = result.parent
            while (stack):
                sys.stdout.write(str(stack.pop()) + " ")
        sys.stdout.write('\n') 


if __name__ == '__main__':
    main()
















