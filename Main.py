#Luke Davidson, Jinho Nam
#CS4700
#Project 1

import csv

with open('ACTORS.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))