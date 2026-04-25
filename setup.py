# Setup to create the CSV data using different DB's
import csv
import os
import sqlite3

#Delete if the db is existed
def del_existing_db(db_name):
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"Deleted existing DB: {db_name}")
    else:
        print(f"No existing DB found: {db_name}")

# Insert the data into the db by reading the csv file
def insert_data(csv_file):
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file) # Can also use pandas: pd.read_csv(file_path) & Normal: csv.reader(file)
        for rows in reader:
            cursor.execute(
                '''Insert INTO Customer (customer_id, zipcode, city, state_code, datetime_created, datetime_updated)
                VALUES (?, ?, ?, ?, ?, ?)''',
            (
                rows["customer_id"],
                rows["zipcode"],
                rows["city"],
                rows["state_code"],
                rows["datetime_created"],
                rows["datetime_updated"]
             )
            )

# Cheking the the db available are not
del_existing_db('tpch.db')
del_existing_db('duckdb.db')

# Connect to the SQLite tpch DataBase
conn = sqlite3.connect('tpch.db')
cursor = conn.cursor()

# Cerate a table structure
cursor.execute(" DROP TABLE IF EXISTS Customer ")
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS Customer(
    customer_id INTEGER PRIMARY KEY,
    zipcode TEXT,
    city TEXT,
    state_code TEXT,
    datetime_created TEXT,
    datetime_updated TEXT
    )'''
)

# Inserting CSV into the Table.
insert_data("./data/customers.csv")

# Close the DB connection
conn.close()
print("Created Table and Inserted the data.")

import duckdb

# duckDB connection
duckdb_conn = duckdb.connect("ducdb.db")

# Create the Customers tables
duckdb_conn.execute("DROP TABLE IF EXISTS Customer")
duckdb_conn.execute(
    '''
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INTEGER,
    zipcode TEXT,
    city TEXT,
    state_code TEXT,
    datetime_created TIMESTAMP,
    datetime_updated TIMESTAMP
)
'''
)

# Weather Table
duckdb_conn.execute("DROP TABLE IF EXISTS WeatherData")
duckdb_conn.execute(
    """
CREATE TABLE IF NOT EXISTS WeatherData (
    id TEXT,
    date TEXT,
    element TEXT,
    value INTEGER,
    m_flag TEXT,
    q_flag TEXT,
    s_flag TEXT,
    obs_time TEXT
)
"""
)

# Exchanges Table
duckdb_conn.execute("DROP TABLE IF EXISTS Exchanges")
duckdb_conn.execute(
    """
CREATE TABLE IF NOT EXISTS Exchanges (
    id TEXT,
    name TEXT,
    rank INTEGER,
    percentTotalVolume FLOAT,
    volumeUsd FLOAT,
    tradingPairs TEXT,
    socket BOOLEAN,
    exchangeUrl TEXT,
    updated BIGINT 
)
"""
)

# Commit and close connection
duckdb_conn.commit()
duckdb_conn.close()

print("Customer table created successfully!")

import random
import datetime
# Generate the data and store in Sample_data.CSV
def generate_name():
    first_names = [
        "Alice",
        "Bob",
        "Charlie",
        "David",
        "Emma",
        "Frank",
        "Grace",
        "Henry",
        "Ivy",
        "Jack",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Rodriguez",
        "Martinez",
    ]
    return random.choice(first_names) + " " + random.choice(last_names)

def generate_age():
    return random.randint(18,70)

def generate_gender():
    return random.choice(['M','F'])

def generate_purchase_amount():
    return round(random.uniform(10,1000) ,2)

def generate_date():
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)
    random_date = start_date + datetime.timedelta(days= random.randint(0,365))
    return random_date.strftime("%Y-%m-%d")

with open("./data/sample_data.csv","w", newline="") as csv_file:
    fieldname = [
        "Customer_ID",
        "Customer_Name",
        "Age",
        "Gender",
        "Purchase_Amount",
        "Purchase_Date",
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldname)

    writer.writeheader()
    for i in range(100):
        writer.writerow(
            {
                "Customer_ID":i+1,
                "Customer_Name": generate_name(),
                "Age": generate_age(),
                "Gender": generate_gender(),
                "Purchase_Amount":generate_purchase_amount(),
                "Purchase_Date":generate_date(),
            }
        )

print("CSV file generated successfully!")