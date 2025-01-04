from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection settings
db_config = {
    "host": "localhost",
    "user": "root",  # Replace with your MySQL username
    "password": "gammer0624",  # Replace with your MySQL password
    "database": "test_db"
}

# Route to serve the login/register HTML file
@app.route("/")
def index():
    return render_template("login.html")  # Ensure your login.html is in the 'templates' folder

# Route to handle login requests
@app.route("/login", methods=["POST"])
def login():
    user_id = request.form["user_id"]
    password = request.form["password"]
    
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (user_id, password))
        user = cursor.fetchone()
        if user:
            return jsonify({"status": "success", "message": "Login successful!"})
        else:
            return jsonify({"status": "failure", "message": "Invalid credentials!"})
    except Error as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Route to handle registration requests
@app.route("/register", methods=["POST"])
def register():
    user_id = request.form["user_id"]
    email = request.form["email"]
    password = request.form["password"]

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, email, password))
        connection.commit()
        return jsonify({"status": "success", "message": "Registration successful!"})
    except Error as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    app.run(debug=True, port=5001)