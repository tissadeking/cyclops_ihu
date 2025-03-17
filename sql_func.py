import mysql.connector, time
from mysql.connector import Error

#create connection to cyclops database
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

connection = create_db_connection("mysql", "root", "password123", "cyclops")
cursor = connection.cursor()

def connect_db():
    #connection = create_db_connection("localhost", "root", "password123", "cyclops")
    connection = create_db_connection("mysql", "root", "password123", "cyclops")
    cursor = connection.cursor()
    return connection, cursor

# Wait for MySQL to be ready
def wait_for_db():
    while True:
        try:
            #connection = mysql.connector.connect(**DB_CONFIG)
            #connection = connect_db()[0]
            connection = create_db_connection("mysql", "root", "password123", "cyclops")
            if connection.is_connected():
                print("✅ Connected to MySQL!")
                #cursor = connection.cursor()
                connection.close()
                break
        except mysql.connector.Error:
            print("⏳ Waiting for MySQL to start...")
            time.sleep(2)  # Wait 2 seconds before retrying

#insert data into users table
def insert_data(email, username, password, userid):
    #connection, cursor = connect_db()
    user_update = "INSERT INTO users (email, username, password, userid) VALUES (%s, %s, %s, %s)"
    lval2 = (email, username, password, userid)
    cursor.execute(user_update, lval2)
    connection.commit()

#check whether username and password are in the users table
def check_data(username, password):
    #cursor = connect_db()[1]
    query = f"""
            SELECT * FROM users 
            WHERE username = %s and password = %s;
    """
    cursor.execute(query, (username, password))
    existing_entry = cursor.fetchone()
    return existing_entry

#check whether email already exists in the users table
def check_email(email):
    #cursor = connect_db()[1]
    query = f"""
            SELECT * FROM users 
            WHERE email = %s;
    """
    cursor.execute(query, (email,))
    existing_entry = cursor.fetchone()
    return existing_entry

#check whether username already exists in the users table
def check_username(username):
    #cursor = connect_db()[1]
    query = f"""
            SELECT * FROM users 
            WHERE username = %s;
    """
    cursor.execute(query, (username,))
    existing_entry = cursor.fetchone()
    return existing_entry

#fetch userid from the users table
def get_userid(username):
    #cursor = connect_db()[1]
    query = f"""
            SELECT userid FROM users 
            WHERE username = %s;
    """
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    return row[0] if row else None

#insert new entry into data_store
def insert_data_store(userid, intent_id, data, data_description):
    #connection, cursor = connect_db()
    data_update = "INSERT INTO data_store (userid, intent_id, data, data_description) VALUES (%s, %s, %s, %s)"
    lval2 = (userid, intent_id, data, data_description)
    cursor.execute(data_update, lval2)
    connection.commit()

#update data_store with new entry
def update_data_store(userid, intent_id, data, data_description):
    #connection, cursor = connect_db()
    data_update = """
    UPDATE data_store 
    SET data = %s, data_description = %s
    WHERE userid = %s AND intent_id = %s
    """
    lval2 = (data, data_description, userid, intent_id)
    cursor.execute(data_update, lval2)
    connection.commit()

#upsert data_store
def upsert_data_store(userid, intent_id, data, data_description):
    #connection, cursor = connect_db()
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

#delete existing entry in data_store
def delete_data_store(userid, intent_id):
    #connection, cursor = connect_db()
    delete_query = """
        DELETE FROM data_store
        WHERE userid = %s AND intent_id = %s
        """
    values = (userid, intent_id)
    cursor.execute(delete_query, values)
    connection.commit()
