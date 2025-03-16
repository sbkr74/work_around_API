import sqlite3

DATABASE = "quiz.db"  # Database file name

def get_db():
    """Connects to the SQLite database and returns the connection."""
    conn = sqlite3.connect(DATABASE)  # Creates "quiz.db" if it does not exist
    # conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

def init_db():
    """Initializes the database by creating tables if they do not exist."""
    db = get_db()  
    cursor = db.cursor()

    # SQL script to create tables
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """
    
    cursor.executescript(schema)  # Execute multiple SQL commands at once
    db.commit()  # Save changes
    db.close()  # Close connection
    print("Database initialized successfully!")

def insert_user(username, password):
    """Inserts a user with a hashed password into the database."""
    # db = sqlite3.connect(DATABASE)
    db = get_db()
    cursor = db.cursor()

    # Hash the password for security
    # hashed_password = hashlib.sha256(password.encode()).hexdigest()
    hashed_password = password

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        db.commit()
        print(f"User '{username}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists.")
    
    db.close()

if __name__ == "__main__":
    init_db()  # Run this to create the database
