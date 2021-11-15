import logging
import os
from logging.handlers import RotatingFileHandler

import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dialogflow_intent_functions import detect_intent_texts

logger = logging.getLogger('tg_support_bot')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Приветствую, {user.mention_markdown_v2()}\!',
        reply_markup=telegram.ForceReply(selective=True),
    )


def handle_error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def handle_tg_messages(update, context):
    text = detect_intent_texts(
        os.getenv("PROJECT_ID"),
        f'tg-{update.effective_user.id}',
        update.message.text)
    update.message.reply_text(text.query_result.fulfillment_text)


def main():
    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger.setLevel(logging.DEBUG)
    chat_id = os.getenv('CHAT_ID')
    bot_token = os.getenv('BOT_TOKEN')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_error_handler(handle_error)
    logger.addHandler(RotatingFileHandler("app.log", maxBytes=200, backupCount=2))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_tg_messages))
    logger.addHandler(TelegramLogsHandler(telegram.Bot(token=bot_token), chat_id))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
