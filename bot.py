#!/usr/bin/env python3

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yfinance as yf

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to CipherScape!\n\n"
        "Commands:\n"
        "/stock AAPL - Get stock price\n"
        "/info AAPL - Get company info\n"
        "/help - Show commands"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n\n"
        "/start - Welcome message\n"
        "/stock <symbol> - Current stock price\n"
        "/info <symbol> - Company information\n"
        "/day <symbol> - Day's high/low\n"
        "/help - This message"
    )


async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /stock AAPL")
        return

    symbol = context.args[0].upper()

    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")

        if data.empty:
            await update.message.reply_text(f"No data found for {symbol}")
            return

        price = data["Close"].iloc[-1]
        prev_close = ticker.info.get("previousClose", price)
        change = price - prev_close
        change_pct = (change / prev_close) * 100

        emoji = "📈" if change >= 0 else "📉"
        sign = "+" if change >= 0 else ""

        await update.message.reply_text(
            f"{emoji} {symbol}\n\n"
            f"Price: ${price:.2f}\n"
            f"Change: {sign}${change:.2f} ({sign}{change_pct:.2f}%)"
        )

    except Exception as e:
        logger.error(f"Error fetching {symbol}: {e}")
        await update.message.reply_text(f"Error fetching data for {symbol}")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /info AAPL")
        return

    symbol = context.args[0].upper()

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        name = info.get("longName", symbol)
        sector = info.get("sector", "N/A")
        market_cap = info.get("marketCap", 0)
        pe_ratio = info.get("trailingPE", "N/A")

        if market_cap >= 1e12:
            cap_str = f"${market_cap/1e12:.2f}T"
        elif market_cap >= 1e9:
            cap_str = f"${market_cap/1e9:.2f}B"
        else:
            cap_str = f"${market_cap/1e6:.2f}M"

        await update.message.reply_text(
            f"📊 {name} ({symbol})\n\n"
            f"Sector: {sector}\n"
            f"Market Cap: {cap_str}\n"
            f"P/E Ratio: {pe_ratio}"
        )

    except Exception as e:
        logger.error(f"Error fetching info for {symbol}: {e}")
        await update.message.reply_text(f"Error fetching info for {symbol}")


async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /day AAPL")
        return

    symbol = context.args[0].upper()

    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")

        if data.empty:
            await update.message.reply_text(f"No data found for {symbol}")
            return

        high = data["High"].iloc[-1]
        low = data["Low"].iloc[-1]
        volume = data["Volume"].iloc[-1]

        await update.message.reply_text(
            f"📅 {symbol} Today\n\n"
            f"High: ${high:.2f}\n"
            f"Low: ${low:.2f}\n"
            f"Volume: {volume:,.0f}"
        )

    except Exception as e:
        logger.error(f"Error fetching day data for {symbol}: {e}")
        await update.message.reply_text(f"Error fetching data for {symbol}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.upper()
    if text.isalpha() and 1 <= len(text) <= 5:
        context.args = [text]
        await stock(update, context)
    else:
        await update.message.reply_text("Send a stock symbol or use /help")


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not token:
        token_file = "token.txt"
        if os.path.exists(token_file):
            with open(token_file) as f:
                token = f.read().strip()

    if not token:
        print("Set TELEGRAM_BOT_TOKEN environment variable or create token.txt")
        return

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stock", stock))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("day", day))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
