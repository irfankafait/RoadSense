# Function Notes - RoadSense ETL

This file explains the purpose of each function in the ETL pipeline.
It is written as a quick reference for future review.

---

# ETLoader

## Purpose

The main class responsible for executing the complete ETL (Extract, Transform, Load) pipeline.

Responsibilities:
- Connect to the database
- Load lookup tables
- Read cleaned CSV
- Validate data
- Transform data
- Load data into MySQL
- Log the pipeline execution

---

# __init__()

## Purpose

Initializes the ETL Loader.

## Why?

Runs once when the ETLoader object is created.

It:
- Creates a DatabaseManager object.
- Connects to MySQL.
- Creates empty dictionaries for lookup tables.
- Prepares the ETL pipeline.

## Techniques Used

- Object-Oriented Programming (OOP)
- Class Constructor
- Database Connection

---

# load_lookup_tables()

## Purpose

Loads all lookup tables into Python dictionaries.

## Why?

Instead of querying MySQL for every CSV row,
lookup tables are loaded only once.

Example

Before

CSV Row
↓

SELECT location_id...

After

CSV Row
↓

self.locations["Lahore"]

## Benefits

- Faster
- Less database traffic
- Better performance

---

# _load_lookup_dictionary()

## Purpose

Generic function that loads any lookup table.

## Why?

Avoid writing the same code multiple times.

Without this function:

load_locations()

load_weather()

load_zone()

...

With this function:

_load_lookup_dictionary()

works for every lookup table.

## Techniques Used

- SQL SELECT
- Dictionary Comprehension
- Generic Function

---

# validate_columns()

## Purpose

Checks whether the CSV contains all required columns.

## Why?

Prevents processing an invalid CSV.

If a required column is missing,
the pipeline stops immediately.

Example

Missing

weather

↓

transform_row()

would fail.

---

# validate_row()

## Purpose

Validates one CSV record.

## Checks

- Location exists
- Zone exists
- Weather exists
- Severity exists
- Road Type exists
- Hour is between 0–23

## Why?

Bad records should be skipped,
not crash the whole ETL.

## Techniques Used

- Dictionary Lookup
- Data Validation
- Logging

---

# transform_row()

## Purpose

Converts one CSV row into a database-ready tuple.

## Why?

CSV stores text.

Database stores foreign key IDs.

Example

CSV

Location = Lahore

↓

Database

location_id = 1

## Techniques Used

- Dictionary Lookup
- Foreign Keys
- Database Normalization

---

# load()

## Purpose

Loads transformed records into MySQL.

## Why?

Keeps database insertion separate from ETL logic.

Current Method

insert_accidents(records)

Future

Can be changed without affecting the rest of the ETL.

---

# run()

## Purpose

Controls the complete ETL process.

## Execution Flow

1. Connect to database
2. Start timer
3. Load lookup tables
4. Read cleaned CSV
5. Validate columns
6. Loop through rows
7. Validate row
8. Transform row
9. Store records in batch
10. Insert into MySQL
11. Insert remaining records
12. Disconnect database
13. Display execution time

This is the main function of the ETL pipeline.

---

# Python Techniques Used

## Dictionary

Used for lookup tables.

Why?

Fast key lookup.

Example

self.locations["Lahore"]

---

## Dictionary Comprehension

Used in

_load_lookup_dictionary()

Purpose

Create dictionaries directly from SQL results.

Example

{
    name: record_id
    for record_id, name in rows
}

---

## Class

ETLoader

Purpose

Group related ETL functions together.

Benefit

Cleaner and reusable code.

---

## Constructor

__init__()

Runs automatically when the object is created.

Purpose

Initialize variables and connect to the database.

---

## Instance Variables

Examples

self.db

self.locations

self.weather

Purpose

Store data that can be used by every function inside the class.

---

## f-string

Used for dynamic SQL.

Example

f"SELECT {id_column} FROM {table_name}"

Purpose

Build SQL queries dynamically.

---

## enumerate()

Used in

for index, row in enumerate(...)

Purpose

Keep track of row numbers.

Useful for logging errors.

---

## itertuples()

Used to iterate through DataFrame rows.

Chosen over iterrows() because it is faster and uses less memory.

---

## Batch Processing

Purpose

Insert many records together instead of one by one.

Current

records.append(...)

↓

Insert when

len(records) >= BATCH_SIZE

Benefits

- Faster
- Fewer database calls
- Lower memory usage

---

## try...except

Purpose

Prevent one bad row from stopping the ETL.

Instead of crashing,

Log the error

↓

Skip the row

↓

Continue processing.

---


## Failed Records Reporting

Till now, we have only the functions that records ERROR, Unknown Location, and Skipping row 241 or we need to
find the log file to check which rows are missing.

The professional solution is to create a CSV file which contain the failed rows record. 

function used:

failed_record = []



## Create environment variable file

.env file is created to make the database name, password, username or other secret information confidential.

Create a new function "def get_required_env(variable_name):" to read required environment variables and raise an early error in config.py. Then change os.getenv to get_required_env function. Also created DATABASE_CONFIG dictionary to make the MySQL connection clean in database.py. 

The ** operator unpacks the dictionary into keyword arguments.
This keeps the connection code cleaner and makes it easier to add new settings later.







## Logger

Used for

logger.info()

logger.warning()

logger.error()

logger.exception()

Purpose

Track ETL execution and help debugging.

---

## perf_counter()

Purpose

Measure ETL execution time.

Useful for comparing performance after optimization.

---

## Pandas

Used for

read_csv()

Purpose

Load CSV into a DataFrame for processing.

---

## Database Normalization

Instead of storing repeated text,

Store IDs.

Example

Weather

Rain

↓

weather_id = 2

Benefits

- Less storage
- Better consistency
- Faster joins

---

# Overall ETL Workflow

Cleaned CSV

↓

Validate Columns

↓

Validate Row

↓

Transform Text → IDs

↓

Batch Processing

↓

Insert into MySQL

↓

Logging

↓

Pipeline Completed



## Unit Testing

There are different types of testing.

| Type             | Purpose                                      |
| ---------------- | -------------------------------------------- |
| Unit Test        | Tests one function or method in isolation.   |
| Integration Test | Tests how multiple components work together. |
| System Test      | Tests the complete application.              |
| End-to-End Test  | Simulates a real user workflow.              |


We will pytest rather than unittest. Because it is good. But the Python community overwhelmingly prefers

Why?

Simpler syntax.
Better error messages.
Less boilerplate.
Powerful fixtures.
Large ecosystem.
Widely used in industry.

Why import ETLLoader class? Because we are testing its methods.

## Dependency Injection

A design technique where an object receives the objects it depends on from outside instead of creating them internally.

I have changed the ETLoader() class to remove the dependency on DataBase Manager (For example, ETLoader() conect to SQL Database everytime) through this techneque. By this we can make easier testing, replacing,and maintaining.

## Loose Coupling

Components know as little as possible about each other, making them easier to replace, test, and maintain.



## FastAPI Architecture


Browser: Browser sends an HTTP request.
   ↓
FastAPI: FastAPI receives every incoming request.
   ↓
Router: FastAPI finds the correct router for the requested URL. At startup, FastAPI registered that router. app.include_router(statistics_router)
   ↓
Service: The service contains the business logic and asks the DatabaseManager to execute SQL queries.
   ↓
DatabaseManager: The DatabaseManager executes SQL queries on the MySQL database and fetches the results.
   ↓
MySQL: MySQL returns raw data.
   ↓
Pydantic: Does this dictionary match the expected model? Without Pydantic, the frontend would receive inconsistent data.
   ↓
Browser

1. The browser sends an HTTP request.

↓

2. FastAPI receives the request.

↓

3. FastAPI checks which router owns the URL.

↓

4. The router calls the appropriate service method.

↓

5. The service contains the business logic.

↓

6. The service asks DatabaseManager to execute SQL.

↓

7. DatabaseManager communicates with MySQL.

↓

8. MySQL returns raw data.

↓

9. The service converts raw SQL results into a structured Python dictionary.

↓

10. Pydantic validates that the dictionary matches the expected API response model.

↓

11. FastAPI converts the validated data into JSON.

↓

12. The browser receives the JSON response.


## SQL Injection

This category of vulnerability is called SQL Injection, and avoiding it is a fundamental security practice.

## The Repository

Talk to the database in terms of RoadSense's business concepts.
The Problem

Open your

src/services/accident_service.py

Your service currently contains SQL like this:

SELECT COUNT(*)
FROM accidents

Then another SQL query.

Then another.

Then another.

Eventually this file becomes

800 lines

1200 lines

1800 lines

because every feature adds more SQL. Repository solve this problem.



## Returning Pydantic Models Instead of Dictionaries

The browser sends a request to router. Then router receives it and send to service. Then service asks the repository. Then repository send it to database. Database returns raw values 1250, 230, (17, 96), ("Mall Road", 180). Then service manually creates a dictionary. Finally FastAPI converts that dictionary into JSON.
Is That Wrong? No. Python dictionaries are perfectly valid. But let's imagine RoadSense becomes much larger. Statistics, Weather, Hotspots, AI Analysis, Predictions, Reports, Alerts, Recommendations. 
Now every service builds dictionaries. Soon you'll have thousands of lines like      return {...}
This becomes repetitive.

## The Solution

So we convert these dictionaries to Pydantic Ojects. FastAPI internally performs serialization and convert it to JSON.


