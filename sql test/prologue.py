import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import threading
import time
from db import *
# --- Logging setup ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Prologue Text ---
PROLOGUE_PART_1 = (
    " LOADING - _When the videos shows up_ \n\n"
    " LOADING - _Press your volume button up for more thrill exp_ \n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4) In the endless void between realms.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)There lies the Abyss—a consuming darkness that devours all.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)Legends speak of its horrors, of warriors who dared to venture within, never to return.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)Yet, amidst the whispers of fear\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)one name emerges, a shadow in the chaos: *Zerath*.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)Once consumed by ambition, Zerath betrayed everything to embrace the darkness.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)But now his path turns against the very shadows he sought.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)For deep within the Abyss, a faint hope calls to him. Not for power, but for love.\n\n"
    "Loading\n\n"
)

PROLOGUE_PART_2 = (
    "[•](https://files.catbox.moe/lupo2r.jpg) Zerath’s heart beats with a single purpose: to conquer the Abyss and revive her—*Aurelia*\n\n"
    "[•](https://files.catbox.moe/lupo2r.jpg) the one who gave him light in his darkness.\n\n"
    "[•](https://files.catbox.moe/lupo2r.jpg) Through the horrors of the void, he stands alone.\n\n"
    "[•](https://files.catbox.moe/lupo2r.jpg) Betrayed by fate, yet unyielding. His journey begins...\n\n"
    "[•](https://files.catbox.moe/lupo2r.jpg) This is the tale of a man who defied destiny.\n\n"
    "[•](https://files.catbox.moe/lupo2r.jpg) A saga of love, loss, and redemption.\n\n"
    "[•](https://files.catbox.moe/1ji0za.mp4) *Abyss Saga : Tale Of Fallen*"
)

# --- Functions ---
def delete_after_delay(context, chat_id, message_id, delay=3):
    """Delete a message after a specified delay."""
    time.sleep(delay)  # Wait for the specified delay
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")



def animated_text(chat_id, context, text, delay=4):
    """Send animated text messages."""
    # Send an initial message
    message = context.bot.send_message(chat_id, ".", parse_mode=ParseMode.MARKDOWN)

    # Animate typing the text
    for sentence in text.split("\n\n"):
        sentence = sentence.strip()
        if not sentence:
            continue
        time.sleep(delay)  # Pause between sentences
        try:
            message.edit_text(sentence, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.warning(f"Failed to edit message: {e}")

    return message  # Return the message object for further use

def enter(update: Update, context: CallbackContext):
    """Handle the /enter command."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Add user to the database if not already present
    add_user_to_database(update.effective_user)

    # Check if the user has already completed the prologue
    started, completed = check_user_progress(user_id)
    if completed:
        context.bot.send_message(
            chat_id,
            "You have already completed the Prologue. Shall we start your journey?",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    # If the user hasn't completed the prologue, update their progress
    update_user_progress(user_id, started=True)

    # Set up an inline keyboard for continuation
    keyboard = [[InlineKeyboardButton("Continue", callback_data="continue_prologue")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the first part of the prologue
    animated_text(chat_id, context, PROLOGUE_PART_1)

    # Add button for continuation
    message = context.bot.send_message(
        chat_id,
        "Do you wish to continue?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN,
    )

    # Schedule deletion of the button message after animation
    threading.Thread(
        target=delete_after_delay,
        args=(context, chat_id, message.message_id, 3),
    ).start()

    # Store the button message ID in context for deletion later
    context.user_data["button_message_id"] = message.message_id


def animated_text2(chat_id, context, text):
# send animated text
    # Send an initial message
    message = context.bot.send_message(chat_id, ".", parse_mode=ParseMode.MARKDOWN)

    # Animate typing the text
    for sentence in text.split("\n\n"):
        time.sleep(4)  # Pause between sentences
        message.edit_text(sentence, parse_mode=ParseMode.MARKDOWN)

    # Call delete_after_delay after the animation

    return message  # Return the message object for further use


def continue_prologue(update: Update, context: CallbackContext):
    """Handle continuation of the prologue."""
    query = update.callback_query
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    # Delete the button message
    button_message_id = context.user_data.get("button_message_id")
    if button_message_id:
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=button_message_id)
        except Exception as e:
            logger.error(f"Failed to delete button message: {e}")

    # Answer the callback query to acknowledge the click
    query.answer()

    # Overwrite the first part with the second part
    animated_text2(chat_id, context, PROLOGUE_PART_2)

    # After completion, update the user's database to reflect completion
    update_user_progress(user_id, completed=True)

    # Send the "Shall we start this journey?" message with a button
    keyboard = [[InlineKeyboardButton("Start Journey", callback_data="start_journey")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id,
        "Shall we start this journey?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN,
    )

def start_journey(update: Update, context: CallbackContext):
    """Handle the 'Start Journey' button click."""
    query = update.callback_query
    chat_id = query.message.chat_id
    user_id = query.from_user.id

    # You can add a function here to start the actual game or adventure
    context.bot.send_message(chat_id, "The journey begins...")

    # You can also update the database to reflect that the user is now in the journey stage
    # For example:
    # update_user_progress(user_id, journey_started=True)


"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import time

# --- Logging setup ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Prologue Text ---
PROLOGUE_PART_1 = (
    " LOADING - _When the videos shows up_ \n\n"
    " LOADING - _Press your volume button up for more thrill exp_ \n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4) In the endless void between realms.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)There lies the Abyss—a consuming darkness that devours all.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)Legends speak of its horrors, of warriors who dared to venture within, never to return.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)Yet, amidst the whispers of fear\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)one name emerges, a shadow in the chaos: *Zerath*.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)Once consumed by ambition, Zerath betrayed everything to embrace the darkness.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)But now his path turns against the very shadows he sought.\n\n"
    "[•](https://files.catbox.moe/vidcv1.mp4)For deep within the Abyss, a faint hope calls to him. Not for power, but for love.\n\n"
    "Loading\n\n"
)

PROLOGUE_PART_2 = (
    "[•](https://files.catbox.moe/lupo2r.jpg)  Zerath’s heart beats with a single purpose: to conquer the Abyss and revive her—*Aurelia*\n\n"
    "[•](https://files.catbox.moe/lupo2r.jpg)  the one who gave him light in his darkness.\n\n"
    "[•](https://files.catbox.moe/lupo2r.jpg)  Through the horrors of the void, he stands alone.\n\n"
    "[•](https://files.catbox.moe/lupo2r.jpg)  Betrayed by fate, yet unyielding. His journey begins...\n\n"
    "[•](https://files.catbox.moe/lupo2r.jpg)  This is the tale of a man who defied destiny.\n\n"
    "[•](https://files.catbox.moe/lupo2r.jpg)  A saga of love, loss, and redemption.\n\n"
    "[•](https://files.catbox.moe/1ji0za.mp4)   *Abyss Saga : Tale Of Fallen*"
)

# --- Functions ---
def delete_after_delay(context, chat_id, message_id, delay=3):
    time.sleep(delay)  # Wait for the specified delay
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")

def animated_text(chat_id, context, text):
    # Send an initial message
    message = context.bot.send_message(chat_id, ".", parse_mode=ParseMode.MARKDOWN)

    # Animate typing the text
    for sentence in text.split("\n\n"):
        time.sleep(4)  # Pause between sentences
        message.edit_text(sentence, parse_mode=ParseMode.MARKDOWN)

    # Call delete_after_delay after the animation
    delete_after_delay(context, chat_id, message.message_id)

    return message  # Return the message object for further use

def animated_text2(chat_id, context, text):
# send animated text
    # Send an initial message
    message = context.bot.send_message(chat_id, ".", parse_mode=ParseMode.MARKDOWN)

    # Animate typing the text
    for sentence in text.split("\n\n"):
        time.sleep(4)  # Pause between sentences
        message.edit_text(sentence, parse_mode=ParseMode.MARKDOWN)

    # Call delete_after_delay after the animation

    return message  # Return the message object for further use


def enter(update: Update, context: CallbackContext):
# handle /enter
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Continue", callback_data="continue_prologue")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the first part of the prologue
    animated_text(chat_id, context, PROLOGUE_PART_1)

    # Add button for continuation
    message = context.bot.send_message(
        chat_id,
        "Do you wish to continue?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN,
    )

    # Store the button message ID in context for deletion later
    context.user_data["button_message_id"] = message.message_id



def continue_prologue(update: Update, context: CallbackContext):
#    HANDLE continuation OF PROLOGUE_PART_2
    query = update.callback_query
    chat_id = query.message.chat_id

    # Delete the button message
    button_message_id = context.user_data.get("button_message_id")
    if button_message_id:
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=button_message_id)
        except Exception as e:
            logger.error(f"Failed to delete button message: {e}")

    # Answer the callback query to acknowledge the click
    query.answer()

    # Overwrite the first part with the second part
    animated_text2(chat_id, context, PROLOGUE_PART_2)
"""