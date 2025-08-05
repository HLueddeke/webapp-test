"""
API route definitions for the web application
"""

from flask import Flask, request, jsonify
from src.auth.login import authenticate_user
from src.database.connection import get_db_connection

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def login_endpoint():
    """
    User login endpoint
    
    Expected JSON payload:
    {
        "username": "string",
        "password": "string"
    }
    
    Returns:
        JSON response with authentication result
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'error': 'Username and password required'
            }), 400
        
        # Authenticate user
        result = authenticate_user(data['username'], data['password'])
        
        if result['success']:
            return jsonify({
                'message': 'Login successful',
                'token': result['token'],
                'expires': result['expires'].isoformat()
            }), 200
        else:
            return jsonify({
                'error': result['error']
            }), 401
            
    except Exception as e:
        return jsonify({
            'error': 'Internal server error'
        }), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Get list of all users (admin only)
    
    Returns:
        JSON array of user objects
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, created_at FROM users")
            users = [dict(row) for row in cursor.fetchall()]
            
        return jsonify(users), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve users'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON response indicating service status
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
