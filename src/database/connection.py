"""
Database connection and management module
"""

import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = "webapp.db"

def connect_to_database():
    """
    Establish connection to the SQLite database
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    try:
        # Create database file if it doesn't exist
        if not os.path.exists(DATABASE_PATH):
            initialize_database()
        
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row  # Enable column access by name
        
        return connection
        
    except sqlite3.Error as e:
        raise Exception(f"Database connection failed: {e}")

def initialize_database():
    """
    Initialize database with required tables
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    connection.commit()
    connection.close()

@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
    """
    connection = None
    try:
        connection = connect_to_database()
        yield connection
    except Exception as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if connection:
            connection.close()
