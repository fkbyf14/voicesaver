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


logger = logging.getLogger()


def start(update: Update, context: CallbackContext):
    context.bot.sendMessage(chat_id=update.message.chat_id, text="Have fun!")
    print("chat_id from start:", update.message.chat_id)


def error(update: Update, context: CallbackContext, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


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
        update_queue = updater.update_queue

    #last_update = update_queue.get().to_json()

    #print('last up', last_update)
    #chat_1 = last_update['message']['chat']['id']
    #print("chat_1", chat_1)
    #dp.add_handler(MessageHandler(Filters.chat(chat_1) & Filters.voice, voice_handler))
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(MessageHandler([], example_handler))  # Remove this line
    
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup(bot_config.WEBHOOK_URL)
