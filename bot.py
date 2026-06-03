import json
import random
import os
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

if not TOKEN:
    raise ValueError("BOT_TOKEN not found")

bot = Bot(token=TOKEN)

# -------------------
# LOAD QUOTES
# -------------------
def load_quotes():
    with open("quotes.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_used():
    if not os.path.exists("used.json"):
        return []
    with open("used.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_used(used):
    with open("used.json", "w", encoding="utf-8") as f:
        json.dump(used, f)

# -------------------
# QUOTE LOGIC
# -------------------
def get_quote():
    quotes = load_quotes()
    used = load_used()

    if len(used) >= len(quotes):
        used = []

    available = [q for q in quotes if q not in used]

    quote = random.choice(available)

    used.append(quote)
    save_used(used)

    return quote

# -------------------
# SEND MESSAGE (SYNC FIX)
# -------------------
def send_message(text):
    bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="Markdown"
    )

def send_quote():
    try:
        quote = get_quote()
        message = f"✨ *Daily Inspiration*\n\n{quote}"

        send_message(message)

        print("Quote sent successfully")

    except Exception as e:
        print(f"ERROR: {e}")

# -------------------
# SCHEDULER
# -------------------
scheduler = BlockingScheduler()
scheduler.add_job(send_quote, "interval", hours=1)

print("Bot is running...")

# Startup message
try:
    send_message("🚀 Quote Bot is ONLINE and running (1 quote every hour).")
    print("Startup message sent")
except Exception as e:
    print(f"Startup error: {e}")

# First quote immediately
send_quote()

scheduler.start()
