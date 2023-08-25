import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    filters, 
    MessageHandler, 
    ApplicationBuilder, 
    ContextTypes, 
    CommandHandler,
    CallbackQueryHandler
)

import config
import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Check that this user already exists in database
        If user is new - start conversation to get him know
    """
    user = update.message.from_user

    print(f"telegram id {update.effective_chat.id}")
    if db.find_user_by_tg_id(update.effective_chat.id) == -1:
        print("User not found")
        keyboard = [
        [
            InlineKeyboardButton("Хлопець", callback_data="0"),
            InlineKeyboardButton("Дівчина", callback_data="1"),
        ],
            [InlineKeyboardButton("Не скажу", callback_data="0")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Привіт друже! Давай знайомитись! Ти {user.first_name}\nПідкажи будь ласка ти дівчина чи хлопець?", reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привіт {user.first_name}! Ось на які теми ми можемо поспілкуватися!")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    #if(db.add_user(update.message.from_user.first_name, query.data, update.effective_chat.id)):
    await query.edit_message_text(text=f"Приємно познайомитися, {update.message.from_user.first_name}: {query.data}")
   # else:
     #  await query.edit_message_text(text=f"Щось пішло не так, бо ми наче знайомі!")

# THIS handler should be added last
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()


    start_handler = CommandHandler('start', start)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(unknown_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)