import mysql.connector
from mysql.connector import Error

def check_user_in_database(username):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="gammer0624",  # Replace with your root password
            database="test_db"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                print(f"User found: {result}")
            else:
                print(f"User '{username}' not found.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Test the function
check_user_in_database("gammer0624")