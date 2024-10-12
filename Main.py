#Luke Davidson, Jinho Nam
#CS4700
#Project 1

import csv

with open('ACTORS.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))


def main():
    userQuery = str(input('Enter your query here: '))
    print(userQuery)





#Results need to be stored in output file
#This will be neede towards the end
    outputFile = open('RAoutput.csv', 'w')
    outputFile.write(f'{userQuery}\n')
    #outputFile.write(f'{queryResult}\n\n')

    outputFile.close()

main()