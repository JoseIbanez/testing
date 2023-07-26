#!/usr/bin/env python

import logging
import os
import time
import json
import shlex
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

import requests
from requests.exceptions import HTTPError,ConnectionError

from botliche.m3u8 import M3u8List
from botliche.common import configure_loger
from botliche.scrape_fetv import EventTVList

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ACELINKHOST = os.environ.get("ACELINKHOST","http://localhost:8008")
ACELINKTOKEN = os.environ.get("ACELINKTOKEN","MAGIC")


configure_loger()

aceList = M3u8List()
eventList = EventTVList()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a super bot, please talk to me!")

    commandList = [
        BotCommand("search","search channel id"),
        BotCommand("hls", "start a tx"),
        BotCommand("check", "check tx status"),
        BotCommand("kill", "kill tx")
        ]


    await context.bot.setMyCommands(commandList)

async def fetv(update: Update, context: ContextTypes.DEFAULT_TYPE):

    result = "\n".join(eventList.get_events())
    await context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a super bot, please talk to me!")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    cmd = shlex.split(update.message.text)

    if len(cmd) < 2:
        await context.bot.send_message(chat_id, text="wrong cmd, try /search <filter>")
        return

    filter=cmd[1]
    result = aceList.search(filter)

    for item in result:
        await context.bot.send_message(chat_id, text=f"{item}")

    await send_promnt(context,chat_id)


async def hls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    cmd = shlex.split(update.message.text)

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
    cmd = shlex.split(update.message.text)

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
    await send_promnt(context,chat_id)




async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    cmd = shlex.split(update.message.text)

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


async def send_promnt(context,chat_id):
    await context.bot.send_message(chat_id, text="I'm a super bot, please talk to me!")



def main():
    application = ApplicationBuilder().token(TOKEN).build()

    handler_list = [
        CommandHandler('start', start),
        CommandHandler('search', search),
        CommandHandler('hls', hls),
        CommandHandler('check', check),
        CommandHandler('kill', kill),
        CommandHandler('ftv', fetv),
        MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    ]

    for handler in handler_list:
        application.add_handler(handler)

    aceList.load()


    application.run_polling()


if __name__ == '__main__':
    main()