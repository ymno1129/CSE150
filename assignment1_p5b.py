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

    #g(n) representing cost from goal to this node
    distFromGoal = None

    #h(n) representing cost from this node to goal
    distToGoal = None

    nextPossible = None

    def __init__(self, state):
        self.state = state

    def __lt__(self, other):
        if ((self.distFromGoal + self.distToGoal) == 
        (other.distFromGoal + other.distToGoal)):
            return (self.nextPossible > other.nextPossible)
        else:
            return ((self.distFromGoal + self.distToGoal) <
                (other.distFromGoal + other.distToGoal))


#hash table holding prime numbers(int)
table = {}
solvable = False
visited = 0

def hammingDistance(a, b):
    if len(str(a)) != len(str(b)):
        print("The two numbers should have same number of digits.")
        return
    dist = 0
    for x in range(0, len(str(a))):
        if str(a)[x] != str(b)[x]:
            dist = dist + 1
    return dist

def isPrime(n):
    if n == 1 or n == 0:
        return False
    if n % 2 == 0 and n > 2:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def peekPossibleNext(current):
    result = 0
    length = len(str(current))
    for x in range(length, 0, -1):
        offset = math.pow(10, x - 1)
        currDigit = int(str(current)[length - x])
        tmpNum = current - (currDigit * offset)
        for y in range(0, 10):
           next = tmpNum + y * offset
           if (next in table):
               continue
           if len(str(int(next)))==length:
               if isPrime(int(next)):
                   result = result + 1
    return result

def getPossibleNext(current):
    currNum = current.state
    next_list = []
    length = len(str(currNum))
    
    #manipulate every digit
    for x in range(length, 0, -1):
        offset = math.pow(10, x - 1)
        
        currDigit = int(str(currNum)[length - x])

        tmpNum = currNum - (currDigit * offset)
        
        #for each digit, ten possible variations
        for y in range(0, 10):
           next = int(tmpNum + y * offset)
           
           if (next in table):
               continue

           table[next] = 1
            
           #discard the number starts with 0
           if len(str(next))==length:
               #check if the number is a prime
               if isPrime(next):
                   #add the number to list
                   tmpNode = Node(next)
                   tmpNode.parent = current
                   tmpNode.distFromGoal = current.distFromGoal + 1
                   next_list.append(tmpNode)

    return next_list

def Astar(start, target):
    global solvable
    global visited
    pq = queue.PriorityQueue()
    pq.put(start)

    if start.state == target:
	    solvable = True
	    return start

    while not pq.empty():
        tmpNode = pq.get()
        visited = visited + 1
        
        tmpList = getPossibleNext(tmpNode)      
       
        for x in tmpList:
            if (x.state == target):
                solvable = True
                return x
            tmpHammDist = hammingDistance(x.state, target)
            x.nextPossible = peekPossibleNext(x.state)
            x.distToGoal = tmpHammDist
            pq.put(x)

    sys.stdout.write("UNSOLVABLE")
    return

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
        if len(str(startPrime)) != len(str(endPrime)):
            print("UNSOLVABLE")
            continue

        root = Node(startPrime)
        root.distFromGoal = 0

        table[startPrime] = 1
#startTime = time.clock()
        result = Astar(root, endPrime)
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

