from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bot import BotDB
from enum import Enum


# проставление индексов и кеширование в БД

class MessageId(Enum):
    GET_NAME = 1
    NONE = 99


class Message:
    def __init__(self):
        self.message = MessageId.NONE

    def changeState(self, msgId):
        self.message = msgId

    def getState(self):
        return self.message


msg = Message()


def start(update: Update, context: CallbackContext) -> None:
    if BotDB.user_exists(update.message.from_user.id):
        username = BotDB.get_name(update.message.from_user.id)
        update.message.reply_text(f"Welcome! {username}")
    else:
        msg.changeState(MessageId.GET_NAME)
        update.message.reply_text("Welcome! Как тебя зовут?")


def name(update: Update, context: CallbackContext) -> None:
    result = BotDB.get_name(update.message.from_user.id)
    if result is None:
        update.message.reply_text(f"Ты еще не назвал свое имя!")
    else:
        update.message.reply_text(f"Я помню, {result}")


def remove_me(update: Update, context: CallbackContext) -> None:
    BotDB.rm_user(update.message.from_user.id)
    update.message.reply_text("Ты успешно удален!")


def get_user_name(update: Update, context: CallbackContext) -> None:
    if msg.getState() == MessageId.GET_NAME:
        value = update.message.text
        BotDB.add_user(update.message.from_user.id, value)
        msg.changeState(MessageId.NONE)
        update.message.reply_text(f"Приятно познакомится, {value}")
