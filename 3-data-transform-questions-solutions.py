print(
    "################################################################################"
)
print("Use standard python libraries to do the transformations")
print(
    "################################################################################"
)

# Question: How do you read data from a CSV file at ./data/sample_data.csv into a list of dictionaries?
import csv
data = []
with open('./data/sample_data.csv','r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)
# print(data)

# Question: How do you remove duplicate rows based on customer ID?
data_unique = []
customer_ids = set()

for row in data:
    if row['Customer_ID'] not in customer_ids:
        data_unique.append(row)
        customer_ids.add(row['Customer_ID'])
    else:
        print(f'Duplicate customer record found {row['Customer_ID']}')

# Question: How do you handle missing values by replacing them with 0?
for row in data_unique:
    if not row['Age']:
        print(f'Customer {row['Customer_ID']} not have Age')
        row['Age'] = 0
    if not row['Purchase_Amount']:
        row['Purchase_Amount'] = 0.0
# Question: How do you remove outliers such as age > 100 or purchase amount > 1000?
data_cleaned = [
    row
    for row in data_unique
    if int(row["Age"]) <=100 and float(row['Purchase_Amount']) >=1000
]
print(data_cleaned)
# Question: How do you convert the Gender column to a binary format (0 for Female, 1 for Male)?
for row in data_unique:
    if row['Gender'] == 'F':
        row['Gender'] = 0
    if row['Gender'] == 'M':
        row["Gender"] = 1
# print(data_unique)
# Question: How do you split the Customer_Name column into separate First_Name and Last_Name columns?
for row in data_unique:
    first_name, last_name = row['Customer_Name'].split(" ",1)
    row['first_name'] = first_name
    row['last_name'] = last_name
# print(data_unique)  
# Question: How do you calculate the total purchase amount by Gender?
f_purchase = 0
m_purchase = 0
for row in data_unique:
    if row['Gender'] == 1:
        f_purchase = f_purchase + float(row['Purchase_Amount'])
    if row['Gender'] == 0:
        m_purchase = m_purchase + float(row['Purchase_Amount'])
print(f'Female purchase: {f_purchase}')
print(f'Male purchase: {m_purchase}')
# Question: How do you calculate the average purchase amount by Age group?
# assume age_groups is the grouping we want
# hint: Why do we convert to float?
age_groups = {"18-30": [], "31-40": [], "41-50": [], "51-60": [], "61-70": []}
for row in data_unique:
    age = int(row['Age'])

    if age <= 30:
        age_groups["18-30"].append(float(row["Purchase_Amount"]))
    elif age <= 40:
        age_groups["31-40"].append(float(row["Purchase_Amount"]))
    elif age <= 50:
        age_groups["41-50"].append(float(row["Purchase_Amount"]))
    elif age <= 60:
        age_groups["51-60"].append(float(row["Purchase_Amount"]))
    elif age <= 70:
        age_groups["61-70"].append(float(row["Purchase_Amount"]))
for k,v in age_groups.items():
    age_groups[k] = sum(v)/len(v)
print(age_groups)

# Question: How do you print the results for total purchase amount by Gender and average purchase amount by Age group?
your_total_purchase_amount_by_gender = {'Female':f_purchase, 'Male':m_purchase} # your results should be assigned to this variable
average_purchase_by_age_group = age_groups # your results should be assigned to this variable

print(f"Total purchase amount by Gender: {your_total_purchase_amount_by_gender}")
print(f"Average purchase amount by Age group: {average_purchase_by_age_group}")

print(
    "################################################################################"
)
print("Use DuckDB to do the transformations")
print(
    "################################################################################"
)

# Question: How do you connect to DuckDB and load data from a CSV file into a DuckDB table?
# Connect to DuckDB and load data
import duckdb

duckdb_connector = duckdb.connect(database=":memory:", read_only=False)
duckdb_connector.execute( "CREATE TABLE data (Customer_ID INTEGER, Customer_Name VARCHAR, Age INTEGER, Gender VARCHAR, Purchase_Amount FLOAT, Purchase_Date DATE)"
)


# Read data from CSV file into DuckDB table
duckdb_connector.execute("COPY data FROM './data/sample_data.csv' WITH HEADER CSV ")
# Question: How do you remove duplicate rows based on customer ID in DuckDB?
duckdb_connector.execute("CREATE TABLE data_unique AS SELECT DISTINCT * FROM  data")
# Question: How do you handle missing values by replacing them with 0 in DuckDB?
duckdb_connector.execute("CREATE TABLE data_cleaned AS SELECT CUSTOMER_ID, COALESCE(Age, 0) AS Age, Gender, COALESCE(Purchase_Amount, 0) AS Purchase_Amount, Purchase_Date FROM data_unique")
# Question: How do you remove outliers (e.g., age > 100 or purchase amount > 1000) in DuckDB?
duckdb_connector.execute("CREATE TABLE data_cleaned_outliers AS SELECT * FROM data_unique WHERE Age <= 100 and purchase_amount <= 1000")
# Question: How do you convert the Gender column to a binary format (0 for Female, 1 for Male) in DuckDB?
duckdb_connector.execute("CREATE TABLE data_cleaned_gender AS SELECT *, CASE WHEN GENDER='F' THEN 0 ELSE 1 END AS GENDER_BINARY FROM data_unique")
# Question: How do you split the Customer_Name column into separate First_Name and Last_Name columns in DuckDB?
duckdb_connector.execute("CREATE TABLE data_cleaned_c AS SELECT CUSTOMER_ID, SPLIT_PART(Customer_name,' ',1) AS First_name, SPLIT_PART(Customer_name,' ',2) AS Last_name, Age, Gender_Binary, Purchase_Amount, Purchase_Date FROM data_cleaned_gender")
# Question: How do you calculate the total purchase amount by Gender in DuckDB?
total_pur_gender = duckdb_connector.execute("SELECT GENDER_BINARY, SUM(Purchase_amount) AS TOTAL_PURCHASE_AMOUNT FROM data_cleaned_gender GROUP BY Gender_binary").fetchall()
# Question: How do you calculate the average purchase amount by Age group in DuckDB?
avg_pur = duckdb_connector.execute("SELECT CASE WHEN AGE BETWEEN 18 AND 30 THEN '18-30' WHEN AGE BETWEEN 31 AND 40 THEN '31-40' WHEN Age BETWEEN 41 AND 50 THEN '41-50' WHEN AGE BETWEEN 51 AND 60 THEN '51-60' ELSE '61-70' END AS Age_grp, AVG(Purchase_amount) FROM data_unique GROUP BY Age_grp").fetchall()
# Question: How do you print the results for total purchase amount by Gender and average purchase amount by Age group in DuckDB?
print("====================== Results ======================")
print(f"Total purchase amount by Gender:{total_pur_gender}")
print(f"Average purchase amount by Age group:{avg_pur}")
