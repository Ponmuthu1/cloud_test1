from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    message TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

# ---------- Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    subject = request.form['subject']
    message = request.form['message']

    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute("INSERT INTO feedback (name, subject, message) VALUES (?, ?, ?)",
              (name, subject, message))
    conn.commit()
    conn.close()

    return redirect('/view')

@app.route('/view')
def view_feedback():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute("SELECT * FROM feedback")
    rows = c.fetchall()
    conn.close()
    return render_template('view.html', feedbacks=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
