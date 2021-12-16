from db import BotDB
import config
import logging
import personal_actions as handler

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)

BotDB = BotDB('sqlite.db')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    updater = Updater(config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handler.start))
    dispatcher.add_handler(CommandHandler("name", handler.name))
    dispatcher.add_handler(CommandHandler("removeMe", handler.remove_me))

    dispatcher.add_handler(MessageHandler(Filters.text, handler.get_user_name))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
