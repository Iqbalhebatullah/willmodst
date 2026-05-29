import telebot
import requests
import os

# Mengambil token dari pengaturan variabel Heroku agar aman
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '7986964958:AAHAtmFfMc7GNSUC_Z8PuRA2Q0fVYwf8MhA')
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK', 'URL_WEBHOOK_DISCORD_KAMU_DISINI')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Membaca pesan masuk (teks dan foto) dari channel Telegram
@bot.channel_post_handler(content_types=['photo', 'text'])
def forward_to_discord(message):
    # Ambil caption jika ada foto, atau ambil teks biasa
    caption = message.caption if message.caption else message.text or ""

    if message.photo:
        # Mengambil foto resolusi tertinggi (index -1 setara dengan fungsi last)
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        
        # Download gambar dari server Telegram
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_info.file_path}"
        image_response = requests.get(file_url)
        
        # Format pengiriman multipart/form-data (sama seperti modul HTTP Make.com)
        files = {'file': ('image.jpg', image_response.content)}
        data = {'content': caption}
        
        # Eksekusi Webhook Discord
        requests.post(DISCORD_WEBHOOK, data=data, files=files)
        print("Foto HD dan teks berhasil dikirim ke Discord!")
        
    else:
        # Jika hanya teks biasa tanpa foto
        data = {'content': caption}
        requests.post(DISCORD_WEBHOOK, data=data)
        print("Teks berhasil dikirim ke Discord!")

print("Bot Telegram ke Discord menyala 24/7...")
bot.infinity_polling()
