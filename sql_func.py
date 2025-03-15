import mysql.connector
from mysql.connector import Error

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

#connection = create_db_connection("localhost", "root", "password123", "cyclops")
connection = create_db_connection("mysql", "root", "password123", "cyclops")
cursor = connection.cursor()

def insert_data(email, username, password, userid):
    user_update = "INSERT INTO users (email, username, password, userid) VALUES (%s, %s, %s, %s)"
    lval2 = (email, username, password, userid)
    cursor.execute(user_update, lval2)
    connection.commit()

def check_data(username, password):
    query = f"""
            SELECT * FROM users 
            WHERE username = %s and password = %s;
    """
    cursor.execute(query, (username, password))
    existing_entry = cursor.fetchone()
    return existing_entry

def check_email(email):
    query = f"""
            SELECT * FROM users 
            WHERE email = %s;
    """
    cursor.execute(query, (email,))
    existing_entry = cursor.fetchone()
    return existing_entry

def check_username(username):
    query = f"""
            SELECT * FROM users 
            WHERE username = %s;
    """
    cursor.execute(query, (username,))
    existing_entry = cursor.fetchone()
    return existing_entry

# Fetch userid from the database
def get_userid(username):
    query = f"""
            SELECT userid FROM users 
            WHERE username = %s;
    """
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    return row[0] if row else None

def insert_data_store(userid, intent_id, data, data_description):
    data_update = "INSERT INTO data_store (userid, intent_id, data, data_description) VALUES (%s, %s, %s, %s)"
    lval2 = (userid, intent_id, data, data_description)
    cursor.execute(data_update, lval2)
    connection.commit()

def update_data_store(userid, intent_id, data, data_description):
    data_update = """
    UPDATE data_store 
    SET data = %s, data_description = %s
    WHERE userid = %s AND intent_id = %s
    """
    lval2 = (data, data_description, userid, intent_id)
    cursor.execute(data_update, lval2)
    connection.commit()

def upsert_data_store(userid, intent_id, data, data_description):
    data_update = """
    INSERT INTO data_store (userid, intent_id, data, data_description)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    data = VALUES(data), 
    data_description = VALUES(data_description)
    """
    values = (userid, intent_id, data, data_description)
    cursor.execute(data_update, values)
    connection.commit()

def delete_data_store(userid, intent_id):
    delete_query = """
        DELETE FROM data_store
        WHERE userid = %s AND intent_id = %s
        """
    values = (userid, intent_id)
    cursor.execute(delete_query, values)
    connection.commit()
