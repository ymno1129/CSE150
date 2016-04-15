import sys
import math
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue
#import queue
import time

class Node:
    state = None
    parent = None

    #g(n) representing cost from goal to this node
    distFromGoal = None

    #h(n) representing cost from this node to goal
    distToGoal = None

    def __init__(self, state):
        self.state = state

    def __lt__(self, other):
         return ((self.distFromGoal + self.distToGoal) <
                (other.distFromGoal + other.distToGoal))

#hash table holding prime numbers(int)
table_start = {}
table_target = {}
solvable = False

def hammingDistance(a, b):
    if len(str(a)) != len(str(b)):
        return 999
    dist = 0
    for x in range(0, len(str(a))):
        if str(a)[x] != str(b)[x]:
            dist = dist + 1
    return dist


def isPrime(n):
    if n == 1:
        return False
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
    
    for x in range(length, 0, -1):
        offset = math.pow(10, x - 1)
        
        currDigit = int(str(currNum)[length - x])

        tmpNum = currNum - (currDigit * offset)
        
        for y in range(0, 10):
           next = tmpNum + y * offset
            
           if len(str(int(next)))==length:
               if isPrime(int(next)):
                   next_list.append(int(next))

    return next_list

def BDS(start, target):
    global solvable
    if (start.state == target.state):
        result = start.state
        sys.stdout.write(str(result))
        return 

    q_start = queue.PriorityQueue()
    q_start.put(start)

    q_target = queue.Queue(0)
    q_target.put(target)

    startNext = None
    targetNext = None
    
    while ((not q_start.empty()) and (not q_target.empty())):
        tmpStart = q_start.get()
        tmpTarget = q_target.get()

        startNext = getPossibleNext(tmpStart)
        targetNext = getPossibleNext(tmpTarget)
        
        for x in startNext:
            tmpNode = Node(x)
            tmpNode.parent = tmpStart
            tmpNode.distFromGoal = tmpStart.distFromGoal + 1
            if x in table_target:
                solvable = True
                tmpNode_target = Node(tmpStart.state)
                tmpNode_target.parent = table_target[x]
                return [tmpNode, tmpNode_target]      
            if x not in table_start:
                tmpNode.distToGoal = hammingDistance(tmpNode.state, target.state)
                table_start[x] = tmpNode
                q_start.put(tmpNode)

        for x in targetNext:      
            tmpNode = Node(x)
            tmpNode.parent = tmpTarget     
            if x in table_start:
                solvable = True
                tmpNode_target = Node(x)
                tmpNode_target.parent = tmpTarget
                return [table_start[x], tmpNode_target]
            if x not in table_target:
                table_target[x] = tmpNode
                q_target.put(tmpNode)

            
    sys.stdout.write("UNSOLVABLE")
   

def main():
    global table_start
    global table_target
    for line in sys.stdin:
        table_start = {}
        table_target = {}

        primes = str(line).split()
        startPrime = int(primes[0])
        endPrime = int(primes[1])
        
        if (not isPrime(startPrime) or not isPrime(endPrime)):
            print("The two input number should be prime numbers!")
            continue
    
        root = Node(startPrime)
        root.distFromGoal = 0
        table_start[startPrime] = root
    
        target = Node(endPrime)
        table_target[endPrime] = target

#startTime = time.clock()
        result = BDS(root, target)
#print("--- %.5f seconds ---" % (time.clock() - startTime))
    
        if (solvable):
            resultFromStart = result[0]
            resultFromTarget = result[1]
            stack = list()
            while (resultFromStart != None):
                stack.append(resultFromStart.state)
                resultFromStart = resultFromStart.parent 
            while (stack):
                sys.stdout.write(str(stack.pop()) + " ")
            sys.stdout.write('\n')
            stack = list()
            while (resultFromTarget != None):
                stack.append(resultFromTarget.state)
                resultFromTarget = resultFromTarget.parent 
            while (stack):
                sys.stdout.write(str(stack.pop()) + " ")
        sys.stdout.write('\n') 

if __name__ == '__main__':
    main()
















