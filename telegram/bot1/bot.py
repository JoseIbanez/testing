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

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ACELINKHOST = os.environ.get("ACELINKHOST","http://localhost:8008")
ACELINKTOKEN = os.environ.get("ACELINKTOKEN","MAGIC")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


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
        path = f"{ACELINKHOST}/hls/{port}/"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f"Bearer {ACELINKTOKEN}"}
        data = {
            'ace_id': ace_id,
            'description': ''
        }
        result = requests.put(path,headers=headers,json=data)


    except (HTTPError, ConnectionError) as e:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{e}")
        return

    if result.status_code > 299:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{result.status_code} {result.text}")
        return

    await context.bot.send_message(chat_id, text=json.dumps(result.json(),indent=2))

    await context.bot.send_message(chat_id, text="I'm a super bot, please talk to me!")


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    cmd = shlex.split(update.message.text, posix=False)

    if len(cmd) < 2:
        await context.bot.send_message(chat_id, text="wrong cmd, try /check <port>")
        return

    port=cmd[1]
    user=update.message.from_user.first_name

    await context.bot.send_message(chat_id, text=f"{user}, wait a second for docker Port:{port}")

    try:
        
        path = f"{ACELINKHOST}/hls/{port}/"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f"Bearer {ACELINKTOKEN}"}
        result = requests.get(path,headers=headers)


    except (HTTPError, ConnectionError) as e:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{e}")
        return

    if result.status_code > 299:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{result.status_code} {result.text}")
        return

    await context.bot.send_message(chat_id, text=json.dumps(result.json(),indent=2))

    await context.bot.send_message(chat_id, text="I'm a super bot, please talk to me!")



async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    cmd = shlex.split(update.message.text, posix=False)

    if len(cmd) < 2:
        await context.bot.send_message(chat_id, text="wrong cmd, try /kill <port>")
        return

    port=cmd[1]
    user=update.message.from_user.first_name

    await context.bot.send_message(chat_id, text=f"{user}, wait a second for docker Port:{port}")

    try:
        
        path = f"{ACELINKHOST}/hls/{port}/"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f"Bearer {ACELINKTOKEN}"}
        result = requests.delete(path,headers=headers)


    except (HTTPError, ConnectionError) as e:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{e}")
        return

    if result.status_code > 299:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{result.status_code} {result.text}")
        return

    await context.bot.send_message(chat_id, text=json.dumps(result.json(),indent=2))

    await context.bot.send_message(chat_id, text="I'm a super bot, please talk to me!")



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    hls_handler = CommandHandler('hls', hls)
    check_handler = CommandHandler('check', check)
    kill_handler = CommandHandler('kill', kill)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(hls_handler)
    application.add_handler(check_handler)
    application.add_handler(kill_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()