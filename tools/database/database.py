from contextlib import closing
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, url_for, g
from flask_login import logout_user #pip install flask-login

def get_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def init():
    with closing(get_connection()) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, profile_picture TEXT)')
        conn.execute('CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, target TEXT, results TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))')
        conn.commit()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'users.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def get_user_flask(id):
    with closing(get_connection()) as con:
        with closing(con.cursor()) as cur:
            user = cur.execute('SELECT * FROM users WHERE id = ?',(id,)).fetchone()
            return user if user else None

def get_user(name):
    with closing(get_connection()) as con:
        with closing(con.cursor()) as cur:
            user = cur.execute('SELECT * FROM users WHERE name = ?',(name,)).fetchone()
            return user if user else None
        
def get_results(id):
    with closing(get_connection()) as con:
        with closing(con.cursor()) as cur:
            results = cur.execute('SELECT * FROM results WHERE user_id = ?',(id,)).fetchall()
            return results if results else None

def add_results(id, name, target, results):
    with closing(get_connection()) as conn:
        conn.execute('INSERT INTO results (user_id, name, target, results) VALUES(?,?,?,?)', (id, name, target, results))
        conn.commit()

        flash('Scan results saved successfully.')
        return redirect(url_for('index'))  

    return redirect(url_for('scan'))

def delete_result(id, user_id):
    with closing(get_connection()) as conn:
        conn.execute('DELETE FROM results WHERE id = ? AND user_id = ?', (id, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('results'))  
    return redirect(url_for('results'))

def create_user(name, password, profile_picture):
    with closing(get_connection()) as conn:
        conn.execute('INSERT INTO users (name, password, profile_picture) VALUES (?, ?, ?)', (name, password, profile_picture))
        conn.commit()

def change_password(id, current_password, new_password, confirm_password):
    if new_password != confirm_password:
        flash('New passwords do not match.')
        return redirect(url_for('account'))
    with closing(get_connection()) as conn:
        user_password = conn.execute('SELECT password FROM users WHERE id = ?', (id,)).fetchone()
        if current_password == new_password:
            flash('You are not changing the password, you write the sameone.')
            return redirect(url_for('account'))

        if not user_password or not check_password_hash(user_password['password'], current_password):
            flash('Actual password do not match.')
            return redirect(url_for('account'))       
        
        flash('Your password has been successfully changed.')
        new_password_hash = generate_password_hash(new_password)
        conn.execute('UPDATE users SET password = ? WHERE id = ?', (new_password_hash, id))
        conn.commit()
        conn.close()

def delete_user(id):
    with closing(get_connection()) as conn:
        conn.execute('DELETE FROM users WHERE id = ?', (id,))
        conn.execute('DELETE FROM results WHERE user_id = ?', (id,))
        conn.commit()
        conn.close()
        logout_user()   
        flash('Your account has been deleted.')
        return redirect(url_for('index'))  
    flash('Invalid action.')
    return redirect(url_for('account'))
