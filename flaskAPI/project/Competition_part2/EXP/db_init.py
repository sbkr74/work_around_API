import sqlite3

DATABASE = "flaskAPI/project/Competition_part2/EXP/quiz.db"  # Database file name

def get_db():
    """Connects to the SQLite database and returns the connection."""
    conn = sqlite3.connect(DATABASE)  # Creates "quiz.db" if it does not exist
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

def view_users():
    """Fetch and display all users from the database."""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id, username, password FROM users")
    users = cursor.fetchall()

    db.close()

    print("\nStored Users:")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Password Hash: {user[2]}")

def authenticate_user(username, password):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()  # Fetch the first matching record

    db.close()

    if user:
        print(f"Login successful! Welcome, {username}.")
    else:
        print("Login failed! Invalid username or password.")

if __name__ == "__main__":
    # Initialize database (run this once)
    init_db()

    while True:
        print("\nUser Management Menu:")
        print("1. Register User")
        print("2. View Users")
        print("3. Login")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            uname = input("Enter a username: ")
            pwd = input("Enter a password: ")
            insert_user(uname, pwd)

        elif choice == "2":
            view_users()

        elif choice == "3":
            uname = input("Enter your username: ")
            pwd = input("Enter your password: ")
            authenticate_user(uname, pwd)

        elif choice == "4":
            print("Exiting program.")
            break

        else:
            print("Invalid choice! Please enter a valid option.")