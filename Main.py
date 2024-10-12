#Luke Davidson, Jinho Nam
#CS4700
#Project 1


#TODO add PROJECT, SELECT, INTERSECT, JOIN, *, UNION, Difference,CROSS PRODUCT

import csv

#This was just for testing how csv worked
#All of this is not needed
# with open('ACTORS.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))


def main():
    queryList = []
    queryFile = open('RAQueries.txt', 'r')
    lines = len(queryFile.readlines())
    queryFile.close()

#Re-Open file to read contents
    queryFile = open('RAQueries.txt', 'r')

    for i in range(1,4+1):
        query  = str(queryFile.readline())
        queryList.append(query)
    
    print(queryList)

    queryFile.close()

    #Hardcoding arguments for now
    #selectFunction('PAY.csv', 'Payment', '>', '70')


#Results need to be stored in output file
#This will be neede towards the end
    outputFile = open('RAoutput.csv', 'w')
    #outputFile.write(f'{userQuery}\n')
    #outputFile.write(f'{queryResult}\n\n')

    outputFile.close()


#SELECT FUNCTION
def selectFunction(relationData, attribute, comparison, value):
#Open the specifed file
    with open(relationData, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            print(row['Payment'])


#PROJECT FUNCTION
def projectFunction(relationData, atttribute):
    return 0

#INTERSECT FUNCTION
def intersectFunction(relationData1, relationData2):
    return 0

#JOIN FUNCTION
def joinFunction(relationData1, relationData2, attribute1, attribute2, comparison):
    #This can simply call CROSS PRODUCT then SELECT
    
    return 0

#NATURAL JOIN FUNCTION
def natJoinFunction(relationData1, relationData2):
    #Natural JOIN is a JOIN with the attributes being those 
    #named the same in each relation and the condition is the values are equal
    return 0


#UNION FUNCTION
def unionFunction(relationData1, relationData2):
    return 0

#DIFFERENCE FUNCTION
def differnceFunction(relationData1, relationData2):
    return 0

#CROSS PRODUCT FUNCTION
def xProdFunction(relationData1, relationData2):
    return 0




main()