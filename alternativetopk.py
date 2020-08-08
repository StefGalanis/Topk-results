#GALANIS STEFANOS 2032
import heapq
import sys
import time
from collections import OrderedDict


def isSameAge(age1,age2):
    if age1 == age2 :
        return True

def isAdult(line):
    line_values = line.split(',')
    age = int(line_values[1])
    if age >= 18:
        return True
    else:
        return False

def isMarried(line):
    line_values = line.split(',')
    status = line_values[8]
    if 'Married' in status and 'Never' not in status:
        return True
    else:
        return False

def getID(line):
    line_values = line.split(',')
    return line_values[0]

males_file = open('males_sorted')
females_file = open('females_sorted')
outputFile = open('outputTopkAlternative','w')
males_dictionary = OrderedDict()
heap = []
heapq.heapify(heap)
topk = int(sys.argv[1])

valid_lines = 0

startTime = time.time()

for line in males_file:
    if isMarried(line) == False and isAdult(line) == True:

        valid_lines += 1

        line_values = line.split(',')

        maleID = int(line_values[0])
        weight = float(line_values[25])
        current_male_weight = weight
        age = int(line_values[1])

        if age not in males_dictionary:
            males_dictionary[age] = (maleID,weight)

for line in females_file:
    if isMarried(line) == False and isAdult(line) == True:

        valid_lines += 1
        
        line_values = line.split(',')

        femaleID = int(line_values[0])
        weight = float(line_values[25])
        current_female_weight = weight
        age = int(line_values[1])

        for male_age in males_dictionary: 
            male_values = males_dictionary[male_age]
            maleID = male_values[0]
            male_weight = male_values[1]
            if isSameAge(age,male_age):
                total_weight = male_weight+weight
                heapq.heappush(heap,(-total_weight,femaleID,maleID))

for i in range (0,topk):
    weight_to_print = -heap[0][0]

    outputFile.write(str(weight_to_print)+','+str(heap[0][1])+','+str(heap[0][2])+'\n')
    heapq.heappop(heap)

endTime = time.time()

print('"time to return top {} results is" : {}\n"valid lines read": {}'.format(topk,endTime-startTime,valid_lines))

