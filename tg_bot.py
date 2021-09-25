import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dialogflow_intent_functions import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main():
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    project_id = os.getenv('PROJECT_ID')
    session_id = os.getenv('SESSION_ID')
    text = 'I love bacon'
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    detect_intent_texts(project_id, session_id, text)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
