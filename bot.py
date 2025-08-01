from telebot import TeleBot, types

TOKEN = '7937933589:AAH5GPd6I0luGDUjLum1XYUFlZB9FDl5-KU'  # Bot token
ADMIN_ID = 7781534875         # O‘zingning Telegram ID’ingni yoz
bot = TeleBot(TOKEN)

# Baza uchun oddiy dictlar
kino_db = {}
reklama_kanali = ""
parol = "fergo211"

# Admin panel tugmalari
def admin_menu():
    btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add("🆕 New post", "➕ Add Kino")
    btn.add("📊 Statistika", "📣 SetChannel")
    btn.add("❌ Delete Kino")
    return btn

# Global vaqtinchalik saqlovchi
user_state = {}

# /start
@bot.message_handler(commands=['start'])
def start(msg):
    if msg.chat.id == ADMIN_ID:
        bot.send_message(msg.chat.id, "Parolni kiriting:")
        user_state[msg.chat.id] = "parol"
    else:
        bot.send_message(msg.chat.id, "Salom, kod yuboring:")
        user_state[msg.chat.id] = "user_kino"

# Admin parolini tekshir
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "parol")
def tekshir_parol(msg):
    if msg.text == parol:
        bot.send_message(msg.chat.id, "Xush kelibsiz Admin!", reply_markup=admin_menu())
        user_state[msg.chat.id] = "admin_menu"
    else:
        bot.send_message(msg.chat.id, "Noto‘g‘ri parol!")

# Admin menyudan tanlov
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "admin_menu")
def admin_menyudan(msg):
    if msg.text == "➕ Add Kino":
        bot.send_message(msg.chat.id, "Kino kodi kiriting:")
        user_state[msg.chat.id] = "add_kod"
    elif msg.text == "📣 SetChannel":
        bot.send_message(msg.chat.id, "Reklama kanal userini yuboring (masalan: @kanalim):")
        user_state[msg.chat.id] = "set_channel"
    elif msg.text == "❌ Delete Kino":
        bot.send_message(msg.chat.id, "O‘chirish uchun kodni yuboring:")
        user_state[msg.chat.id] = "delete_kino"
    elif msg.text == "📊 Statistika":
        bot.send_message(msg.chat.id, f"Jami kinolar soni: {len(kino_db)}")
    elif msg.text == "🆕 New post":
        bot.send_message(msg.chat.id, "Kanalga yuboriladigan xabarni yozing:")
        user_state[msg.chat.id] = "new_post"

# Add Kino – Kod
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "add_kod")
def add_kod(msg):
    user_state[msg.chat.id] = {"state": "add_tavsif", "kod": msg.text}
    bot.send_message(msg.chat.id, "Kino tavsifini yozing:")

# Add Kino – Tavsif
@bot.message_handler(func=lambda m: isinstance(user_state.get(m.chat.id), dict) and user_state[m.chat.id]["state"] == "add_tavsif")
def add_tavsif(msg):
    kod = user_state[msg.chat.id]["kod"]
    kino_db[kod] = msg.text
    user_state[msg.chat.id] = "admin_menu"
    bot.send_message(msg.chat.id, "Kino muvaffaqiyatli qo‘shildi ✅", reply_markup=admin_menu())

# Reklama kanalini o‘rnatish
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "set_channel")
def set_channel(msg):
    global reklama_kanali
    reklama_kanali = msg.text
    user_state[msg.chat.id] = "admin_menu"
    bot.send_message(msg.chat.id, f"Reklama kanali o‘rnatildi: {reklama_kanali}", reply_markup=admin_menu())

# Kino o‘chirish
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "delete_kino")
def delete_kino(msg):
    if msg.text in kino_db:
        kino_db.pop(msg.text)
        bot.send_message(msg.chat.id, "Kino o‘chirildi ❌")
    else:
        bot.send_message(msg.chat.id, "Bunday kod topilmadi.")
    user_state[msg.chat.id] = "admin_menu"

# Kanalga post yuborish
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "new_post")
def new_post(msg):
    if reklama_kanali:
        try:
            bot.send_message(reklama_kanali, msg.text)
            bot.send_message(msg.chat.id, "Xabar kanalga yuborildi!")
        except:
            bot.send_message(msg.chat.id, "Xatolik yuz berdi (kanalga admin emasman balki)")
    else:
        bot.send_message(msg.chat.id, "Avval kanalni sozlang 📣")
    user_state[msg.chat.id] = "admin_menu"

# Obychan foydalanuvchi
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "user_kino")
def foydalanuvchi(msg):
    kod = msg.text
    if kod in kino_db:
        javob = kino_db[kod]
        bot.send_message(msg.chat.id, f"🎬 Kino topildi:\n\n{javob}")
        if reklama_kanali:
            bot.send_message(msg.chat.id, f"Obuna bo‘ling: {reklama_kanali}")
    else:
        bot.send_message(msg.chat.id, "❌ Bunday koddagi kino topilmadi")

bot.infinity_polling()
