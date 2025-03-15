import mysql.connector
from mysql.connector import Error
from flask import Flask, request

#http://0.0.0.0:5001/?userid=!!06!E85QWE2VBJ6NNLV

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        #print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_db_connection("localhost", "root", "password123", "cyclops")
cursor = connection.cursor()


app = Flask(__name__)

# Function to check if a userid is valid
def is_valid_userid(userid):
    query = f"""
            SELECT username FROM users 
            WHERE userid = %s;
    """
    cursor.execute(query, (userid,))
    row = cursor.fetchone()
    #print('row: ', row)
    return row

@app.route('/')
def protected_page():
    userid = request.args.get("userid")
    if not userid or not is_valid_userid(userid):
        return "Access Denied", 403

    return f"Welcome to NLP Chat! Your userid ({userid}) is valid."


if __name__ == '__main__':
    app.run(port=5001, debug=True)
