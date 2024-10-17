#Luke Davidson, Jinho Nam
#CS4700
#Project 1


import csv
import operator
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
    #callFunction(queryList[0])

    testOne = ['1','5','6','8','9', 'word']
    testTwo = ['1','2','4','8','9']

    # print(intersectFunction(testOne, testTwo))

    #Hardcoding arguments for now
    #selectFunction('PAY.csv', 'Payment', '>', '70')
    # xProdFunction('ACTORS.csv', 'MOVIES.csv')
    natJoinFunction('MOVIES.csv', 'PAY.csv')


#Results need to be stored in output file
#This will be neede towards the end
    #outputFile = open('RAoutput.csv', 'w')
    #outputFile.write(f'{userQuery}\n')
    #outputFile.write(f'{queryResult}\n\n')
    #outputFile.close()


#PARSE FUNCTION maybe rename this
def parseQuery(inputQuery):
    operatorList = [">=", ">" , "!=" , "=", "<=", "<", "*", "-"]

    for char in string.punctuation:
        if char in operatorList:
            continue
        inputQuery = inputQuery.replace(char, ' ')

    return(inputQuery)

#
def callFunction(inputQuery):
#Loop through the input query
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
            criterionValue = value
            currentValue = row[attribute]
            # Perform the operation. If the operation is true,
            # then add the current value to the "results" list
            if operation(criterionValue, currentValue):
                results.append(currentValue)
                # print(currentValue)
    
    # print (results) # Uncomment this to test this function
    return results

#PROJECT FUNCTION
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
    firstSet = []
    firstSet.extend((relationData1))

#Put second realational data into set 2
    secondSet = []
    secondSet.extend((relationData2))
    

#Sort so they are the same order
    firstSet.sort()
    secondSet.sort()

    result = []

#For every tuple in the first set, check if it is in the second set
# if the tuple is in both, add it, if not ignore it
    for tuple in firstSet:
        if tuple in secondSet:
            result.append(tuple)

    return result

#JOIN FUNCTION
def joinFunction(relationData1, relationData2, attribute1, attribute2, comparison):
    #This can simply call CROSS PRODUCT then SELECT
    xProdResult = xProdFunction(relationData1, relationData2)
    result = selectFunction(xProdResult, attribute1, comparison, attribute2)

    return result

#NATURAL JOIN FUNCTION
def natJoinFunction(relationData1, relationData2):
    #Natural JOIN is a JOIN with the attributes being those 
    #named the same in each relation and the condition is the values are equal
    with open(relationData1, newline='') as csvfile:
        reader1 = csv.DictReader(csvfile, delimiter=',')
        headers1 = reader1.fieldnames # attributes of relationalData1
        rows1 = [] # a list for rows in relationalData1
        for row in reader1:
            rows1.append(list(row.values()))
    
    with open(relationData2, newline='') as csvfile:
        reader2 = csv.DictReader(csvfile, delimiter=',')
        headers2 = reader2.fieldnames # attributes of relationalData2
        rows2 = [] # a list for rows in relationalData2
        for row in reader2:
            rows2.append(list(row.values()))

    print(headers1)
    print(headers2)
    commonAttributes = []
    for attribute in headers1:
        if attribute in headers2:
            commonAttributes.append(attribute)
    # print(commonAttributes)
    # print(rows1)

    indexList = []
    for commonAttribute in commonAttributes:
        index = headers1.index(commonAttribute)
        indexList.append(index)
    # print(indexList)

    result = []
    result.append(commonAttributes)
    for row in rows1:
        mapping = []
        for index in indexList:
            mapping.append(row[index])
        result.append(mapping)    
    print(result)
    
    return result


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
    with open(relationData2, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            #Add all tuples to the list
            tableTwoRows.append(row)
    csvfile.close()  

    combinedRows = tableOneRows.extend(tableTwoRows)

    return set(combinedRows)

#DIFFERENCE FUNCTION
def differnceFunction(relationData1, relationData2):
#Put first Realtional data into set 1
    firstSet = []
    firstSet.extend((relationData1))

#Put second realational data into set 2
    secondSet = []
    secondSet.extend((relationData2))
    

#Sort so they are the same order
    firstSet.sort()
    secondSet.sort()

    result = []

#For every tuple in the first set, check if it is in the second set
# if the tuple is in both, ignore it, if not, add it to the result set 

    for tuple in firstSet:
        if tuple not in secondSet:
            result.append(tuple)

    return result

#CROSS PRODUCT FUNCTION
def xProdFunction(relationData1, relationData2):
    with open(relationData1, newline='') as csvfile:
        reader1 = csv.DictReader(csvfile, delimiter=',')
        headers1 = reader1.fieldnames # attributes of relationalData1
        rows1 = [] # a list for rows in relationalData1
        for row in reader1:
            rows1.append(list(row.values()))
    
    with open(relationData2, newline='') as csvfile:
        reader2 = csv.DictReader(csvfile, delimiter=',')
        headers2 = reader2.fieldnames # attributes of relationalData2
        rows2 = [] # a list for rows in relationalData2
        for row in reader2:
            rows2.append(list(row.values()))

    attributes = [] # combine the headers of both relations
    attributes.extend(headers1)
    attributes.extend(headers2)
    
    combined = []
    combined.append(attributes) # add attributes
    for row1 in rows1:
        for row2 in rows2:
            # print(row1)
            # print(row2)
            # print(row1 + row2)
            combined.append(row1 + row2) # add rows from each relation

    # print(combined)
    # print(len(combined))
    return combined

if __name__=="__main__":
    main()