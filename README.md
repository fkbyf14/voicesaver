# Voicesaver Bot

A bot which enables to download voice messages from telegram chats to your server.

## Installation and starting:
Clone the repository:

`git clone https://github.com/fkbyf14/voicesaver.git`

Adjust all necessary values in configurations/bot_config.py.
If webhook is not configure, bot run with long-polling: 

`python bot.py`

## Configuration
Bots are unable to scan the whole chat history, can't upload files larger than 20MB. 

Enable `/setjoingroups` for your bot via the BotFather. Telegram bots can't be added to groups
by default. 
Disable the privacy mode via the BotFather. Telegram bots can't read group messages by default.

## Commands
The bot save all voice messages from chats, where he is added.  
`/start` Greeting from the bot
