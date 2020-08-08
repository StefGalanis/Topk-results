#GALANIS STEFANOS 2032
import sys
import heapq
import time
from collections import OrderedDict

def threshold(current_male_weight,current_female_weight):
    avg1 = current_female_weight + max_male_weight
    avg2 = current_male_weight + max_female_weight
    T = -max(avg1,avg2)
    return T

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

topk = int(sys.argv[1])
males_file = open('males_sorted')
females_file = open('females_sorted')
outputFile = open('outputTopk','w')
flag = 0
max_female_weight = 0
max_male_weight = 0
current_female_weight = 0
current_male_weight = 0
males_dictionary = OrderedDict()
females_dictionary = OrderedDict()
heap = [] 
heapq.heapify(heap)
eof = 0

number_of_results = 0

validLines = 0


switch = False

startTime = time.time()

while topk != 0:

    if switch == False :
        for line in males_file:
            if isMarried(line) == False and isAdult(line) == True:

                validLines += 1

                line_values = line.split(',')

                maleID = int(line_values[0])
                weight = float(line_values[25])
                current_male_weight = weight
                age = int(line_values[1])

                if age not in males_dictionary:
                    males_dictionary[age] = (maleID,weight)

                if flag == 0:
                    max_male_weight = weight

                T = threshold(current_male_weight,current_female_weight)

                for female_age in females_dictionary:
                    female_values = females_dictionary[female_age]
                    femaleID = female_values[0]
                    female_weight = female_values[1]
                    if isSameAge(age,female_age):
                        total_weight = female_weight+weight
                        heapq.heappush(heap,(-total_weight,femaleID,maleID))
                break
            else:
                continue
    if switch == True :
        if eof == 0:
            for line in females_file:

                if isMarried(line) == False and isAdult(line) == True:

                    validLines += 1

                    line_values = line.split(',')

                    femaleID = int(line_values[0])
                    weight = float(line_values[25])
                    current_female_weight = weight
                    age = int(line_values[1])

                    if age not in females_dictionary:
                        females_dictionary[age] = (femaleID,weight)

                    if flag == 0:
                        max_female_weight = weight
                        flag = 1
                    T = threshold(current_male_weight,current_female_weight)

                    for male_age in males_dictionary:
                        male_values = males_dictionary[male_age]
                        maleID = male_values[0]
                        male_weight = male_values[1]
                        if isSameAge(age,male_age):
                            total_weight = male_weight+weight
                            heapq.heappush(heap,(-total_weight,femaleID,maleID))

                    break
                else:
                    continue
            else:
                eof = 1
            
    if len(heap) > 0 :
        if (heap[0][0] <= T):
            weight_to_print = -heap[0][0]
            outputFile.write(str(weight_to_print)+','+str(heap[0][1])+','+str(heap[0][2])+'\n')
            heapq.heappop(heap)
            number_of_results += 1
            topk -= 1
        #elif eof == 1:
            #print(heap[0])
        #    outputFile.write(str(heap[0])+'\n')
        #    heapq.heappop(heap)
        #    number_of_results += 1
        #    topk -= 1
    switch = not switch
    #print('male Dictionary contains: {} \nfemale Dictionary contains: {}\n'.format(males_dictionary,females_dictionary))
endTime = time.time()

print('"time to return top {} results is": {} sec \n"valid lines read": {}'.format(number_of_results,endTime-startTime,validLines))

executionTime = open('executionTime','w')

executionTime