import telebot
import sqlite3
from flask import Flask, request
import os

API_TOKEN = 'توکن_بات_تو'  # اینجا توکن باتت رو بذار
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

# دیکشنری برای ذخیره موقت اطلاعات هر کاربر
user_data = {}

# تابع برای ذخیره اطلاعات در دیتابیس
def save_song(code, file_id, text):
    conn = sqlite3.connect('songs.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS songs (code TEXT PRIMARY KEY, file_id TEXT, text TEXT)')
    c.execute('INSERT INTO songs (code, file_id, text) VALUES (?, ?, ?)', (code, file_id, text))
    conn.commit()
    conn.close()

# هندل پیام‌های صوتی یا آهنگ
@bot.message_handler(content_types=['audio', 'voice'])
def handle_audio(message):
    file_id = message.audio.file_id if message.audio else message.voice.file_id
    user_data[message.from_user.id] = {'file_id': file_id}
    bot.reply_to(message, "لطفا کد یکتا برای آهنگ بفرست (مثلا code123):")

# هندل کد
@bot.message_handler(func=lambda m: m.from_user.id in user_data and 'file_id' in user_data[m.from_user.id] and 'code' not in user_data[m.from_user.id])
def get_code(message):
    code = message.text
    user_data[message.from_user.id]['code'] = code
    bot.reply_to(message, "حالا متن ترجمه رو بفرست:")

# هندل متن ترجمه
@bot.message_handler(func=lambda m: m.from_user.id in user_data and 'code' in user_data[m.from_user.id])
def get_text(message):
    text = message.text
    file_id = user_data[message.from_user.id]['file_id']
    code = user_data[message.from_user.id]['code']
    save_song(code, file_id, text)
    link = f"https://t.me/Daylightmusic_bot?start={code}"
    bot.reply_to(message, f"آهنگ و متن ذخیره شد! لینک مخصوص: {link}")
    del user_data[message.from_user.id]

# هندل /start
@bot.message_handler(commands=['start'])
def send_song_text(message):
    try:
        code = message.text.split(' ')[1]
    except IndexError:
        bot.reply_to(message, "کدی ارسال نشده!")
        return
    conn = sqlite3.connect('songs.db')
    c = conn.cursor()
    c.execute('SELECT file_id, text FROM songs WHERE code=?', (code,))
    result = c.fetchone()
    conn.close()
    if result:
        file_id, text = result
        bot.send_audio(message.chat.id, file_id)
        bot.send_message(message.chat.id, text)
    else:
        bot.reply_to(message, "چیزی پیدا نشد!")

# ---- Flask Webhook ----
WEBHOOK_URL = 'https://YOUR-RENDER-APP-URL.onrender.com/'  # اینجا URL سرویس Render رو بذار

@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def index():
    return 'بات آنلاین است!'

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + API_TOKEN)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
