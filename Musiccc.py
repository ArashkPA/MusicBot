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

import telebot
import os
from flask import Flask

# توکن بات
TOKEN = '7989861669:AAF_qJhya4tsuOHVcYq2sstR0Ni8RDVz8as'
bot = telebot.TeleBot(TOKEN)

# جواب ساده به هر پیامی
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "پیام شما دریافت شد!")

# راه‌اندازی Flask برای باز کردن پورت (Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    from threading import Thread

    # اجرای بات تلگرام در یک Thread جدا
    def run_bot():
        bot.polling(non_stop=True)

    Thread(target=run_bot).start()

    # اجرای وب‌سرور Flask روی پورت 5000 (یا پورت ENV)
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
