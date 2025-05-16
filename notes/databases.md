https://en.wikipedia.org/wiki/Cursor_(databases)  
https://en.wikipedia.org/wiki/Database_transaction  


# <u>Introduction to databases</u>

https://www.digitalocean.com/community/conceptual-articles/an-introduction-to-databases

A database is any logically modeled collection of information. In the context of websites and applications, when people refer to a database, they're often talking about a computer program that allows them to interact with their database. These programs are formally known as database management systems (DBMS). Different DBMS generally fall into two categories: relational and non-relational databases.

## <u>Relational databases</u>

Most DBMS are designed around the **relational model**, that is, they are relational DBMS or RDBMS.

The fundamental elements in the relational model are relations, also known as tables. A relation is a set of **tuples**, or rows in a table, with each tuple sharing a set of **attributes**, or columns.

![Relation](https://assets.digitalocean.com/articles/understanding_relational_dbs/tuples_chart_final.png)




How to set up MySQL:
* https://documentation.ubuntu.com/server/how-to/databases/install-mysql/index.html 
* https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql
* https://www.digitalocean.com/community/tutorials/introduction-to-queries-mysql
* https://dev.mysql.com/doc/refman/8.4/en/sql-statements.html


SQLite tutorial: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-sqlite-on-ubuntu-20-04




https://www.khanacademy.org/computing/computer-programming/sql/sql-basics/v/welcome-to-sql

Relational database - like storing data in a table/spreadsheet

Easy to form relationships between tables

Query language to interact with the database - structured query language

# <u>SQL basics</u>

## <u>Creating a table and inserting data</u>

Here's an example of how to create a table and insert data.
```sql
/** 
Grocery list: 
Bananas (4)
Peanut Butter (1)
Dark Chocolate Bars (2)
**/

/**
* Create a table named groceries with 3 columns
* PRIMARY KEY tells the database that the id column is the row ID; each row needs a unique value for this column
* Format: CREATE TABLE <table-name> (<column-name> <data-type>, <column-name> <data-type>, etc.)
**/
CREATE TABLE groceries(id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER);

INSERT INTO groceries VALUES (1, "Bananas", 4);
INSERT INTO groceries VALUES (2, "Peanut Butter", 1);
INSERT INTO groceries VALUES (3, "Dark Chocolate Bars", 2);
```