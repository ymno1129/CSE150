import sys
import math
import queue
import time

'''
The node class
Has a state representing the number and
a parent representing its previous number
and a depth representing current search depth
'''
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

'''
The function for checking if a number is prime
'''
def isPrime(n):
    if n % 2 == 0 and n > 2:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

'''
The function for generating all possible prime numbers resulting from
changing one digit of current number
'''
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

           if next in localTable:
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

'''
Depth limited Search
'''
def DLS(start, target):
    global visited
    global solvable
    stack = list()
    stack.append(start)

    currDepth = None

    while(len(stack) != 0):
        
        tmpNode = stack.pop()
        visited = visited + 1
        
        currDepth = tmpNode.depth
        
        if (tmpNode.state == target):
            solvable = True
            return tmpNode

        if (currDepth == 5):
            continue
        
        tmpList = getPossibleNext(tmpNode)
        
        for x in tmpList:
            if (x.state == target):
                solvable = True
                return x
            x.depth = (currDepth) + 1
            stack.append(x)
            
    print("UNSOLVABLE")
        

def main():
    primes = str(sys.stdin.readline()).split()
    startPrime = int(primes[0])
    endPrime = int(primes[1])
    
    root = Node(startPrime)
    root.depth = 0
    table[startPrime] = 1

    s = set()
    s.add(1)
    s.add(1)
    print(len(s))
    
    # calculate time
    startTime = time.clock()
    result = DLS(root, endPrime)
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
















