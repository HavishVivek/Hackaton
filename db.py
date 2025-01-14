import mysql.connector
from mysql.connector import Error


def test_user_login(username, email, password):
    """
    Test a user login:
    - Check if the user exists in the database using both username and email.
    - If not, insert the user into the database.
    """
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host="localhost",  # MySQL server host
            port=3306,  # Default MySQL port
            user="root",  # MySQL username
            password="gammer0624",  # Replace with your MySQL root password
            database="login",  # Database name
        )

        if connection.is_connected():
            print("Connected to MySQL.")

            # Create a cursor
            cursor = connection.cursor()

            # Ensure the table exists
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """
            )
            print("Table 'users' is ready.")

            # Check if the user already exists using both username and email
            query = "SELECT * FROM users WHERE username = %s AND email = %s AND password = %s"
            cursor.execute(query, (username, email, password))
            user = cursor.fetchone()

            if user:
                print(f"Login successful for user: {username}")
            else:
                # Insert the new user into the database
                insert_query = (
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
                )
                cursor.execute(insert_query, (username, email, password))
                connection.commit()
                print(f"New user '{username}' added to the database.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")


# Simulate a user login
if __name__ == "__main__":
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    test_user_login(username, email, password)

