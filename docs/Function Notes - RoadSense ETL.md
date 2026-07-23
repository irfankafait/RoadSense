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
