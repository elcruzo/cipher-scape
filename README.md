# CipherScape

Telegram bot for real-time stock data.

## Setup

1. Clone the repo:
```bash
git clone https://github.com/elcruzo/cipher-scape.git
cd cipher-scape
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get a Telegram bot token from [@BotFather](https://t.me/botfather)

4. Set your token:
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

Or create a `token.txt` file with your token.

5. Run the bot:
```bash
python bot.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/stock AAPL` | Current stock price |
| `/info AAPL` | Company information |
| `/day AAPL` | Day's high/low/volume |
| `/help` | List commands |

You can also just send a stock symbol directly (e.g., `AAPL`).

## Example

```
/stock TSLA

📈 TSLA

Price: $248.50
Change: +$5.20 (+2.14%)
```

## Requirements

- Python 3.8+
- python-telegram-bot
- yfinance

## License

MIT License - see [LICENSE](LICENSE) for details.
