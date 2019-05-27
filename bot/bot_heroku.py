import json
import logging
import os
from queue import Queue
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Handler, Dispatcher, CallbackContext
from telegram import Update, Bot
from telegram.utils import request
from configurations import bot_config


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.sendMessage(chat_id=update.message.chat_id, text="Have fun!")
    print("chat_id from start:", update.message.chat_id)


def error(update: Update, context: CallbackContext, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


if __name__ == '__main__':
    # Set these variable to the appropriate values
    TOKEN = bot_config.TOKEN
    NAME = 'voicesaver'

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Set up the Updater
    updater = Updater(bot_config.TOKEN, use_context=True, request_kwargs=bot_config.REQUEST_KWARGS)
    bot = updater.bot
    dp = updater.dispatcher
    update_queue = updater.update_queue

    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_error_handler(error)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
