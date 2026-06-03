import json
import random
import os
import asyncio
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

async def main():
    bot = Bot(token=TOKEN)

    with open("quotes.json", "r", encoding="utf-8") as f:
        quotes = json.load(f)

    quote = random.choice(quotes)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"✨ Daily Inspiration\n\n{quote}"
    )

    print("Quote sent successfully")

if __name__ == "__main__":
    asyncio.run(main())
