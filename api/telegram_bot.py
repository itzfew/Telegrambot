import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

# Initialize the Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the Telegram Bot Token from environment variables (set this in Vercel)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # The token for your bot
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Will be set automatically by Vercel

# Create the bot and dispatcher
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Command handler for '/start'
def start(update, context):
    update.message.reply_text(f"Hello, {update.message.from_user.first_name}! Welcome to the bot.")

# Add the '/start' command handler to the dispatcher
dispatcher.add_handler(CommandHandler('start', start))

# Define the webhook endpoint
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return 'ok', 200

# Set the webhook for the Telegram bot
def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
    bot.setWebhook(webhook_url)
    print(f"Webhook set to {webhook_url}")

# Start the Flask app
if __name__ == '__main__':
    set_webhook()  # Set webhook when the app starts
    app.run(debug=True, host='0.0.0.0', port=5000)
