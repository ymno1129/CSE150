import sys
import math
import queue

class Node:
    state = None
    parent = None

    def __init__(self, state):
        self.state = state

#hash table holding prime numbers(int)
table_start = {}
table_target = {}
solvable = False

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
            
           #discard the number starts with 0
           if len(str(int(next)))==length:
               #check if the number is a prime
               if isPrime(int(next)):
                   #add the number to list
                   next_list.append(int(next))

    return next_list

def BDS(start, target):
    q_start = queue.Queue(0)
    q_start.put(start)

    q_target = queue.Queue(0)
    q_target.put(target)

    global solvable

    startNext = None
    targetNext = None
    while ((not q_start.empty()) and (not q_target.empty())):
        tmpStart = q_start.get()
        tmpTarget = q_target.get()

        startNext = getPossibleNext(tmpStart)
##        for x in startNext:
##            tmpNode = Node(x)
##            tmpNode.parent = tmpStart
##            tmpNode_target = Node(tmpStart.state)
##            if x == target.state:
##                solvable = True
##                tmpNode_target.parent = target
##                print('a')
##                return [tmpNode, tmpNode_target]
##            for y in list(q_target.queue):
##                if x == y.state:
##                    solvable = True
##                    tmpNode_target.parent = y
##                    print('d')
##                    return [tmpNode, tmpNode_target]
##                if x == tmpTarget.state:
##                    solvable = True
##                    tmpNode_target.parent = tmpTarget
##                    print('e')
##                    return [tmpNode, tmpNode_target]
        targetNext = getPossibleNext(tmpTarget)

        frontier = list()
        for x in q_start.queue:
            tmpList = getPossibleNext(x)
            for y in tmpList:
                frontier.append(y)

        for x in frontier:
            tmpNode = Node(x)
            tmpNode.parent = tmpStart
        
        for x in startNext:
            tmpNode = Node(x)
            tmpNode.parent = tmpStart   
            if x in targetNext:
                solvable = True
                tmpNode_target = Node(x)
                tmpNode_target.parent = tmpTarget
                print('b')
                return [tmpNode, tmpNode_target]      
            if x not in table_start:
                table_start[x] = 1
                q_start.put(tmpNode)            
        for x in targetNext:      
            tmpNode = Node(x)
            tmpNode.parent = tmpTarget     
            if x not in table_target:
                table_target[x] = 1
                q_target.put(tmpNode)

            
    print("UNSOLVABLE")
   

def main():
    primes = str(sys.stdin.readline()).split()
    startPrime = int(primes[0])
    endPrime = int(primes[1])
    
    root = Node(startPrime)
    table_start[startPrime] = 1
    
    target = Node(endPrime)
    table_target[endPrime] = 1

    result = BDS(root, target)

    if (solvable):
        resultFromStart = result[0]
        resultFromTaget = result[1]
        stack = list()
        while (resultFromStart != None):
            stack.append(resultFromStart.state)
            resultFromStart = resultFromStart.parent 
        while (stack):
            print(stack.pop(), end=" ")
        print()
        stack = list()
        while (resultFromTaget != None):
            stack.append(resultFromTaget.state)
            resultFromTaget = resultFromTaget.parent 
        while (stack):
            print(stack.pop(), end=" ")

if __name__ == '__main__':
    main()
















