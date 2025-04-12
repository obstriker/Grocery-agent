from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime, timedelta
from grocery_list import agent
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Dictionary to track user sessions and their last interaction time
user_sessions = {}
SESSION_TIMEOUT = timedelta(hours=4)


async def conv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_chat.id)
    user_message = update.message.text

    # Check if the session exists and if it has expired
    if user_id in user_sessions:
        last_active = user_sessions[user_id]['last_active']
        if datetime.now() - last_active > SESSION_TIMEOUT:
            # Session has expired; create a new session
            agent.storage.delete_session(user_id)
            user_sessions[user_id] = {'last_active': datetime.now()}
    else:
        # New user session
        user_sessions[user_id] = {'last_active': datetime.now()}

    # Update the last active time
    user_sessions[user_id]['last_active'] = datetime.now()

    # Run the agent with the user's message
    response = agent.run(user_message, user_id=user_id)

    # Send the agent's response back to the user
    await update.message.reply_text(response.content)

async def clear_session(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_chat.id)
    agent.storage.delete_session(user_id)
    if user_id in user_sessions:
        del user_sessions[user_id]
    await update.message.reply_text("Your session has been cleared.")

# Initialize the Telegram bot application
app = ApplicationBuilder().token(getenv("TELEGRAM_KEY")).build()

# Add handlers for messages and commands
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, conv))
app.add_handler(CommandHandler("clear", clear_session))

# Run the bot
app.run_polling()
