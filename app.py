import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, content, date FROM notices ORDER BY id DESC')
    notices = cursor.fetchall()
    conn.close()
    return render_template('index.html', notices=notices)

@app.route('/add', methods=['POST'])
def add_notice():
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        conn = sqlite3.connect('notices.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notices (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)