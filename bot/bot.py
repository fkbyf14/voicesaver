#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from queue import Queue
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot
from telegram.utils import request
from configurations.bot_config import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger()
chat_voices = dict()


def start(update, context):
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Hello! I\'m bot Saver Voicevich, I\'ll save all '
                                                                 'voice messages from chats, where I\'m added.')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"' % (update, context.error))


def voice_handler(update, context):
    file_id = update.message.voice.file_id
    chat_id = str(update.message.chat_id)
    if not chat_voices.get(chat_id):
        chat_voices[chat_id] = list()
    file = context.bot.get_file(file_id)

    try:
        if not os.path.isdir(chat_id):
            os.mkdir(chat_id)

        file_name = 'voice_message_{}'.format(len(os.listdir(chat_id)))
        file.download(custom_path=os.path.join(chat_id, file_name))
        chat_voices[chat_id].append(file_name)
        logging.debug("chat_voices: {}".format(chat_voices))
    except PermissionError:
        context.bot.sendMessage(chat_id=update.message.chat_id, text="Please, configure permissions for work directory")


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    if webhook_url:
        req = request.Request(1, config.REQUEST_KWARGS['proxy_url'])
        bot = Bot(config.TOKEN, req)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(config.TOKEN, use_context=True, request_kwargs=config.REQUEST_KWARGS)
        bot = updater.bot
        dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))
    dp.add_error_handler(error)

    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
