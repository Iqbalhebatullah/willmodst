import telebot
import requests
import os
from flask import Flask
from threading import Thread

# Mengambil token dari Environment Variables Render
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '7986964958:AAHAtmFfMc7GNSUC_Z8PuRA2Q0fVYwf8MhA')
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK', 'https://discord.com/api/webhooks/1509838445982519347/3oP1brM2EusJZS811IfZHlAa7ja603pY6-Lu1xvcZ_TUHmjO7ruF13jO29GJaghhTMjW')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# Route mini untuk mengelabui Render agar port terbuka
@app.route('/')
def home():
    return "Server Telegram-Discord Bot Sedang Berjalan!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Logika Forwarder Bot
@bot.channel_post_handler(content_types=['photo', 'text'])
def forward_to_discord(message):
    caption = message.caption if message.caption else message.text or ""

    if message.photo:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_info.file_path}"
        image_response = requests.get(file_url)
        
        files = {'file': ('image.jpg', image_response.content)}
        data = {'content': caption}
        
        requests.post(DISCORD_WEBHOOK, data=data, files=files)
        print("Foto HD dan teks dikirim!")
    else:
        data = {'content': caption}
        requests.post(DISCORD_WEBHOOK, data=data)
        print("Teks dikirim!")

if __name__ == "__main__":
    # Menjalankan Web Server dan Bot secara bersamaan
    server_thread = Thread(target=run_server)
    server_thread.start()
    print("Bot Telegram ke Discord menyala...")
    bot.infinity_polling()
