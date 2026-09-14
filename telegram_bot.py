import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

# Get the bot token from Railway Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in Railway Variables")


class Country:
    def __init__(
        self,
        capital: str,
        population: str,
        currency: str,
        region: str,
    ):
        self.capital = capital
        self.population = population
        self.currency = currency
        self.region = region

    def __str__(self):
        return (
            f"🏛 Capital: {self.capital}\n"
            f"👥 Population: {self.population}\n"
            f"🪙 Currency: {self.currency}\n"
            f"📍 Region: {self.region}"
        )


DATA = {
    "cambodia": Country(
        "Phnom Penh",
        "16.9 million",
        "Riel (KHR)",
        "Southeast Asia",
    ),
    "japan": Country(
        "Tokyo",
        "125.1 million",
        "Yen (JPY)",
        "East Asia",
    ),
    "france": Country(
        "Paris",
        "67.7 million",
        "Euro (EUR)",
        "Western Europe",
    ),
}


async def reply_capital(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message or not update.message.text:
        return

    country = update.message.text.strip().lower()
    info = DATA.get(country)

    if info:
        await update.message.reply_text(str(info))
    else:
        await update.message.reply_text(
            f"❌ '{update.message.text}' doesn't look like "
            "a valid country name.\n\n"
            "Try: Cambodia, Japan, or France."
        )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            reply_capital,
        )
    )

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
