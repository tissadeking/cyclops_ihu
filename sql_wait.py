import time
import mysql.connector
from mysql.connector import Error

#let ihu app wait for sql connection to be up
#sql_func.wait_for_db()
DB_HOST = "mysql"
DB_USER = "root"
DB_PASSWORD = "password123"
DB_NAME = "cyclops"

def wait_for_mysql():
    connection = None
    retries = 10  # Maximum number of retries
    delay = 5  # Wait time between retries (in seconds)

    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}: Connecting to MySQL...")
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if connection.is_connected():
                print("✅ MySQL is ready!")
                connection.close()
                return  # Exit function
        except Error as e:
            print(f"❌ MySQL is not ready yet ({e}). Retrying in {delay} seconds...")
            time.sleep(delay)

    print("❗ MySQL connection failed after multiple attempts. Exiting...")
    exit(1)  # Exit with an error if MySQL is still unavailable

wait_for_mysql()