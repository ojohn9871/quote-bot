import json
import random
import os
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# Load quotes
def load_quotes():
    with open("quotes.json", "r") as f:
        return json.load(f)

def load_used():
    if not os.path.exists("used.json"):
        return []
    with open("used.json", "r") as f:
        return json.load(f)

def save_used(used):
    with open("used.json", "w") as f:
        json.dump(used, f)

def get_quote():
    quotes = load_quotes()
    used = load_used()

    # reset if all used
    if len(used) == len(quotes):
        used = []

    available = [q for q in quotes if q not in used]

    quote = random.choice(available)
    used.append(quote)
    save_used(used)

    return quote

def send_quote():
    quote = get_quote()
    message = f"✨ *Daily Inspiration*\n\n{quote}"
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

# Scheduler
scheduler = BlockingScheduler()

# 4 times daily (adjust if needed)
scheduler.add_job(send_quote, "cron", hour=6, minute=0)
scheduler.add_job(send_quote, "cron", hour=12, minute=0)
scheduler.add_job(send_quote, "cron", hour=18, minute=0)
scheduler.add_job(send_quote, "cron", hour=22, minute=0)

print("Bot is running...")
scheduler.start()
