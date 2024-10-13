#Luke Davidson, Jinho Nam
#CS4700
#Project 1


#TODO add PROJECT, SELECT, INTERSECT, JOIN, *, UNION, Difference,CROSS PRODUCT

import csv
import operator
import re

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
    queryFile.close()

    #print(projectFunction('PAY.csv', 'MNO'))
    print(unionFunction('',''))

#Call parse function on all of the queries
    # for i in range(0,len(queryList)):
    #     parseQuery(queryList[i])
    #parseQuery(queryList[0])

    #Hardcoding arguments for now
    #selectFunction('PAY.csv', 'Payment', '>', '70')


#Results need to be stored in output file
#This will be neede towards the end
    #outputFile = open('RAoutput.csv', 'w')
    #outputFile.write(f'{userQuery}\n')
    #outputFile.write(f'{queryResult}\n\n')
    #outputFile.close()


#PARSE FUNCTION
def parseQuery(inputQuery):
    if re.search('W*(SELE_)W*', inputQuery):
        relation = (re.search(r'\(([a-z]*?)\)',inputQuery, re.IGNORECASE).group(1)) + '.csv'
        print(relation)
        selectFunction(relation, 'Payment', '>', '70')

#SELECT FUNCTION
    # The query: SELE_{Payment > 70} (PAY)
    # relationData: PAY
    # attribute: payment
    # comparision: >
    # value: 70
def selectFunction(relationData, attribute, comparison, value):
    # A list to return for this function
    results = []

    # A dictionary to handle a value assigned to comparison
    operators = {
        "<": operator.lt, 
        "<=": operator.le,
        "=": operator.eq,
        "!=": operator.ne,
        ">": operator.le,
        ">=": operator.ge
    }

    # Check if "comparision" is a operator in the dictionary
    # Otherwise, throw an error
    try:
        operation = operators.get(comparison)
    except:
        raise ValueError(f"selectFunction()::invalid operator -> {comparison}")

    # Open the specifed file
    with open(relationData, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        # Read the file row by row
        for row in reader:
            criterionValue = value;
            currentValue = row[attribute]
            # Perform the operation. If the operation is true,
            # then add the current value to the "results" list
            if operation(criterionValue, currentValue):
                results.append(currentValue)
                # print(currentValue)
    
    # print (results) # Uncomment this to test this function
    return results

#PROJECT FUNCTION
#TODO Ask if this needs to work with multiple attributes or just one like in examples
def projectFunction(relationData, atttribute):
#This list will have all tuples called from column
    allTuples = []

    # Open the specifed file
    with open(relationData, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            #Add all tuples to the list
            allTuples.append(row[atttribute])

#By using the set() function it gets rid of all duplicates in the list
    return set(allTuples)



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
    tableOneRows = []
    tableTwoRows = []
    combinedRows = []

    # Open the first specifed file
    with open(relationData1, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            #Add all tuples to the list
            tableOneRows.append(row)
    csvfile.close()    

    # Open the second specifed file
    with open(relationData1, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            #Add all tuples to the list
            tableTwoRows.append(row)
    csvfile.close()  

    combinedRows = tableOneRows.extend(tableTwoRows)

    return set(combinedRows)

#DIFFERENCE FUNCTION
def differnceFunction(relationData1, relationData2):
    return 0

#CROSS PRODUCT FUNCTION
def xProdFunction(relationData1, relationData2):
    return 0




main()