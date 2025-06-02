from flask import Flask
import telebot
import sqlite3
import os

TOKEN = '7989861669:AAF_qJhya4tsuOHVcYq2sstR0Ni8RDVz8as'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def save_song(code, file_id, text):
    conn = sqlite3.connect('songs.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS songs (code TEXT, file_id TEXT, text TEXT)')
    c.execute('INSERT INTO songs (code, file_id, text) VALUES (?, ?, ?)', (code, file_id, text))
    conn.commit()
    conn.close()

user_data = {}

@app.route('/')
def home():
    return "ربات DaylightMusicBot فعال است!"

@bot.message_handler(content_types=['audio', 'voice'])
def handle_audio(message):
    file_id = message.audio.file_id if message.audio else message.voice.file_id
    user_data[message.from_user.id] = {'file_id': file_id}
    bot.reply_to(message, "لطفا کد یکتا برای این آهنگ بفرست:")

@bot.message_handler(func=lambda m: m.from_user.id in user_data and 'file_id' in user_data[m.from_user.id] and 'code' not in user_data[m.from_user.id])
def get_code(message):
    code = message.text
    user_data[message.from_user.id]['code'] = code
    bot.reply_to(message, "حالا متن ترجمه رو بفرست:")

@bot.message_handler(func=lambda m: m.from_user.id in user_data and 'code' in user_data[m.from_user.id])
def get_text(message):
    text = message.text
    file_id = user_data[message.from_user.id]['file_id']
    code = user_data[message.from_user.id]['code']
    save_song(code, file_id, text)
    bot.reply_to(message, f"آهنگ ذخیره شد! برای دریافت: https://t.me/{bot.get_me().username}?start={code}")
    del user_data[message.from_user.id]

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
        bot.reply_to(message, "آهنگ پیدا نشد!")

if __name__ == '__main__':
    from threading import Thread
    Thread(target=lambda: bot.polling(none_stop=True)).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)