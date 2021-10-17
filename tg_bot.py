import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dialogflow_intent_functions import detect_intent_texts

logger = logging.getLogger('tg_support_bot')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, chat_id, bot_token):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = bot_token

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update, bot):
    update.message.reply_text('Здравствуйте!')


def handle_error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def handle_tg_messages(update, chat_id):
    text = detect_intent_texts(
        os.getenv("PROJECT_ID"),
        chat_id,
        update.message.text)
    if text.query_result.intent.is_fallback:
        update.message.reply_text(
            'К сожалению, бот не знает ответа на ваш вопрос.')
    else:
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
    logger.addHandler(TelegramLogsHandler(chat_id, bot_token))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
