from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import datetime

app = Flask(__name__)

DB_FILE = 'course_management.db'

def execute_query(query, params=()):
    conn = sql.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

def fetch_data(query, params=()):
    conn = sql.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    conn.close()
    return data

@app.route('/')
def home():
    return redirect('courses')

@app.route('/courses')
def courses():
    courses = fetch_data('SELECT * FROM courses;')
    return render_template('courses.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        execute_query('INSERT INTO courses (title, description) VALUES (?, ?);', (title, description))
        execute_query('INSERT INTO log (timestamp, action, table_name) VALUES (?, ?, ?);', (datetime.datetime.now(), 'INSERT', 'courses'))
        return redirect('/courses')
    return render_template('add_course.html')

@app.route('/videos/<int:course_id>')
def videos(course_id):
    videos = fetch_data('SELECT * FROM videos WHERE course_id = ?;', (course_id,))
    return render_template('videos.html', videos=videos, course_id=course_id)

@app.route('/add_videos/<int:course_id>', methods=['GET', 'POST'])
def add_video(course_id):
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        execute_query('INSERT INTO videos (course_id, title, url) VALUES (?, ?, ?);', (course_id, title, url))
        return redirect(f'/videos/{course_id}')
    return render_template('add_videos.html', course_id=course_id)

if __name__ == '__main__':
    app.run(debug=True)
