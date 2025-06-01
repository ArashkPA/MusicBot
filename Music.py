import sqlite3
conn = sqlite3.connect('songs.db')
 

c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        file_id TEXT,
        text TEXT
    )
''')

conn.commit()
conn.close()

print("دیتابیس ساخته شد و جدول songs آماده است.")
