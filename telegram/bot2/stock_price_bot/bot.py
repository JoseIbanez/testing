#!/usr/bin/env python

import logging
import os
import time
import json
import shlex
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests
from requests.exceptions import HTTPError,ConnectionError

from stock_price_bot.common import configure_loger
from stock_price_bot.yfinance_lib import get_simbol_info


TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


configure_loger()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a super bot, please talk to me!")



async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    cmd = shlex.split(update.message.text)

    if len(cmd) < 2:
        await context.bot.send_message(chat_id, text="wrong cmd, try /s <symbol>")
        return

    simbol_id=cmd[1]
    result = get_simbol_info(simbol_id)

    await context.bot.send_message(chat_id, text=f"{result}")

    await send_promnt(context,chat_id)




async def send_promnt(context,chat_id):
    await context.bot.send_message(chat_id, text="I'm a super bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    handler_list = [
        CommandHandler('s', search),
        MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    ]

    for handler in handler_list:
        application.add_handler(handler)



    application.run_polling()