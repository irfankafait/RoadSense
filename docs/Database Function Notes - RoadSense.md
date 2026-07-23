# Database Function Notes - RoadSense

This file explains the purpose of each function in the DatabaseManager class.
It serves as a quick reference for understanding how the application communicates with MySQL.

---

# DatabaseManager

## Purpose

Handles all database operations for the RoadSense project.

Responsibilities

- Create the database
- Connect to MySQL
- Create tables
- Seed lookup tables
- Execute SELECT queries
- Insert accident records
- Close database connection

This class separates database logic from the ETL logic, making the project easier to maintain.

---

# __init__()

## Purpose

Initializes the DatabaseManager object.

## Why?

Runs automatically when the object is created.

It:

- Creates placeholders for the database connection.
- Creates placeholders for the database cursor.
- Logs that the DatabaseManager has been initialized.

## Techniques Used

- Object-Oriented Programming (OOP)
- Constructor
- Instance Variables

---

# create_database()

## Purpose

Creates the RoadSense database if it does not already exist.

## Why?

The application should automatically prepare the database before creating tables.

Instead of manually creating the database in MySQL Workbench,
the application creates it automatically.

## SQL Used

CREATE DATABASE IF NOT EXISTS

## Benefits

- Automatic setup
- Prevents duplicate databases
- Easier deployment

---

# connect()

## Purpose

Connects the application to the MySQL database.

## Why?

Every database operation requires an active connection.

After connecting, a cursor is created to execute SQL statements.

## Returns

Database connection object if successful.

Returns None if the connection fails.

## Techniques Used

- mysql.connector
- Exception Handling
- Database Cursor

---

# create_tables()

## Purpose

Creates all required tables for the project.

## Why?

Instead of writing SQL inside Python,
SQL is stored in a separate file.

Current SQL File

sql/002_create_tables.sql

The function reads the file and executes each SQL statement.

## Benefits

- Cleaner Python code
- Easier SQL maintenance
- SQL can be modified without changing Python

## Techniques Used

- File Handling
- SQL Script Execution
- String Processing

---

# seed_lookup_tables()

## Purpose

Inserts default values into lookup tables.

## Why?

Lookup tables must contain values before the ETL starts.

Example

Locations

Weather

Severity

Zones

Road Types

Without these values,
the ETL cannot convert text into foreign key IDs.

Current SQL File

sql/003_seed_lookup_tables.sql

## Techniques Used

- File Handling
- SQL Script Execution

---

# fetch_all()

## Purpose

Executes a SELECT query and returns all matching rows.

## Why?

Instead of writing SELECT logic everywhere,
all SELECT queries go through one function.

Current Usage

ETLoader

↓

load_lookup_tables()

↓

fetch_all()

## Returns

List of rows.

Returns an empty list if the query fails.

## Techniques Used

- SQL SELECT
- fetchall()
- Exception Handling

---

# insert_accidents()

## Purpose

Inserts multiple accident records into the accidents table.

## Why?

Instead of inserting one record at a time,
the function inserts many records together.

Current Method

executemany()

This is called Batch Processing.

## Benefits

- Faster inserts
- Fewer database calls
- Better scalability

## Techniques Used

- Batch Processing
- executemany()
- Transactions
- Rollback

---

# disconnect()

## Purpose

Closes the database cursor and connection.

## Why?

Every opened database connection should be closed after use.

Closing connections:

- Frees resources
- Prevents connection leaks
- Follows good database practices

## Techniques Used

- Resource Management

---

# Python Techniques Used

## Class

DatabaseManager

Purpose

Groups all database operations into one reusable object.

---

## Constructor

__init__()

Runs automatically when the object is created.

Purpose

Initialize connection and cursor variables.

---

## Instance Variables

Examples

self.connection

self.cursor

Purpose

Store database objects that are shared by all methods.

---

## try...except

Purpose

Prevent the application from crashing when a database error occurs.

Instead of

Database Error

↓

Application Stops

Use

Database Error

↓

Log Error

↓

Continue or Return

---

## mysql.connector

Purpose

Connect Python to MySQL.

Main Functions Used

connect()

cursor()

commit()

rollback()

close()


## To make clear this function: def create_database(self):

Added a fuction (**DATABASE_CONFIG) from config.py to make the 'mysql.connector.connect' clean. 


---

## Cursor

Purpose

Executes SQL statements.

Examples

SELECT

INSERT

CREATE TABLE

CREATE DATABASE

---

## SQL Script Execution

Purpose

Store SQL separately from Python.

Current Files

002_create_tables.sql

003_seed_lookup_tables.sql

Benefits

- Cleaner code
- Easier maintenance
- Better organization

---

## File Handling

Used

open()

read()

Purpose

Read SQL files from the project folder.

---

## Context Manager

Used

with open(...)

Purpose

Automatically closes the file after reading.

Benefits

- Cleaner code
- Prevents file leaks

---

## String Methods

split(';')

Purpose

Separate multiple SQL statements inside one SQL file.

strip()

Purpose

Remove extra spaces and blank lines.

---

## Transactions

commit()

Purpose

Save database changes permanently.

Used After

CREATE TABLE

INSERT

UPDATE

DELETE

---

## Rollback

rollback()

Purpose

Undo changes if an error occurs.

Why?

Prevents incomplete or corrupted data.

Example

Insert 1000 rows

↓

Error occurs

↓

Rollback

↓

Database returns to previous state.

---

## Logging

Used

logger.info()

logger.error()

Purpose

Track database operations and simplify debugging.

---

## Constants

Used

DB_HOST

DB_PORT

DB_NAME

DB_USER

DB_PASSWORD

PROJECT_ROOT

Purpose

Store configuration in one place instead of hardcoding values.

Benefits

- Easier maintenance
- More secure
- Reusable across the project

---

# Database Workflow

Application Starts

↓

Create Database

↓

Connect to MySQL

↓

Create Tables

↓

Seed Lookup Tables

↓

ETL Reads Lookup Tables

↓

Insert Accident Records

↓

Disconnect Database
