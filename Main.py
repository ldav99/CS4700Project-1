#Luke Davidson, Jinho Nam
#CS4700
#Project 1

import ast
import copy
import csv
import operator
import string

#Main
def main():
#Open the RAqueries file and count the number of lines
    queryList = []
    queryFile = open('RAQueries.txt', 'r')
    lines = len(queryFile.readlines())
    queryFile.close()

#Re-Open file to read contents and put them in a list
    queryFile = open('RAQueries.txt', 'r')

    for i in range(1,lines+1):
        query = str(queryFile.readline())
        query = query.strip('\n')
        queryList.append(query)
    queryFile.close()

#Set global variables for all the datasets to be used in dictionaries
    global PAY 
    global MOVIES
    global ACTORS
    PAY = './data/PAY.csv'
    MOVIES = './data/MOVIES.csv'
    ACTORS = './data/ACTORS.csv'

#Reformat the datasets to 2D arrays for functions
    PAY = reformat_to_2Darray(PAY)
    MOVIES = reformat_to_2Darray(MOVIES)
    ACTORS = reformat_to_2Darray(ACTORS)

    outputFile = open('RAoutput.csv', 'w')

#Run program on all queries and print to RAoutput.csv (COMMENTED FOR NOW)
    # for i in range(0,len(queryList)):
    #     parsedQuery = parseQuery(queryList[i])
    #     outputFile.write(f'{queryList[i]}:\n')
    #     outputFile.write(f'{callFunction(parsedQuery)}\n\n\n')

    #outputFile.close()

############################################################################################################################

    # query = parseQuery(queryList[3])
    # print(f'{query}:')
    # print(callFunction(query))

    queryTwo = parseQuery(queryList[1])
    print(f'{queryTwo}:')
    print(callFunction(queryTwo))

    # testQ = parseQuery('(SELE_{Payment < 60} (PAY))')
    # print(f'TEST QUERY: {testQ}')
    # print(callFunction(testQ))
    # testTwo = parseQuery('(SELE_{Payment < 60} (PAY))')
    # funOne = callFunction(testTwo)
    # testQ = parseQuery('(PROJ_{ANO} (SELE_{Payment < 60} (PAY))')
    # funTwo = callFunction(testQ)
    # # print(f'TEST QUERY: {testQ}')
    # # print(callFunction(testQ))
    # print(f'ONE {funOne}')
    # print(f'TWO {funTwo}')
    # print('HERE-----------')
    # print(differnceFunction(funOne, funTwo))

    # print(selectFunction(PAY, ['Payment'], '>', 70))
    #print(projectFunction(intersectFunction(ACTORS, PAY), "ANO"))

    Faculty = [['Class','Dept','Position'],
               [5,'CSE','Assistant Professor'],
               [5,'CSE','Assistant Professor'],
               [6,'EE','Assistant Professor'],
               [6,'EE','Assistant Professor']]
    proj_result = projectFunction(Faculty, 'Position')
    # print(proj_result)

    #natJoin_result = natJoinFunction(ACTORS, PAY)
    # print(natJoin_result)
    # print("")
    #project_result = projectFunction(natJoin_result, 'ANO')
    #print(project_result)

    # testOne = ['1','5','6','8','9', 'word']
    # testTwo = ['1','2','4','8','9']
    # print(intersectFunction(testOne, testTwo))
    # print(selectFunction(PAY, 'Payment', '>', 70)) # Test SELECT
    # print(selectFunction(PAY, 'Payment', '>=', 70)) # Test SELECT
    # print(selectFunction(PAY, 'Payment', '<', 60)) # Test SELECT
    # print(selectFunction(PAY, 'Payment', '<=', 60)) # Test SELECT
    # print(selectFunction(PAY, 'Payment', '=', 1)) # Test SELECT
    # print(selectFunction(PAY, 'ANO', '=', 'A4')) # Test SELECT
    # print(projectFunction(PAY, 'ANO'))
    # print(projectFunction(selectFunction(PAY, 'Payment', '>', 70), 'ANO')) # Test PROJECT & SELECT
    # intersectFunction(PAY, MOVIES)
    # print(differnceFunction(PAY, MOVIES))
    # result_left = projectFunction(selectFunction(PAY, 'Payment', '>', 70), 'ANO')
    # print(result_left)
    # result_right = projectFunction(selectFunction(PAY, 'Payment', '<', 60), 'ANO')
    # print(result_right)
    # difference_left_right = differnceFunction(result_left, result_right)
    # print(difference_left_right)

    COURSES = [['CID','Course','Dept'],
               ['CS01','Database','CS'],
               ['ME01','Mechanics','ME'],
               ['EE01','Electronics','EE']]
    HoD = [['Dept','Head'],
           ['CS','Alex'],
           ['ME','Maya'],
           ['EE','Mira']]
    result_inner = natJoinFunction(COURSES, HoD)
    # print(result_inner)

    # result_inner = natJoinFunction(ACTORS, PAY)
    # print(result_inner)
    # result_outer = projectFunction(result_inner, 'ANO')
    # print(result_outer)
    # xProdFunction(PAY, MOVIES)
    # unionFunction(PAY, MOVIES)
    # natJoinFunction('MOVIES.csv', 'PAY.csv') 
    # joinFunction(MOVIES, PAY, "MNO", "MNO", "=") # has an issue in select()
    # joinFunction(Student, Subjects, "Std", "Class", "=")
    #print(natJoinFunction(Courses, HoD))

######################################################################################################################

def reformat_to_2Darray(csvfile):
    # data = list(csv.reader(open(csvfile)))
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        data = []
        for row in reader:
            parsed_row = [] # A list to store the converted values
            for cell in row:
                # Convert each cell to its original data type
                try:
                    parsed_row.append(ast.literal_eval(cell))
                # If can't convert, leave it as string
                except:
                    parsed_row.append(cell)
            data.append(parsed_row)
    
    return data

#PARSE FUNCTION Takes the inputed query and removes any symbols that arent in the opperator list
def parseQuery(inputQuery):
    operatorList = [">=", ">" , "!=" , "=", "<=", "<", "*", "-"]

    for char in string.punctuation:
        if char in operatorList:
            continue
        inputQuery = inputQuery.replace(char, ' ')

    return(inputQuery)

#Analyze query function
def analyzeQuery(queryHalf, splitList, relations, relation):
    if 'SELE' in queryHalf:
        wordIndex = queryHalf.index('SELE')
        attributes = queryHalf[wordIndex + 1]
        comparison = queryHalf[wordIndex + 2]
        value = queryHalf[wordIndex + 3]
        addCSV = relations.get(relation)
        selectResults = selectFunction(addCSV, attributes, comparison, value)
        if 'PROJ' in queryHalf:
            wordIndex = queryHalf.index('PROJ')
            projAttribute = queryHalf[wordIndex + 1]
            halfResult =  projectFunction(selectResults, projAttribute)
            return halfResult
        else:
            return selectResults
    elif 'PROJ' in queryHalf:
        wordIndex = queryHalf.index('PROJ')
        projAttribute = queryHalf[wordIndex + 1]
        halfResult =  projectFunction(relation, projAttribute)
        return halfResult


#Split the lsit based on what charcter is in the list
def splitTheList(splitList, splitChar, relations):
    wordIndex = splitList.index(splitChar)

    firstHalf = splitList[:wordIndex]
    secondHalf = splitList[wordIndex+1:]

#Get the relations that the two queries use
    firstrelation = len(firstHalf)
    thefirstRelation = firstHalf[firstrelation-1]
#Check for natural join
    if firstHalf[firstrelation-2] == '*':
        joinRelationOne = firstHalf[firstrelation - 3]
        joinedRelation = natJoinFunction(relations.get(joinRelationOne), relations.get(thefirstRelation))
        thefirstRelation = joinedRelation
    secondrelation = len(secondHalf)
    thesecondRelation = secondHalf[secondrelation-1]
#Check for natural join
    if secondHalf[secondrelation-2] == '*':
        joinRelationOne = secondHalf[secondrelation - 3]
        joinedRelation = natJoinFunction(relations.get(joinRelationOne), relations.get(thesecondRelation))
        thesecondRelation = joinedRelation

    return firstHalf, secondHalf, thefirstRelation, thesecondRelation

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

    firstrelation = []
    thefirstRelation = []
    secondrelation = []
    thesecondRelation = []

    for word in splitQuery:
        splitList.append(word)


#If there is a union or difference or intersection split the list before and after the U
    if 'U' in splitList:
        firstHalf, secondHalf, thefirstRelation, thesecondRelation = splitTheList(splitList,'U', relations)
        firstHalfResult = analyzeQuery(firstHalf, splitList, relations, thefirstRelation)

        if len(secondHalf) != 0:
            secondHalfResult = analyzeQuery(secondHalf, splitList, relations, thesecondRelation)

        #return unionFunction(firstHalfResult, secondHalfResult)
#Difference
    elif '-' in splitList:
        firstHalf, secondHalf, thefirstRelation, thesecondRelation = splitTheList(splitList,'-', relations)
        firstHalfResult = analyzeQuery(firstHalf, splitList, relations, thefirstRelation)

        if len(secondHalf) != 0:
            secondHalfResult = analyzeQuery(secondHalf, splitList, relations, thesecondRelation)

        return differnceFunction(firstHalfResult, secondHalfResult)
#Intersection
    elif 'INTE' in splitList:
        firstHalf, secondHalf, thefirstRelation, thesecondRelation = splitTheList(splitList,'INTE', relations)
        firstHalfResult = analyzeQuery(firstHalf, splitList, relations, thefirstRelation)

        if len(secondHalf) != 0:
            secondHalfResult = analyzeQuery(secondHalf, splitList, relations, thesecondRelation)

        return intersectFunction(firstHalfResult, secondHalfResult)
    else:
#Else it doesnt need anything above so it just needs to check for select and project
        firstHalf.extend(splitList)
        firstrelation = len(firstHalf)
        thefirstRelation = firstHalf[firstrelation-1]
        #Check for natural join
        if firstHalf[firstrelation-2] == '*':
            joinRelationOne = firstHalf[firstrelation - 3]
            joinedRelation = natJoinFunction(relations.get(joinRelationOne), relations.get(thefirstRelation))
            thefirstRelation = joinedRelation
        
        return analyzeQuery(firstHalf, splitList, relations, thefirstRelation)


# SELECT FUNCTION
# "relationData" parameter should be a 2-D array
# "attributes" parameter should be a string
# returns 2-D array
def selectFunction(relationData, attribute, comparison, value):
    # A 2-D array to return for this function
    results = []

    # A dictionary to handle a value assigned to comparison
    operators = {
        "<": operator.lt, 
        "<=": operator.le,
        "=": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge
    }

    # Check if "comparison" is a operator in the dictionary
    # Otherwise, throw an error
    try:
        operation = operators.get(comparison)
    except:
        raise ValueError(f"selectFunction()::invalid operator -> {comparison}")

    # Get the index of the target attribute(column)
    for column in relationData[0]: # attribute row = relationaData[0]
        if column == attribute:
            column_index = relationData[0].index(column)            
    results.append(relationData[0])

    # Read the 2-D array(relationData) row by row
    for row in relationData[1:]:
        criterionValue = value
        currentValue = row[column_index]

        # If the data type of currentValue is int
        if isinstance(currentValue, int):
            if (comparison == '<') or (comparison == '<='):
                if operation(int(currentValue), int(criterionValue)):
                    results.append(row)
            elif (comparison == '>') or (comparison == '>=') :
                if operation(int(currentValue), int(criterionValue)):
                    results.append(row)
            elif operation(int(currentValue), int(criterionValue)):
                results.append(row)
        # Else the data type of currentValue is str
        else:
            if operation(criterionValue, currentValue):
                results.append(row)
    
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
    duplicate_check = [] # temporal row
    for row in relationData[1:]:
        for column_index in index_list:
            currentValue = row[column_index]
            if currentValue not in duplicate_check:
                mapping.append(currentValue)
                duplicate_check.append(currentValue)
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

    # Do cross-product of them
    cross_product = xProdFunction(relationData1, relationData2)    

    # Extract common attributes between two relations
    commonAttributes = []
    for attribute in relationData1[0]:
        if attribute in relationData2[0]:
            commonAttributes.append(attribute)
    # print(commonAttributes)
    
    # Condition check to be natural join
    if len(commonAttributes) == 0:
        print("natJoinFunction::Natural Join Condition violated")
        print(f"-> There is no common attributes between two relations. {relationData1},{relationData2}")
        return ValueError

    # Add the attributes of the result of natural join to results[]
    result_attributes = relationData1[0]

    # Add unique attributes to results[]
    for attribute in relationData2[0]:
        if attribute not in commonAttributes:
            result_attributes.append(attribute)
    results.append(result_attributes)

    # index list of the common attributes in both relations
    indices_relation_1 = []
    indices_relation_2 = []
    for attribute in commonAttributes:
        indices_relation_1.append(relationData1[0].index(attribute))
    for attribute in commonAttributes:
        indices_relation_2.append(relationData2[0].index(attribute))
    
    # Compare rows from both relations to find common attribute values
    # If common attribute values are equal, combine rows
    for row1 in relationData1[1:]:
        for row2 in relationData2[1:]:
            # Check if common attribute values match
            attributes_equal = True
            for i, j in zip(indices_relation_1, indices_relation_2):
                # Compare the value of the common attribute in row1 with the value in row2
                if row1[i] != row2[j]:
                    attributes_equal = False
                    break
            # If commmon attribute values are equal, combine rows
            if attributes_equal:
                # new_row = a copy of row1
                new_row = row1[:]
                # Add values from row2 that aren't part of the common attributes
                for k in range(len(row2)):
                    if k not in indices_relation_2:
                        new_row.append(row2[k])
                results.append(new_row)
        

    
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

    # Remove duplicated elements in relationData1
    unique_relationData1 = []
    unique_relationData1.append(relationData1[0])
    for element in relationData1[1:]:
        if element not in unique_relationData1:
            unique_relationData1.append(element)

    # Perform relationData1 - relationData2
    for row in unique_relationData1[1:]:
        if row in relationData2[1:]:
            unique_relationData1.remove(row)
    
    results = unique_relationData1
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