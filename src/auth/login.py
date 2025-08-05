"""
User authentication module for the web application
"""

import hashlib
import jwt
from datetime import datetime, timedelta

def authenticate_user(username, password):
    """
    Authenticate a user with username and password
    
    Args:
        username (str): User's username
        password (str): User's password
        
    Returns:
        dict: Authentication result with token if successful
    """
    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Check against database (simulated)
    if validate_credentials(username, password_hash):
        # Generate JWT token
        token = generate_jwt_token(username)
        return {
            'success': True,
            'token': token,
            'expires': datetime.now() + timedelta(hours=24)
        }
    else:
        return {
            'success': False,
            'error': 'Invalid credentials'
        }

def validate_credentials(username, password_hash):
    """
    Validate user credentials against database
    
    Args:
        username (str): Username to validate
        password_hash (str): Hashed password
        
    Returns:
        bool: True if credentials are valid
    """
    # Simulated database check
    valid_users = {
        'admin': 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f',
        'user1': 'ac9689e2272427085e35b9d3e3e8bed88cb3434828b43b86fc0596cad4c6e270'
    }
    
    return username in valid_users and valid_users[username] == password_hash

def generate_jwt_token(username):
    """
    Generate JWT token for authenticated user
    
    Args:
        username (str): Username to include in token
        
    Returns:
        str: JWT token
    """
    payload = {
        'username': username,
        'exp': datetime.now() + timedelta(hours=24),
        'iat': datetime.now()
    }
    
    # In production, use a secure secret key
    secret_key = "your-secret-key-here"
    
    return jwt.encode(payload, secret_key, algorithm='HS256')
