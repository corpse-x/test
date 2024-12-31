from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

# --- Menu Handler ---
def menu(update: Update, context: CallbackContext):
    """Display the main menu."""
    chat_id = update.effective_chat.id
    menu_text = (
        "Welcome to the RPG Bot Menu!\n"
        "Here you can manage your profile, check your stats, and explore other options.\n"
        "[ • ](https://files.catbox.moe/965fj9.jpg)"
    )

    # Inline buttons for menu options (two per row)
    keyboard = [
        [InlineKeyboardButton("📋 Profile", callback_data="menu_profile"), InlineKeyboardButton("🎒 Inventory", callback_data="menu_inventory")],
        [InlineKeyboardButton("📊 My Stats", callback_data="menu_stats"), InlineKeyboardButton("☠️ Kills & Exp", callback_data="menu_kills_exp")],
        [InlineKeyboardButton("🐾 Pets", callback_data="menu_pets")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Check if this is a new message or an edited message
    if update.message:
        update.message.reply_text(
            text=menu_text,
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )
    elif update.callback_query:
        update.callback_query.edit_message_text(
            text=menu_text,
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )

# --- Callback Handler for Menu Buttons ---
def menu_button_handler(update: Update, context: CallbackContext):
    """Handle menu button clicks and edit the menu message."""
    query = update.callback_query
    query.answer()

    # Define the back button
    back_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_main")]
    ])

    # Content based on button clicked
    if query.data == "menu_profile":
        text = "📋 This is your profile information."
    elif query.data == "menu_inventory":
        text = "🎒[ • ](https://files.catbox.moe/965fj9.jpg) Here is your inventory."
    elif query.data == "menu_stats":
        text = "📊 [ • ](https://files.catbox.moe/965fj9.jpg)These are your stats."
    elif query.data == "menu_kills_exp":
        text = "☠️[ • ](https://files.catbox.moe/965fj9.jpg) Here is your Kills & EXP."
    elif query.data == "menu_pets":
        text = "🐾[ • ](https://files.catbox.moe/965fj9.jpg) These are your pets."
    elif query.data == "menu_main":
        # Return to the main menu
        menu(update, context)
        return
    else:
        text = "Unknown action!"

    # Edit the message with the new content and add a back button
    query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=back_button,
    )

