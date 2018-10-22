import requests
import zipfile
import psycopg2

# change this to aws_connection_string; example below is local db
conn = psycopg2.connect("host=localhost" dbname=postgres user=postgres")

# download the Kiva snapshot in csv format to local directory
url = "http://s3.kiva.org/snapshots/kiva_ds_csv.zip"
download = requests.get(url, allow_redirects=True)
open('kiva_ds_csv.zip', 'wb').write(download.content)

# unzip the file to local directory
kiva_csv = zipfile.ZipFile('kiva_ds_csv.zip', 'r')
kiva_csv.extractall()
kiva_csv.close()

# import csv into PostgreSQL db
cur = conn.cursor()
with open('lenders.csv', 'r') as f:
    next(f) # skips the header row
    cur.copy_from(f, 'lenders', sep=',')

conn.commit()
print("Successfully imported lenders.csv")

with open('loans_lenders.csv', 'r') as f:
    next(f) # skips the header row
    cur.copy_from(f, 'loans_lenders', sep=',')

conn.commit()
print("Successfully imported loans_lenders.csv")

with open('loans.csv', 'r') as f:
    next(f) # skips the header row
    cur.copy_from(f, 'loans', sep=',')

conn.commit()
print("Successfully imported loans.csv")
