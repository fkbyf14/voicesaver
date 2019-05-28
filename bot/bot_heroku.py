#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
from configurations.bot_config import config


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


logger = logging.getLogger()
chat_voices = dict()


def start(update: Update, context: CallbackContext):
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Hello! I\'m bot Saver Voicevich, I\'ll save all '
                                                                 'voice messages from chats, where I\'m added.')


def error(update: Update, context: CallbackContext):
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


if __name__ == '__main__':
    TOKEN = config.TOKEN
    NAME = 'voicesaver'
    PORT = os.environ.get('PORT')

    updater = Updater(config.TOKEN, use_context=True, request_kwargs=config.REQUEST_KWARGS)
    bot = updater.bot
    dp = updater.dispatcher
    update_queue = updater.update_queue

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
