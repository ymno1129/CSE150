import sys
import math
import queue
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
visited = 0

def isPrime(n):
    if n % 2 == 0 and n > 2:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def getPossibleNext(current):
    currNum = current.state
    next_list = []
    length = len(str(currNum))
    localTable = {}
    
    #manipulate every digit
    for x in range(length, 0, -1):
        offset = math.pow(10, x - 1)
        
        currDigit = int(str(currNum)[length - x])

        # subtract offset * currDigit from currNum
        # for example, if currNum is 23, then when
        # manipulating the first digit, subtract it
        # by 20 and start with 3.
        # when manipulating the second digit, subtract
        # int by 3 and start with 20.
        tmpNum = currNum - (currDigit * offset)
        
        #for each digit, ten possible variations
        for y in range(0, 10):
           next = tmpNum + y * offset
           
           if (next in localTable):
               continue

           localTable[next] = 1
            
           #discard the number starts with 0
           if len(str(int(next)))==length:
               #check if the number is a prime
               if isPrime(int(next)):
                   #add the number to list
                   tmpNode = Node(int(next))
                   tmpNode.parent = current
                   next_list.append(tmpNode)

    return next_list

def IDFS(start, target):

    currDepth = None
    depthLimit = None

    global visited
    global solvable

    for x in range(0,9):
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
                x.depth = (currDepth) + 1
        global table
        table = {}
            
    print("UNSOLVABLE")
        

def main():
    primes = str(sys.stdin.readline()).split()
    startPrime = int(primes[0])
    endPrime = int(primes[1])
    
    root = Node(startPrime)
    root.depth = 0
    table[startPrime] = 1

    startTime = time.clock()
    result = IDFS(root, endPrime)
    print("--- %.5f seconds ---" % (time.clock() - startTime))
    print('Nodes visited: ', visited)
    
    if (solvable):
        stack = list()
        while (result != None):
            stack.append(result.state)
            result = result.parent 
        print('Path length:' ,len(stack))
        while (stack):
            print(stack.pop(), end=" ")



if __name__ == '__main__':
    main()
















