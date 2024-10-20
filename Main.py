#Luke Davidson, Jinho Nam
#CS4700
#Project 1


import copy
import csv
import operator
import string


def main():
    queryList = []
    queryFile = open('RAQueries.txt', 'r')
    lines = len(queryFile.readlines())
    queryFile.close()

    # Re-Open file to read contents
    queryFile = open('RAQueries.txt', 'r')

    for i in range(1,4+1):
        query  = str(queryFile.readline())
        queryList.append(query)
    queryFile.close()

    #print(projectFunction('PAY.csv', 'MNO'))
    #print(unionFunction('',''))

    # Call parse function on all of the queries
    # for i in range(0,len(queryList)):
    #     queryList[i] = queryList[i].strip('\n')
    #     queryList[i] = parseQuery(queryList[i])

    #print(queryList)
    #callFunction(queryList[0])

    # testOne = ['1','5','6','8','9', 'word']
    # testTwo = ['1','2','4','8','9']

    # print(intersectFunction(testOne, testTwo))

    #Hardcoding arguments for now

    # Open the specifed file
    global PAY 
    global MOVIES
    global ACTORS
    PAY = './PAY.csv'
    MOVIES = './MOVIES.csv'
    ACTORS = './ACTORS.csv'

    PAY = reformat_to_2Darray(PAY)
    MOVIES = reformat_to_2Darray(MOVIES)
    ACTORS = reformat_to_2Darray(ACTORS)


    query = parseQuery("(PROJ_{ANO} (SELE_{Payment > 90} (PAY))) U (PROJ_{ANO} (SELE_{ANAME ='Rivers'} (ACTORS)))")
    print(f'{query}:')
    print(callFunction(query))

    queryTwo = parseQuery("SELE_{Payment > 70} (PAY)")
    print(f'{queryTwo}:')
    print(callFunction(queryTwo))

    # print(selectFunction(PAY, ['Payment'], '>', 70))
    #print(projectFunction(intersectFunction(ACTORS, PAY), "ANO"))
              
    # selectFunction(PAY, ['Payment'], '>', '70')
    #projectFunction(PAY, 'ANO')
    # intersectFunction(PAY, MOVIES)
    # differnceFunction(PAY, MOVIES)
    # xProdFunction(PAY, MOVIES)
    # unionFunction(PAY, MOVIES)
    # natJoinFunction(MOVIES, PAY) 
    # joinFunction(MOVIES, PAY, "MNO", "MNO", "=")
    # joinFunction(Student, Subjects, "Std", "Class", "=")


#Results need to be stored in output file
    # outputFile = open('RAoutput.csv', 'w')
    # for i in range(0,len(queryList)):
    #     outputFile.write(f'{queryList[i]}\n')
    #     outputFile.write(f'{callFunction(queryList[i])}\n\n')
    
    #outputFile.close()

def reformat_to_2Darray(csvfile):
    data = list(csv.reader(open(csvfile)))
    
    return data

#PARSE FUNCTION Takes the inputed query and removes any symbols that arent in the opperator list
def parseQuery(inputQuery):
    operatorList = [">=", ">" , "!=" , "=", "<=", "<", "*", "-"]

    for char in string.punctuation:
        if char in operatorList:
            continue
        inputQuery = inputQuery.replace(char, ' ')

    return(inputQuery)

#This is the main function that depending on what is in the query calls the other functions
def callFunction(inputQuery):
    relations = {
        "PAY": PAY,
        "ACTORS": ACTORS,
        "MOVIES": MOVIES
    }

#Loop through the input query
    splitQuery = inputQuery.split()
    splitList = []

    firstHalf = []
    secondHalf = []

    selectResults = []
    secondHalfResult = []

    for word in splitQuery:
        splitList.append(word)


#If there is a union split the list before and after the U
    if 'U' in splitList:
        wordIndex = splitList.index('U')

        firstHalf = splitList[:wordIndex]
        secondHalf = splitList[wordIndex+1:]

        firstHalfResult = []

#Get the relations that the two queries use
        firstrelation = len(firstHalf)
        thefirstRelation = firstHalf[firstrelation-1]
        secondrelation = len(secondHalf)
        thesecondRelation = secondHalf[secondrelation-1]
    else:
        firstHalf.extend(splitList)
        firstrelation = len(firstHalf)
        thefirstRelation = firstHalf[firstrelation-1]


    if 'SELE' in firstHalf:
        wordIndex = splitList.index('SELE')
        attributes = []
        attributes.append(splitList[wordIndex + 1])
        comparison = splitList[wordIndex + 2]
        value = splitList[wordIndex + 3]
        addCSV = relations.get(thefirstRelation) 

        #print(addCSV, attribute, comparison, value)
        selectResults = selectFunction(addCSV, attributes, comparison, value)

        if 'PROJ' in firstHalf:
            wordIndex = splitList.index('PROJ')
            projAttribute = splitList[wordIndex + 1]
            firstHalfResult =  projectFunction(selectResults, projAttribute)
            print(firstHalfResult)
        else:
            return selectResults
    
    if len(secondHalf) != 0:
        if 'SELE' in secondHalf:
            wordIndex = secondHalf.index('SELE')
            attributes = secondHalf[wordIndex + 1]
            comparison = secondHalf[wordIndex + 2]
            value = secondHalf[wordIndex + 3]
            addCSV = relations.get(thesecondRelation) 

            #print(addCSV, attributes, comparison, value)
            selectResults = selectFunction(addCSV, attributes, comparison, value)
            #print(selectResults)

            if 'PROJ' in secondHalf:
                wordIndex = splitList.index('PROJ')
                projAttribute = splitList[wordIndex + 1]
                #print(selectResults)
                secondHalfResult =  projectFunction(selectResults, projAttribute)

    #return unionFunction(firstHalfResult, secondHalfResult)

# SELECT FUNCTION
# "relationData" parameter should be a 2-D array
# "attributes" parameter should be a 1-D array (e.g. ['Payment'])
# returns 2-D array
def selectFunction(relationData, attributes, comparison, value):
    # A 2-D array to return for this function
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

    # Get the index of the target attribute(column)
    index_list = []
    target_attributes = []
    for column in relationData[0]: # attribute row = relationaData[0]
        for attribute in attributes:
            if column == attribute:
                target_attributes.append(column)
                index = relationData[0].index(column)
                index_list.append(index)
    results.append(relationData[0])

    # Read the 2-D array(relationData) row by row
    # mapping = [] # temporal row
    for row in relationData[1:]:
        for column_index in index_list:
            criterionValue = value
            currentValue = row[column_index]
            # Perform the operation. If the operation is true,
            # then add the current value to the "results" list
            if operation(int(criterionValue), int(currentValue)):
                # mapping.append(currentValue) 
                results.append(row)
            # else:
            #     mapping.append("")
            #     results.append(mapping)
        # results.extend(mapping)
        # mapping = [] # Clear to contain new data
    
    # print(results) # Uncomment this to test this function
    return results


# PROJECT FUNCTION
# "relationData" parameter should be a 2-D array
# "attributes" parameter should be a string
# returns 2-D array
def projectFunction(relationData, attribute):
    # A 2-D array to return
    results = []

    # Get the index of the target attribute(column)
    index_list = []
    result_attributes = []
    for column in relationData[0]: # attribute row = relationaData[0]
        if column == attribute:
            result_attributes.append(column)
            index = relationData[0].index(column)
            index_list.append(index)
    results.append(result_attributes)
    #print(results)

    # Read the 2-D array(relationData) row by row
    mapping = [] # temporal row
    for row in relationData[1:]:
        for column_index in index_list:
            currentValue = row[column_index]
            mapping.append(currentValue)
        results.append(mapping)
        mapping = [] # Clear to contain new data
    
    # print(results) # Uncomment this to test this function
    return results


# INTERSECT FUNCTION
# "relationData1" parameter should be a 2-D array
# "relationData2" parameter should be a 2-D array
# Return 2-D array
def intersectFunction(relationData1, relationData2):
    # An 2-D array to return
    results = []

    # Extract common attribute
    common_attributes = []
    for relation1_attribute in relationData1[0]:
        for relation2_attribute in relationData2[0]:
            if relation1_attribute == relation2_attribute:
                common_attributes.append(relation1_attribute)
    results.append(common_attributes)
    
    # Get the index of the common attributes(columns) from relationData1
    index_list = []    
    for column in relationData1[0]:
        for attribute in common_attributes:
            if column == attribute:
                index = relationData1[0].index(column)
                index_list.append(index)
        
    # Read the 2-D array(relationData1) row by row
    mapping = [] # temporal row
    for row in relationData1[1:]:
        for column_index in index_list:
            currentValue = row[column_index]
            mapping.append(currentValue)
        results.append(mapping)
        mapping = [] # Clear to contain new data

    # print(results)
    return results

# JOIN FUNCTION
def joinFunction(relationData1, relationData2, attribute1, attribute2, comparison):
    # A 2-D array to return
    results = []

    #This can simply call CROSS PRODUCT then SELECT
    xProdResult = xProdFunction(relationData1, relationData2)
    # results = selectFunction(xProdResult, xProdResult[0], comparison) # no value parameter in select()

    results.append(xProdResult[0]) # append the attributes
    # print(xProdResult)

    # Get the index of attribute1 and attribute2 from the xProdResult
    attribute1_index = xProdResult[0].index(attribute1)
    attribute2_index = xProdResult[0].index(attribute2)

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
        raise ValueError(f"joinFunction()::invalid operator -> {comparison}")
    
    # Check each row of xProductResult
    for row in xProdResult[1:]:
        value_1 = row[attribute1_index]
        value_2 = row[attribute2_index]
        # Perform the operation. If the operation is true,
        # then add the current value to the "results" list
        if operation(value_1, value_2):
            results.append(row)
        
    # https://www.tutorialspoint.com/dbms/database_joins.htm
    #print(results)
    return results

#NATURAL JOIN FUNCTION
def natJoinFunction(relationData1, relationData2):
    # A 2-D array to return
    results = []
    
    # Extract common attributes between two relations
    commonAttributes = []
    for attribute in relationData1[0]:
        if attribute in relationData2[0]:
            commonAttributes.append(attribute)
    # print(commonAttributes)
    
    # Condition check to be natural join
    if len(commonAttributes) == 0:
        print("natJoinFunction::There is no common attributes between two relations.")
        return ValueError

    # Extract the index of common attribute
    indexList = []
    for commonAttribute in commonAttributes:
        index = relationData1[0].index(commonAttribute)
        indexList.append(index)
    # print(indexList)

    intersection = intersectFunction(relationData1, relationData2)
    diff1 = differnceFunction(relationData1, intersection)
    diff2 = differnceFunction(relationData2, intersection)

    # zip pairs each row from diff1 with corresponding row from diff2
    combined = [row1 + row2 for row1, row2, in zip(diff1, diff2)]
    # zip pairs each row from intersection with corresponding row from combined
    results = [row1 + row2 for row1, row2, in zip(intersection, combined)]
    
    # https://www.tutorialspoint.com/dbms/database_joins.htm   
    # print(results)
    return results


# UNION FUNCTION
# "relationData1" parameter should be a 2-D array
# "relationData2" parameter should be a 2-D array
# returns a 2-D array
def unionFunction(relationData1, relationData2):
    # An 2-D array to return
    results = []

    # Check union compatible: 
    # both relations must have the exact same attributes in the same order
    if relationData1[0] != relationData2[0]:
        print("unionFunction::Union Compatible violated")
        print("-> 2 relations must have the same attributes in the same order.")
        return ValueError()

    # Append attribute row of relationData1
    attribute_row = relationData1[0]
    results.append(attribute_row)

    # Append data tuples to results[]
    for row1 in relationData1[1:]:
        results.append(row1)
    for row2 in relationData2[1:]:
        if row2 not in results: # check row2 already exists results[]
            results.append(row2)
            
    # print(results)
    return results

# DIFFERENCE FUNCTION
# "relationData1" parameter should be a 2-D array
# "relationData2" parameter should be a 2-D array
# returns a 2-D array
def differnceFunction(relationData1, relationData2):
    # An 2-D array to return
    results = []
    
    # Extract unique attribute(s) from relationData1
    relation1_attributes = relationData1[0]
    relation2_attributes = relationData2[0]
    unique_attributes = copy.deepcopy(relationData1[0]) # deep copy the value(array)
    for attribute1 in relation1_attributes:
        for attribute2 in relation2_attributes:
            if attribute1 == attribute2:
                unique_attributes.remove(attribute1)
    results.append(unique_attributes)

    # Get the index of unique attributes(columns) from relationData1
    index_list = []
    for column in relationData1[0]:
        for attribute in unique_attributes:
            if column == attribute:
                index = relationData1[0].index(column)
                index_list.append(index)
    
    # Read the 2-D array(relationData1) row by row
    mapping = [] # temporal row
    for row in relationData1[1:]:
        for column_index in index_list:
            currentValue = row[column_index]
            mapping.append(currentValue)
        results.append(mapping)
        mapping = [] # clear to contain new data

    # print(results)
    return results

# CROSS PRODUCT FUNCTION
# "relationData1" parameter should be a 2-D array
# "relationData2" parameter should be a 2-D array
# returns a 2-D array
def xProdFunction(relationData1, relationData2):
    # A 2-D array to return
    results = []

    x_attributes = [] # combine the headers of both relations
    x_attributes.extend(relationData1[0])
    x_attributes.extend(relationData2[0])
    results.append(x_attributes)
    # print(x_attributes)

    # Multiply each row of relationData1 to each row of relationData2
    for row1 in relationData1[1:]:
        for row2 in relationData2[1:]:
            results.append(row1 + row2)

    # print(results)
    # print(len(results)) # need to subtract 1 (attribute row included)
    return results

if __name__=="__main__":
    main()