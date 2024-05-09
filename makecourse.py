import sqlite3

conn = sqlite3.connect('course_management.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT
            );''')

cur.execute('''CREATE TABLE IF NOT EXISTS log (
                id INTEGER PRIMARY KEY,
                timestamp TIMESTAMP,
                action TEXT,
                table_name TEXT
            );''')
cur.execute('''CREATE TRIGGER IF NOT EXISTS log_course_insert
    AFTER INSERT ON courses
    BEGIN
        INSERT INTO log (timestamp, action, table_name)
        VALUES (datetime('now'), 'INSERT', 'courses');
    END;
''')
cur.execute('''CREATE VIEW IF NOT EXISTS course_videos AS
               SELECT c.id as course_id, c.name as course_name, c.link as course_link,
                      v.id as video_id, v.title as video_title, v.url as video_url
               FROM courses c LEFT JOIN videos v ON c.id = v.course_id;
''')
conn.commit()
conn.close()

