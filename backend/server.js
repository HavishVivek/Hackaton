const express = require('express');
const mysql = require('mysql');
const bcrypt = require('bcryptjs');
const cors = require('cors');
const app = express();
const port = 3306;

// Middleware
app.use(express.json()); // for parsing application/json
app.use(cors()); // enabling CORS

// MySQL connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'gammer0624', // Your MySQL password
  database: 'login' // Replace with your database name
});

db.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    return;
  }
  console.log('Connected to MySQL database');
});

// User registration endpoint
app.post('/register', async (req, res) => {
  const { username, email, password } = req.body;

  // Check if required fields are provided
  if (!username || !email || !password) {
    console.log('Registration failed: Missing required fields');
    return res.status(400).json({ message: 'Please provide all fields' });
  }

  console.log('Attempting to register user:', username, email);

  try {
    // Hash the password before storing it
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insert new user into the database
    const query = 'INSERT INTO users (username, email, password) VALUES (?, ?, ?)';
    db.query(query, [username, email, hashedPassword], (err, result) => {
      if (err) {
        console.error('Error inserting new user:', err);
        return res.status(500).json({ message: 'Error registering user' });
      }

      // Success message in server logs
      console.log(`New user registered: ${username} (${email})`); // Confirmation in server logs
      res.status(201).json({ message: 'User registered successfully' });
    });
  } catch (err) {
    console.error('Error hashing password:', err);
    res.status(500).json({ message: 'Error registering user' });
  }
});

// User login endpoint
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  // Check if required fields are provided
  if (!username || !password) {
    return res.status(400).json({ message: 'Please provide both username and password' });
  }

  // Check if user exists
  const query = 'SELECT * FROM users WHERE username = ? OR email = ?';
  db.query(query, [username, username], async (err, result) => {
    if (err) {
      console.error('Error checking user:', err);
      return res.status(500).json({ message: 'Error logging in' });
    }

    if (result.length === 0) {
      return res.status(404).json({ message: 'User not found' });
    }

    const user = result[0];

    // Compare passwords
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid credentials' });
    }

    res.status(200).json({ message: 'Login successful' });
  });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});