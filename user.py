import mysql.connector
from mysql.connector import Error
from bcrypt import hashpw, gensalt, checkpw
import os

def connect_to_database():
    """
    Establish a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",       # MySQL server host
            port=3306,              # Default MySQL port
            user="root",            # MySQL username
            password="gammer0624",  # Replace with your MySQL root password or use os.getenv("MYSQL_PASSWORD")
            database="login"      # Database name
        )
        if connection.is_connected():
            print("Connected to MySQL.")
            return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def create_users_table(connection):
    """
    Ensure the 'users' table exists in the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        connection.commit()
        print("Table 'users' is ready.")
    except Error as e:
        print(f"Error creating table: {e}")

def hash_password(password):
    """
    Hash the password using bcrypt.
    """
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def register_user(connection, username, email, password):
    """
    Register a new user in the database.
    """
    try:
        cursor = connection.cursor()

        # Check if the user already exists
        query = "SELECT * FROM users WHERE username = %s OR email = %s"
        cursor.execute(query, (username, email))
        if cursor.fetchone():
            print("User already exists.")
            return False

        # Hash the password
        hashed_password = hash_password(password)

        # Insert the new user
        insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, email, hashed_password))
        connection.commit()
        print(f"User '{username}' registered successfully.")
        return True
    except Error as e:
        print(f"Error registering user: {e}")
        return False

def login_user(connection, username, password):
    """
    Authenticate the user.
    """
    try:
        cursor = connection.cursor()

        # Fetch user by username
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            print(f"Login successful for user: {username}")
            return True
        else:
            print("Invalid username or password.")
            return False
    except Error as e:
        print(f"Error during login: {e}")
        return False

def main():
    """
    Main function to test the user registration and login system.
    """
    connection = connect_to_database()
    if not connection:
        return

    # Ensure the users table exists
    create_users_table(connection)

    while True:
        print("\nChoose an option:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            register_user(connection, username, email, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_user(connection, username, password)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the database connection
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed.")

if __name__ == "__main__":
    main()