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
from flask import Flask, request
import os

# 🔑 توکن بات (اینجا توکن واقعی رو بذار)
TOKEN = '7989861669:AAF_qJhya4tsuOHVcYq2sstR0Ni8RDVz8as'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 🔸 صفحه اصلی برای تست
@app.route('/')
def home():
    return "Bot is running!"

# 🔸 مسیر Webhook
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

# 🔸 هندل پیام‌ها
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "پیام شما دریافت شد!")

# 🔸 ست کردن وبهوک
WEBHOOK_URL = f'https://your-app-name.arashk.com/{TOKEN}'  # 🔸 اینجا your-app-name رو با آدرس اپ خودت جایگزین کن
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
