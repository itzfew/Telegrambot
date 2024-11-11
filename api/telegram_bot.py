import os
import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext import Dispatcher
from flask import Flask, request

# Initialize Flask application
app = Flask(__name__)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your bot's token (store this in environment variables for security)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Vercel will set this automatically

# Initialize the bot and updater
bot = Bot(TOKEN)
updater = Updater(bot=bot, use_context=True)
dp = updater.dispatcher

# Handle the '/start' command
def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f"Hello, {user.first_name}! Welcome to the bot.\n\nHere are some options:")

# Handle button presses
def button(update, context):
    query = update.callback_query
    query.answer()  # Acknowledge the callback
    if query.data == "info":
        query.edit_message_text(text="Here is some information about our services...")
    elif query.data == "contact":
        query.edit_message_text(text="You can contact us at: contact@example.com")
    elif query.data == "help":
        query.edit_message_text(text="For assistance, visit: https://help.example.com")

# Route to handle the incoming webhook from Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return 'ok', 200

# Set webhook
def set_webhook():
    webhook_url = f'{WEBHOOK_URL}/{TOKEN}'
    bot.setWebhook(webhook_url)
    print(f"Webhook set to {webhook_url}")

# Main entry point
if __name__ == '__main__':
    set_webhook()  # Set the webhook when the app starts
    app.run(debug=True, host='0.0.0.0', port=5000)
