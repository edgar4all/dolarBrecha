import mysql.connector
import config

# Connect to the database
conn = config.conn

cursor = conn.cursor()
query = "SELECT * FROM clients"
cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
    msg= ""
    for i in range(len(row)):
        msg += "  -  " + str(row[i])
    print( msg)
cursor.close()
conn.close()