
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_url_path='/static', static_folder='static')

def initialize_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "password"))
    conn.commit()
    conn.close()

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY, note TEXT)''')
    conn.commit()
    conn.close()

def authenticate(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def create_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def create_note(note):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    conn.close()

def read_notes():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return notes

def update_note(note_id, new_note):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("UPDATE notes SET note = ? WHERE id = ?", (new_note, note_id))
    conn.commit()
    conn.close()

def delete_note(note_id):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            return redirect(url_for('notes'))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html', error=False)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        create_user(username, password)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        note = request.form['note']
        create_note(note)
    notes = read_notes()
    return render_template('notes.html', notes=notes)

@app.route('/update/<int:note_id>', methods=['GET', 'POST'])
def update(note_id):
    if request.method == 'POST':
        new_note = request.form['note']
        update_note(note_id, new_note)
        return redirect(url_for('notes'))
    return render_template('update.html', note_id=note_id)

@app.route('/delete/<int:note_id>')
def delete(note_id):
    delete_note(note_id)
    return redirect(url_for('notes'))

if __name__ == "__main__":
    initialize_database()  
    app.run(debug=True)
