import logging
from datetime import datetime
from telegram import Update, ParseMode
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    CallbackQueryHandler,
)
from db import *  # Importing the database functions from db.py
from prologue import *
from menu import *
# --- Logging setup ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# --- Bot Configuration ---
TOKEN = "8032359051:AAH0ICsIFbO9F2LECVeYvKk0T3tmkaC_Erc"  # Replace with your bot token
LOG_CHANNEL_ID = "-1002369420179"  # Replace with your log group/channel ID

# --- Logging Function ---
def log_new_user(update: Update, context: CallbackContext):
    """Log new user information to the LOGS channel."""
    user = update.effective_user
    context.bot.send_message(
        chat_id=LOG_CHANNEL_ID,
        text=f"""#NEWUSER
<b>Name:</b> {user.full_name}
<b>Username:</b> @{user.username if user.username else 'N/A'}
<b>ID:</b> {user.id}
<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""",
        parse_mode=ParseMode.HTML,
    )

def animation_text(context: CallbackContext, chat_id: int, text: str):
    """Send animated text messages."""
    messages = text.split("\n")
    for msg in messages:
        context.bot.send_chat_action(chat_id, action="typing")
        context.bot.send_message(chat_id, msg, parse_mode=ParseMode.HTML)

def log_bot_start(context: CallbackContext):
    """Send a bot startup log."""
    bot = context.bot
    chat_id = context.job.context["chat_id"]

    bot.send_message(
        chat_id=chat_id,
        text="Bot started",
        parse_mode=ParseMode.HTML,
    )

# --- Command Handlers ---
def start(update: Update, context: CallbackContext):
    """Handle the /start command."""
    user = update.effective_user
    is_new_user = add_user_to_database(user)  # Add user to the database if not present

    if is_new_user:
        log_new_user(update, context)  # Log only if the user is new

    update.message.reply_text(f"Welcome, {user.first_name}!")


# --- Main Function ---
def main():
    """Start the bot."""
    # Ensure the database file exists and is initialized correctly
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("enter", enter))
    dispatcher.add_handler(CallbackQueryHandler(continue_prologue, pattern="continue_prologue"))
    dispatcher.add_handler(CallbackQueryHandler(start_journey, pattern='^start_journey$'))
# --- MENU ---
    dispatcher.add_handler(CommandHandler("menu", menu))
    dispatcher.add_handler(CallbackQueryHandler(menu_button_handler))
    
    # Log the bot start event
    updater.job_queue.run_once(
        log_bot_start,
        0,
        context={
            "chat_id": LOG_CHANNEL_ID,
        },
    )

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    print("BOT STARTED")
    main()
