## Database management system in LCJ
This is a management system of a database written in an access language called LCJ and it is implemented in Python.

### Libraries not permitted to use
- csv

### Notes
- Assumes the data entries are complete, i.e. no missing data in each entry. Refer to this [issue](https://github.com/IIC2233-2016-1/syllabus/issues/287) for permission to ignore this case
- Really trying to stick to the concept of functional programming - (my take on the basic [concept](https://maryrosecook.com/blog/post/a-practical-introduction-to-functional-programming)): input -> function -> output, no data change in the middle
- Tables are dicts with column names as keys and column entries as values. Separating the columns of a table from the very beginning makes later manipulation much easier.
- **Valid table**: a table is valid if all its columns have the same number of entries, i.e. same number of rows in all columns.
- Tables are then contained in another dictionary which has table names as keys and tables as values.
- Prints complete statements as file consults are being completed, or else it's kind of hard to know when the consult progress.

### Notes on commands
- Assumes that for queries that unite two query results will not have TODO as column to return. With TODO in any one of the queries, this means that there is no order of columns in query results. The combination of two query results requires that the col_1 of table1 have the same data type as col_1 of table2, for all columns in the two tables. A random column order is used if TODO is used as column to return, this allows random error to be thrown at the ```check_type_match(type_lst1, type_lst2)``` method.
- For set operation on query results, set operation on multiple queries would be ```(single query) SET_OPERATOR (single query) SET_OPERATOR (single query)```. E.g.```(EMPRESTA Id DE personas) COMUN CN (EMPRESTA Id DE personas ONDE (sexo = 'Hombre')) UNETELO CN (EMPRESTA Id DE personas ONDE (sexo = 'Mujer'));```
- For function ```PROMEDIO(entries)```, as shown in sample query results, if the entries are in ```int``` format, the average returns as a float after the calculation of the average.


### [Helper](helper.py)
File containing helper methods, e.g. ```log_method(testing)```, a decorator for logging methods

### [Main](main.py)
The required file to hand in. Note that in main since it is not part of the implementation of LCJ, for and while loops can and are used.

### [Database](database.py)
Contains database related methods.
##### Methods
- ```read_table(fname)```
- ```read_entries_two(file, types)```
- ```read_line_two(types, line)```
- ```get_types(lst)```
- ```query_entries(table, cols, start=0, end=None)```

### [Manipulation](manipulation.py)
Contains methods that manipulates the columns of a table, e.g. filter, check columns. Also, support filter and joining entire tables.

### [Consult](consult.py)
Contains query logics. Query is done by getting a valid expression then splitting the valid expression into atomic subexpressions and evaluate subexpressions.
A subexpression contain a ```keyword``` + ```variables```, where ```variables``` can be values, columns, tables and functions.
##### ONDE
- Split overall expression into atomic conditions and connectives
- Evaluate each atomic condition with its respective column name and return a list of column indexes that meets the conditional
- Join all the returned column indexes by the connectives

### [Evaluation](evaluation.py)
Contains all the methods that help with the functions with conditional statements. The mappings:

| Symbol | Method |
| --- | --- |
| <= | ```lteq(var1, var2)``` |
| >= | ```gteq(var1, var2)``` |
| != | ```nteq(var1, var2)``` |
| < | ```lst(var1, var2)``` |
| > | ```grt(var1, var2)``` |
| = | ```eql(var1, var2)``` |
| PARECIO A | ```like(var1, var2)``` |
| ENTRE | n/a |
| EN | ```en(var1, var2)``` |
| EXISTE | ```exist(var1, var2)``` |
| Y | ```y(cond1, cond2)``` |
| O | ```o(cond1, cond2)``` |

#### Notes
- ```eval(str)``` and ```__lt()__``` were considered however, having methods that takes in two variables for the operator allow construction of functions to be used in ```filter_col(table, col, func)```
- If "PARECIO A" is used with ```int``` or ```float```, it **will** throw error, since

### Testing
According to me, all the test methods used are pretty straight forward, with longgg-ass names for each test method.

Only issue is that I am having some trouble with ```Import Errors``` using command line due to the project structure but as long as tests can be executed in pycharm.

#### [Testing consult.py](tests/test_consult.py)
Unittest file containing all the tests for consult.py

#### [Testing manipulation.py](tests/test_manip.py)
Unittest file containing all the tests for manipulation.py

### Notes
- Can deal with query of any csv files with the specified structure

### Ideas
Use metaclass to create a new class for each table, i.e. each csv file and add the columns as attributes to the created class.
Afterwards query will just make use of map, reduce and filter to query the list of objects.
The filename will be the new class name, remember to convert it to CamelCase.
