import json
import logging
import os
from queue import Queue
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Handler, Dispatcher, CallbackContext, TypeHandler


from telegram import Update, Bot, Chat
from telegram.utils import request
from configurations import bot_config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger()
chat_voices = dict()


def start(update: Update, context: CallbackContext):
    context.bot.sendMessage(chat_id=update.message.chat_id, text="Have fun!")
    chat_voices[str(update.message.chat_id)] = list()
    print("chat_id from start:", update.message.chat_id)


def error(update: Update, context: CallbackContext, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def voice_handler(update: Update, context: CallbackContext):
    file_id = update.message.voice.file_id
    chat_id = str(update.message.chat_id)
    file = context.bot.get_file(file_id)

    print("chat_voices", chat_voices)

    if not os.path.isdir(chat_id):
        os.mkdir(chat_id)
    print("downloading....")
    chat_voices[chat_id].append(file_id)
    try:
        file.download(chat_id)
    except PermissionError:
        context.bot.sendMessage(text="Please, configure permissions for folder access")




def setup(webhook_url=None):
    #If webhook_url is not passed, run with long-polling.
    #logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        req = request.Request(1, bot_config.REQUEST_KWARGS['proxy_url'])
        bot = Bot(bot_config.TOKEN, req)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(bot_config.TOKEN, use_context=True, request_kwargs=bot_config.REQUEST_KWARGS)
        bot = updater.bot
        dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))

    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        #bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
