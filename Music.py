import sqlite3
from flask import Flask
import os

# ساخت دیتابیس و جدول
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

# ایجاد اپ Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot and Database are running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
