import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler

app = Flask(__name__)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Create the bot instance
bot = Bot(TOKEN)

# Update your dispatcher setup to use the Application class
application = Application.builder().token(TOKEN).build()

# Define the start command handler
async def start(update: Update, context):
    await update.message.reply_text(f"Hello, {update.message.from_user.first_name}! Welcome to the bot.")

# Add the handler to the application
application.add_handler(CommandHandler("start", start))

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    application.process_update(update)
    return 'ok', 200

def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
    bot.setWebhook(webhook_url)
    print(f"Webhook set to {webhook_url}")

if __name__ == '__main__':
    set_webhook()  # Set the webhook when the app starts
    app.run(debug=True, host='0.0.0.0', port=5000)
