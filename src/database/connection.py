"""
Database connection and management module
"""

import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = "webapp.db"

def connect_to_database():
    """
    Establish connection to the SQLite database with enhanced features
    
    Returns:
        sqlite3.Connection: Database connection object with optimizations
    """
    try:
        # UPDATED: Added connection validation
        if not DATABASE_PATH:
            raise Exception("Database path not configured")
        
        # Create database file if it doesn't exist
        if not os.path.exists(DATABASE_PATH):
            print(f"Creating new database at: {DATABASE_PATH}")
            initialize_database()
        
        # UPDATED: Enhanced connection with performance settings
        connection = sqlite3.connect(
            DATABASE_PATH,
            timeout=30.0,  # 30 second timeout
            check_same_thread=False  # Allow multi-threading
        )
        
        # Enable column access by name
        connection.row_factory = sqlite3.Row
        
        # UPDATED: Enable foreign key constraints
        connection.execute("PRAGMA foreign_keys = ON")
        
        # UPDATED: Set journal mode for better performance
        connection.execute("PRAGMA journal_mode = WAL")
        
        # UPDATED: Connection validation
        connection.execute("SELECT 1").fetchone()
        
        print(f"Database connection established successfully")
        return connection
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        raise Exception(f"Database connection failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
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
