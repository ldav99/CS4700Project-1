# CS4700 Project 1
Jinho Nam and Luke Davidson


## How to run the program
- Clone this repository
- Write any queries in RAQueries.txt
- Run `Main.py`

## Implemented Operators/Queries
    * SELECT
    * PROJECT
    * INTERSECT
    * JOIN
    * NATURAL JOIN
    * UNION
    * DIFFERENCE
    * CROSS PRODUCT
    
    - Some of the queries work on relational algebra format, such as
        > SELE_{Payment > 70} (PAY)
        > (PROJ_{ANO} (SELE_{Payment > 90} (PAY)))
          This is the left side of the union operator, which is 
          (PROJ_{ANO} (SELE_{Payment > 90} (PAY))) U (PROJ_{ANO} (SELE_{ANAME=’Swanson’} (ACTORS)))


## Screenshots 
- Select operator in relational algebra
![SELECT-relational-algebra](./images/select-operator.png)

- Left side of union operator in relational algebra
    (underlined blue line is the left query)
![Left-side-of-UNION](./images/left-query-of-union-operator.png)
## Output
