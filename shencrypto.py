import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Bot Token and Binance API Details
TELEGRAM_API_KEY = '7158116811:AAFGOfj74qFPXpnwBCVYCdFLryTOF5uPk8A'
BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/24hr'

# Function to fetch data from Binance
def get_crypto_data(symbol):
    response = requests.get(BINANCE_API_URL, params={'symbol': symbol + 'USDT'})
    if response.status_code != 200:
        return None
    data = response.json()
    return {
        'name': symbol,
        'price': float(data['lastPrice']),
        'change_24h': float(data['priceChangePercent']),
        'volume': float(data['quoteVolume']),  # 24-hour quote volume in USDT
    }

# Function to format price with appropriate decimal places
def format_price(price):
    if price >= 1:
        return f"{price:,.2f}"  # Standard format for prices >= 1
    else:
        return f"{price:.8f}"  # Use 8 decimal places for smaller prices

async def crypto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = update.message.text[1:].upper()
    data = get_crypto_data(symbol)
    if data:
        emoji = '📈' if data['change_24h'] >= 0 else '📉'
        formatted_price = format_price(data['price'])
        response_message = (
            f"🌟 *{data['name']} Info*\n"
            f"💵 Current Price: ${formatted_price} {emoji}\n"
            f"🔄 24h Change: {data['change_24h']:+.2f}%\n"
            f"📊 24h Volume: ${data['volume']:,.2f}"
        )
    else:
        response_message = "❌ Sorry, that cryptocurrency is not listed on Binance. Please try another one."
    
    await update.message.reply_text(response_message, parse_mode='Markdown')

async def crypto_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        symbol = context.args[0].upper()
        data = get_crypto_data(symbol)
        if data:
            emoji = '📈' if data['change_24h'] >= 0 else '📉'
            formatted_price = format_price(data['price'])
            response_message = (
                f"🌟 *{data['name']} Info*\n"
                f"💵 Current Price: ${formatted_price} {emoji}\n"
                f"🔄 24h Change: {data['change_24h']:+.2f}%\n"
                f"📊 24h Volume: ${data['volume']:,.2f}"
            )
        else:
            response_message = "❌ Sorry, that cryptocurrency is not listed on Binance. Please try another one."
    else:
        response_message = "❗ Please provide a cryptocurrency name after the command. For example: `/crypto btc`"

    await update.message.reply_text(response_message, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🎩 Welcome to *Shen Crypto*! 🌟\n\n"
        "I'm your personal assistant to navigate the vibrant world of cryptocurrencies. 🌐✨\n\n"
        "Whether you are a seasoned trader or a crypto newbie, I provide real-time data and insightful analytics to help you make informed decisions. 📊🚀\n\n"
        "To see what I can do, type `/help` for a list of commands and how to use them. Let's dive into the dynamic and exciting world of cryptocurrency trading together! 💼📈"
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = (
        "🆘 *Help & Commands*\n\n"
        "Here’s how you can interact with me:\n"
        "- `/btc` — Bitcoin info 🪙\n"
        "- `/eth` — Ethereum info 🪙\n"
        "- `/ltc` — Litecoin info 🪙\n"
        "- `/bnb` — Binance Coin info 🪙\n"
        "- `/xrp` — Ripple info 🪙\n"
        "- `/ada` — Cardano info 🪙\n"
        "- `/sol` — Solana info 🪙\n"
        "- `/doge` — Dogecoin info 🪙\n"
        "- `/crypto <name>` — Get info on any listed cryptocurrency (e.g., `/crypto btc`) 🔍\n\n"
        "Simply type any of the above commands to get real-time data on your favorite cryptocurrencies."
    )
    await update.message.reply_text(help_message, parse_mode='Markdown')

def main():
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("crypto", crypto_search))
    crypto_commands = ['btc', 'eth', 'ltc', 'bnb', 'xrp', 'ada', 'sol', 'doge']
    for command in crypto_commands:
        application.add_handler(CommandHandler(command, crypto_command))
    application.run_polling()

if __name__ == '__main__':
    main()
