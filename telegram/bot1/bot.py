#!/usr/bin/env python

import logging
import os
import time
import shlex
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import subprocess


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a super bot, please talk to me!")

async def hls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    cmd = shlex.split(update.message.text, posix=False)

    if len(cmd) < 2:
        await context.bot.send_message(chat_id, text="wrong cmd, try /hls <aceid> [port]")
        return

    ace_id=cmd[1]
    port=cmd[2] if len(cmd)>1 else "3231"
    user=update.message.from_user.first_name

    await context.bot.send_message(chat_id, text=f"{user}, wait a second for AceId:{ace_id}, Port:{port}")

    try:
        result = subprocess.run(["hls", ace_id, port], stderr=subprocess.PIPE, text=True)
    except FileNotFoundError as e:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{e}")
        return

    if result.stderr:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{result.stderr}")
        return

    await context.bot.send_message(chat_id, text="I'm a super bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    hls_handler = CommandHandler('hls', hls)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(hls_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()