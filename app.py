#!/usr/bin/env python3
"""
Cyber Vault Password Manager
A self-hosted password manager with encryption
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sqlite3
import hashlib
import secrets
import base64
import os

app = Flask(__name__)
CORS(app)

DB_PATH = '/data/vault.db'
SECRET = os.environ.get('SECRET_KEY', secrets.token_hex(32))

def setup_database():
    os.makedirs('/data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        username TEXT,
        encrypted_password TEXT NOT NULL,
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
    h = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return base64.b64encode(h).decode(), base64.b64encode(salt).decode()

@app.route('/')
def home():
    return open('index.html', 'r').read()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cur.fetchone():
        conn.close()
        return jsonify({'error': 'Username already exists'}), 409
    
    pwd_hash, salt = hash_pwd(password)
    cur.execute('INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)',
                (username, pwd_hash, salt))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute('SELECT id, password_hash, salt FROM users WHERE username = ?', (username,))
    user = cur.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    user_id, stored_hash, salt_b64 = user
    salt = base64.b64decode(salt_b64)
    pwd_hash, _ = hash_pwd(password, salt)
    
    if pwd_hash != stored_hash:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = secrets.token_hex(32)
    return jsonify({
        'message': 'Login successful',
        'user_id': user_id,
        'token': token
    }), 200

@app.route('/api/passwords', methods=['GET', 'POST'])
def manage_passwords():
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    if request.method == 'GET':
        cur.execute('''SELECT id, name, username, encrypted_password, url, notes, 
                       created_at, updated_at FROM passwords WHERE user_id = ?
                       ORDER BY updated_at DESC''', (user_id,))
        
        results = []
        for row in cur.fetchall():
            results.append({
                'id': row[0], 'name': row[1], 'username': row[2],
                'encrypted_password': row[3], 'url': row[4], 'notes': row[5],
                'created_at': row[6], 'updated_at': row[7]
            })
        
        conn.close()
        return jsonify(results), 200
    
    else:  # POST
        data = request.json
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
def handle_password(pwd_id):
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    if request.method == 'GET':
        cur.execute('''SELECT id, name, username, encrypted_password, url, notes,
                       created_at, updated_at FROM passwords 
                       WHERE id = ? AND user_id = ?''', (pwd_id, user_id))
        
        row = cur.fetchone()
        if not row:
            conn.close()
            return jsonify({'error': 'Password not found'}), 404
        
        result = {
            'id': row[0], 'name': row[1], 'username': row[2],
            'encrypted_password': row[3], 'url': row[4], 'notes': row[5],
            'created_at': row[6], 'updated_at': row[7]
        }
        conn.close()
        return jsonify(result), 200
    
    elif request.method == 'PUT':
        data = request.json
        cur.execute('''UPDATE passwords SET name = ?, username = ?, 
                       encrypted_password = ?, url = ?, notes = ?, 
                       updated_at = CURRENT_TIMESTAMP
                       WHERE id = ? AND user_id = ?''',
                    (data.get('name'), data.get('username'),
                     data.get('encrypted_password'), data.get('url'),
                     data.get('notes'), pwd_id, user_id))
        
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
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        
        if not cur.fetchone():
            conn.close()
            return jsonify({'status': 'unhealthy', 'error': 'Tables not found'}), 500
        
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Cyber Vault...")
    setup_database()
    print("Listening on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
else:
    setup_database()
