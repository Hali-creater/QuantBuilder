import sqlite3
import hashlib

def init_db():
    """Initializes the database and creates the users table if it doesn't exist."""
    conn = sqlite3.connect('trading_platform.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    """Hashes a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    """Adds a new user to the database."""
    conn = sqlite3.connect('trading_platform.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # This error occurs if the username is already taken.
        conn.close()
        return False

def get_user(username):
    """Retrieves a user from the database by username."""
    conn = sqlite3.connect('trading_platform.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def verify_user(username, password):
    """Verifies a user's credentials."""
    user = get_user(username)
    if user:
        password_hash = user[2] # The password_hash is the 3rd column
        if password_hash == hash_password(password):
            return True
    return False
