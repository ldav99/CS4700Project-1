#Luke Davidson, Jinho Nam
#CS4700
#Project 1


import csv
import operator
import re
import string


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
    #print(unionFunction('',''))

#Call parse function on all of the queries
    for i in range(0,len(queryList)):
        queryList[i] = queryList[i].strip('\n')
        queryList[i] = parseQuery(queryList[i])

    #print(queryList)
    callFunction(queryList[0])

    #Hardcoding arguments for now
    #selectFunction('PAY.csv', 'Payment', '>', '70')


#Results need to be stored in output file
#This will be neede towards the end
    #outputFile = open('RAoutput.csv', 'w')
    #outputFile.write(f'{userQuery}\n')
    #outputFile.write(f'{queryResult}\n\n')
    #outputFile.close()


#PARSE FUNCTION maybe rename this
def parseQuery(inputQuery):
    characterList = [">=", ">" , "!=" , "=", "<=", "<", "*", "-"]

    for char in string.punctuation:
        if char in characterList:
            continue
        inputQuery = inputQuery.replace(char, ' ')

    return(inputQuery)

#
def callFunction(inputQuery):
    # keywords = {
    #     "SELE ": selectFunction(),
    #     "PROJ ": projectFunction(),
    #     "U": unionFunction(),
    #     " * ": natJoinFunction(),
    #     " - ": differnceFunction(),
    #     " x ": xProdFunction(),
    #     " INTE ": intersectFunction(),
    #     " JOIN ": joinFunction()
    # }

#Loop through the input query
#TODO Ask about multiple statements in a query
    splitQuery = inputQuery.split()
    splitList = []

    for word in splitQuery:
        splitList.append(word)

    if 'SELE' in splitList:
        wordIndex = splitList.index('SELE')
        attribute = splitList[wordIndex + 1]
        comparison = splitList[wordIndex + 2]
        value = splitList[wordIndex + 3]
        addCSV = splitList[wordIndex + 4] + '.csv'

        print(selectFunction(addCSV, attribute, comparison, value))

    #print(splitList)

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
#ANSWER^: 
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