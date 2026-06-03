import json
import random
import os
import asyncio
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

if not TOKEN:
    raise ValueError("BOT_TOKEN not found")

bot = Bot(token=TOKEN)

# Load quotes
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

async def send_message_async(message):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=message,
        parse_mode="Markdown"
    )

def send_quote():
    try:
        quote = get_quote()

        message = f"✨ *Daily Inspiration*\n\n{quote}"

        asyncio.run(send_message_async(message))

        print("Quote sent successfully")

    except Exception as e:
        print(f"ERROR: {e}")

# Scheduler
scheduler = BlockingScheduler()

# 4 times daily
scheduler.add_job(send_quote, "cron", hour=6, minute=0)
scheduler.add_job(send_quote, "cron", hour=12, minute=0)
scheduler.add_job(send_quote, "cron", hour=18, minute=0)
scheduler.add_job(send_quote, "cron", hour=22, minute=0)

print("Bot is running...")

# SEND TEST MESSAGE IMMEDIATELY AFTER DEPLOYMENT
try:
    asyncio.run(
        send_message_async(
            "🚀 Quote Bot is ONLINE and connected successfully."
        )
    )
    print("Startup message sent")
except Exception as e:
    print(f"Startup error: {e}")

scheduler.start()
