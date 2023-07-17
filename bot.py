import logging
import os
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the bot token from the environment variable
TOKEN = os.environ.get('TOKEN')

# Get the authorized user IDs from the environment variable (comma-separated list or list literal)
AUTHORIZED_USERS = os.environ.get('AUTHORIZED_USERS', '').replace('[', '').replace(']', '').split(',')
AUTHORIZED_USERS = [int(user_id) for user_id in AUTHORIZED_USERS if user_id]

# Variable to store the message to be sent
message_to_send = None

# Function to send the message periodically
def send_message_periodically(context: CallbackContext):
    global message_to_send
    if message_to_send:
        for chat_id in context.bot.get_chat_ids():
            try:
                context.bot.send_message(chat_id=chat_id, text=message_to_send, parse_mode=ParseMode.HTML)
            except Exception as e:
                logger.error(f"Error sending message to chat {chat_id}: {e}")

    context.job_queue.run_repeating(send_message_periodically, interval=300, first=0)  # 300 seconds = 5 minutes

# Handler for /start command
# ... (rest of the bot.py remains unchanged)


# Handler for /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I am your Telegram bot. Send me any message, and I'll echo it back to you.")

# Handler for /forwardall command (ask the user to send a message to be sent periodically)
def forward_all(update: Update, context: CallbackContext):
    global message_to_send
    if update.effective_user.id in AUTHORIZED_USERS:
        update.message.reply_text("Please send the message that you want to send to all group chats every 5 minutes. Use /stop to stop the periodic sending.")
        message_to_send = update.message.text_html
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Handler for /stop command (stop the periodic sending)
def stop_periodic_sending(update: Update, context: CallbackContext):
    global message_to_send
    if update.effective_user.id in AUTHORIZED_USERS:
        update.message.reply_text("Periodic sending has been stopped.")
        message_to_send = None
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Handler for echoing messages (restricted to authorized users)
def echo(update: Update, context: CallbackContext):
    if update.effective_user.id in AUTHORIZED_USERS:
        update.message.reply_text(update.message.text)
    else:
        update.message.reply_text("You are not authorized to use this bot.")

# Error handler
def error_handler(update: Update, context: CallbackContext):
    logger.error("Error encountered: %s", context.error)
    update.message.reply_text("An error occurred. Please try again later.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("forwardall", forward_all))
    dp.add_handler(CommandHandler("stop", stop_periodic_sending))
    
    # Message handler to echo messages (restricted to authorized users)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo), group=1)

    # Error handler
    dp.add_error_handler(error_handler)

    # Start the Bot and the periodic sending
    updater.start_polling()
    logger.info("Bot started!")
    context = updater.job_queue
    context.run_repeating(send_message_periodically, interval=300, first=0)  # 300 seconds = 5 minutes
    updater.idle()

if __name__ == '__main__':
    main()
