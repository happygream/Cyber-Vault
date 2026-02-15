#!/usr/bin/env python3
"""
Cyber Vault Password Manager - Secure Edition
Zero-knowledge password manager with proper encryption
"""

from flask import Flask, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import hashlib
import secrets
import base64
import os
import traceback
from functools import wraps

app = Flask(__name__)

# Security configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://"
)

DB_PATH = '/data/vault.db'

def setup_database():
    os.makedirs('/data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        vault_salt TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        username TEXT,
        encrypted_password TEXT NOT NULL,
        iv TEXT NOT NULL,
        url TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    conn.commit()
    conn.close()
    print("Database ready")

def hash_pwd(password, salt=None):
    if not salt:
        salt = secrets.token_bytes(32)
    h = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 250000)
    return base64.b64encode(h).decode(), base64.b64encode(salt).decode()

def require_auth(f):
    """Decorator for protected routes - uses Flask sessions"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated

@app.after_request
def add_security_headers(response):
    """Add security headers"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com"
    return response

@app.route('/')
def home():
    return open('index.html', 'r').read()

@app.route('/api/register', methods=['POST'])
@limiter.limit("3 per hour")
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cur.fetchone():
        conn.close()
        return jsonify({'error': 'Username already exists'}), 409
    
    pwd_hash, salt = hash_pwd(password)
    vault_salt = base64.b64encode(secrets.token_bytes(32)).decode()
    
    cur.execute('INSERT INTO users (username, password_hash, salt, vault_salt) VALUES (?, ?, ?, ?)',
                (username, pwd_hash, salt, vault_salt))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Check if vault_salt column exists, add if missing
        cur.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cur.fetchall()]
        if 'vault_salt' not in columns:
            print("Adding vault_salt column...")
            cur.execute('ALTER TABLE users ADD COLUMN vault_salt TEXT')
            # Update existing users with random vault salts
            cur.execute('SELECT id FROM users WHERE vault_salt IS NULL')
            users = cur.fetchall()
            for user_row in users:
                vault_salt = base64.b64encode(secrets.token_bytes(32)).decode()
                cur.execute('UPDATE users SET vault_salt = ? WHERE id = ?', (vault_salt, user_row[0]))
            conn.commit()
        
        cur.execute('SELECT id, password_hash, salt, vault_salt FROM users WHERE username = ?', (username,))
        user = cur.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        user_id, stored_hash, salt_b64, vault_salt = user
        salt = base64.b64decode(salt_b64)
        pwd_hash, _ = hash_pwd(password, salt)
        
        if pwd_hash != stored_hash:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Set session
        session['user_id'] = user_id
        session.permanent = False
        
        return jsonify({
            'message': 'Login successful',
            'vault_salt': vault_salt
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Server error'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

@app.route('/api/passwords', methods=['GET', 'POST'])
@require_auth
def manage_passwords():
    try:
        user_id = session['user_id']
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Check if iv column exists, add if missing
        cur.execute("PRAGMA table_info(passwords)")
        columns = [row[1] for row in cur.fetchall()]
        if 'iv' not in columns:
            print("Adding iv column to passwords table...")
            cur.execute('ALTER TABLE passwords ADD COLUMN iv TEXT')
            conn.commit()
        
        if request.method == 'GET':
            cur.execute('''SELECT id, name, username, encrypted_password, iv, url, notes, 
                           created_at, updated_at FROM passwords WHERE user_id = ?
                           ORDER BY updated_at DESC''', (user_id,))
            
            results = []
            for row in cur.fetchall():
                results.append({
                    'id': row[0], 'name': row[1], 'username': row[2],
                    'encrypted_password': row[3], 'iv': row[4], 
                    'url': row[5], 'notes': row[6],
                    'created_at': row[7], 'updated_at': row[8]
                })
            
            conn.close()
            return jsonify(results), 200
        
        else:  # POST
            data = request.json
            
            if not data.get('name') or not data.get('encrypted_password') or not data.get('iv'):
                return jsonify({'error': 'Missing required fields'}), 400
            
            cur.execute('''INSERT INTO passwords 
                           (user_id, name, username, encrypted_password, iv, url, notes)
                           VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (user_id, data.get('name'), data.get('username'),
                         data.get('encrypted_password'), data.get('iv'),
                         data.get('url'), data.get('notes')))
            
            pwd_id = cur.lastrowid
            conn.commit()
            conn.close()
            return jsonify({'id': pwd_id, 'message': 'Password created'}), 201
            
    except Exception as e:
        print(f"Password management error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Server error'}), 500
        cur.execute('''INSERT INTO passwords 
                       (user_id, name, username, encrypted_password, url, notes)
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (user_id, data.get('name'), data.get('username'),
                     data.get('encrypted_password'), data.get('url'), data.get('notes')))
        
        pwd_id = cur.lastrowid
        conn.commit()
        conn.close()
        return jsonify({'id': pwd_id, 'message': 'Password created'}), 201

@app.route('/api/passwords/<int:pwd_id>', methods=['GET', 'PUT', 'DELETE'])
@require_auth
def handle_password(pwd_id):
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    if request.method == 'GET':
        cur.execute('''SELECT id, name, username, encrypted_password, iv, url, notes,
                       created_at, updated_at FROM passwords 
                       WHERE id = ? AND user_id = ?''', (pwd_id, user_id))
        
        row = cur.fetchone()
        if not row:
            conn.close()
            return jsonify({'error': 'Password not found'}), 404
        
        result = {
            'id': row[0], 'name': row[1], 'username': row[2],
            'encrypted_password': row[3], 'iv': row[4],
            'url': row[5], 'notes': row[6],
            'created_at': row[7], 'updated_at': row[8]
        }
        conn.close()
        return jsonify(result), 200
    
    elif request.method == 'PUT':
        data = request.json
        cur.execute('''UPDATE passwords SET name = ?, username = ?, 
                       encrypted_password = ?, iv = ?, url = ?, notes = ?, 
                       updated_at = CURRENT_TIMESTAMP
                       WHERE id = ? AND user_id = ?''',
                    (data.get('name'), data.get('username'),
                     data.get('encrypted_password'), data.get('iv'),
                     data.get('url'), data.get('notes'), pwd_id, user_id))
        
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Password not found'}), 404
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Password updated'}), 200
    
    else:  # DELETE
        cur.execute('DELETE FROM passwords WHERE id = ? AND user_id = ?', 
                    (pwd_id, user_id))
        
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Password not found'}), 404
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Password deleted'}), 200

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=5000)
