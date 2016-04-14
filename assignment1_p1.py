import sys
import math
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue
#import queue
import time

'''
The node class
Has a state representing the number and
a parent representing its previous number
'''
class Node:
    state = None
    parent = None

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
           
           if (next in table):
               continue

           table[next] = 1
            
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
Breadth first search
'''
def BFS(start, target):
    global solvable
    q = queue.Queue(0)
    q.put(start)

    if start.state == target:
        solvable = True
        return start

    while not q.empty():
        tmpNode = q.get()
        
        tmpList = getPossibleNext(tmpNode)      
       
        for x in tmpList:
            if (x.state == target):
                solvable = True
                return x
            q.put(x)

    print("UNSOLVABLE")
    return

def main():
    
#inputName = sys.argv[1]
#f = open(inputName, "r")
    global table
    for line in sys.stdin:
        table = {}
        primes = str(line).split()
        startPrime = int(primes[0])
        endPrime = int(primes[1])

        if (not isPrime(startPrime) or not isPrime(endPrime)):
            print("The two input number should be prime numbers!")
            continue

        root = Node(startPrime)
        table[startPrime] = 1

        result = BFS(root, endPrime)
            
        if (solvable):
            stack = list()
            while (result != None):
                stack.append(result.state)
                result = result.parent
            while (stack):
#curr = str(stack.pop()) + " "
#print curr
                sys.stdout.write(str(stack.pop()) + " ")
        sys.stdout.write('\n')

if __name__ == '__main__':
    main()
















