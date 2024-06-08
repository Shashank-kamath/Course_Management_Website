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
cur.execute('''
            Create table if not exists videos (id int auto_increment, course_id int, title varchar, URL text)
            ''')
cur.execute('''CREATE TRIGGER IF NOT EXISTS log_course_insert
    AFTER INSERT ON courses
    BEGIN
        INSERT INTO log (timestamp, action, table_name)
        VALUES (datetime('now'), 'INSERT', 'courses');
    END;
''')
cur.execute('''CREATE VIEW course_videos as Select course_id, title from videos where title = 'Java'           
''')
conn.commit()
conn.close()

