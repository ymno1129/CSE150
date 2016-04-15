import sys
import math
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue
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
visited = None

'''
The function for checking if a number is prime
'''
def isPrime(n):
    if n == 1 or n == 0:
        return False
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
    currDepth = current.depth

    next_list = []
    length = len(str(currNum))
     
    #manipulate every digit
    for x in range(length, 0, -1):
        offset = math.pow(10, x - 1)
        
        currDigit = int(str(currNum)[length - x])
        
        tmpNum = currNum - (currDigit * offset)
        
        for y in range(0, 10):
           next = int(tmpNum + y * offset)

           if next in table:
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
                   next_list.append(tmpNode)

    return next_list
    

'''
Depth limited Search
'''
def DLS(start, target):
    global visited
    global solvable
    global table
    stack = list()
    stack.append(start)

    currDepth = None

    visited = 0
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
        result = DLS(root, endPrime)
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
















