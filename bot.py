import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram bot token here
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Handler for /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I am your Telegram bot. Send me any message, and I'll echo it back to you.")

# Handler for echoing messages
def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)

# Error handler
def error_handler(update: Update, context: CallbackContext):
    logger.error("Error encountered: %s", context.error)
    update.message.reply_text("An error occurred. Please try again later.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))

    # Message handler to echo messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Error handler
    dp.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()
    logger.info("Bot started!")
    updater.idle()

if __name__ == '__main__':
    main()
          
