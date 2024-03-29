#!/usr/bin/env python

import logging
import os
import time
import re
import json
import yaml
import shlex
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

import requests
from requests.exceptions import HTTPError,ConnectionError

from botliche.m3u8 import M3u8List
from botliche.common import configure_loger
from botliche.scrape_fetv import EventTVList
from botliche import fav
from botliche.auto import match_channel

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ACELINKHOST = os.environ.get("ACELINKHOST","http://localhost:8008")
ACELINKTOKEN = os.environ.get("ACELINKTOKEN","MAGIC")
VIP_USERS = [ "vlan717", "Jacobo", "Diego", "Jorge", "ocsalbi", "Ignacio" ]

configure_loger()

aceList = M3u8List()
eventList = EventTVList()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id

    commandList = [
        BotCommand("ftv", "see the tv guide"),
        BotCommand("list", "see the current channels"),
        BotCommand("hls", "start a tx"),
        BotCommand("check", "check a tx"),
        ]

    help = """
Welcome to BotLiche bot!
* Look for next tv events with /ftv
* See current active channels /list
* Search a TV channel just with the name ex: "EuroSport"
See menu for other commands
    """

    await context.bot.setMyCommands(commandList)
    await context.bot.send_message(chat_id, text=help)


async def fetv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id

    eventList.get_events()
    result = match_channel(eventList,aceList)
    for event in result:
        await context.bot.send_message(chat_id, text=event)

    await send_promnt(context,chat_id)


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


async def search_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    filter = update.message.text

    if len(filter) < 3:
        await context.bot.send_message(chat_id, text="search for a longer text")
        return

    result = aceList.search(filter)

    for item in result:
        await context.bot.send_message(chat_id, text=f"{item}")

    await send_promnt(context,chat_id)



async def hls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    user_id=update.message.from_user.username
    user_name=update.message.from_user.first_name
    cmd = shlex.split(update.message.text)

    # parse command
    if len(cmd) < 2:
        await context.bot.send_message(chat_id, text="wrong cmd, try /hls <aceid> [port] [description]")
        return

    ace_id=cmd[1]
    port=cmd[2] if int(len(cmd))>2 else None
    description=cmd[3] if len(cmd)>3 else None

    # exec command
    await context.bot.send_message(chat_id, text=f"{user_name}, wait a second for AceId:{ace_id}")
    try:
        result = exec_hls(ace_id,port,description,user_id,user_name)
        result['check']=f"/{result['port']}"

    except Exception as e:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{e}")
        return

    # show results
    await context.bot.send_message(chat_id, text=yaml.dump(result))
    await context.bot.send_message(chat_id, text="Done")



async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id

    try:        
        path = f"{ACELINKHOST}/hls/"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f"Bearer {ACELINKTOKEN}"}
        result = requests.get(path,headers=headers)


    except (HTTPError, ConnectionError) as e:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{e}")
        return

    if result.status_code > 299:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{result.status_code} {result.text}")
        return

    for item in result.json():
        await context.bot.send_message(chat_id, text=f"/{item.get('port')} {item.get('description')}")
    await context.bot.send_message(chat_id, text="I'm a super bot, please talk to me!")



async def hls_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    user_id=update.message.from_user.username
    user_name=update.message.from_user.first_name
    cmd = shlex.split(update.message.text)
    ace_id = None
    port = None

    command=cmd[0][1:]

    if len(command)==4 and re.match(r"3[0-9]+",command):
        port = int(command)

    elif len(command)>39:
        ace_id = command


    # exec command
    try:

        if port:
            await context.bot.send_message(chat_id, text=f"{user_name}, wait a second for Port:{port}")
            result = exec_check(port,user_id,user_name)
        elif ace_id:
            await context.bot.send_message(chat_id, text=f"{user_name}, wait a second for AceId:{ace_id}")
            result = exec_hls(ace_id, None, None, user_id, user_name) 
            result['check']=f"/{result['port']}"
        else:
            await context.bot.send_message(chat_id, text="Unknown cmd")
            return

    except Exception as e:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{e}")
        return

    # show results
    await context.bot.send_message(chat_id, text=yaml.dump(result))



async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    user_id=update.message.from_user.username
    user_name=update.message.from_user.first_name
    cmd = shlex.split(update.message.text)

    if len(cmd) < 2:
        await context.bot.send_message(chat_id, text="wrong cmd, try /check <port>")
        return

    port=cmd[1]

    await context.bot.send_message(chat_id, text=f"{user_name}, wait a second for docker Port:{port}")
    try:
        result = exec_check(port, user_id, user_name) 

    except Exception as e:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{e}")
        return

    # show results
    await context.bot.send_message(chat_id, text=yaml.dump(result))




async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    user_id=update.message.from_user.username
    user_name=update.message.from_user.first_name
    cmd = shlex.split(update.message.text)

    if len(cmd) < 2:
        await context.bot.send_message(chat_id, text="wrong cmd, try /kill <port>")
        return

    port=cmd[1]

    await context.bot.send_message(chat_id, text=f"{user_name}, wait a second for docker Port:{port}")

    try:
        
        path = f"{ACELINKHOST}/hls/{port}/"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f"Bearer {ACELINKTOKEN}"}
        result = requests.delete(path,headers=headers)
        fav.save("kill", None, port, None, user_id, user_name)


    except (HTTPError, ConnectionError) as e:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{e}")
        return

    if result.status_code > 299:
        await context.bot.send_message(chat_id, text=f"Something was wrong:\n{result.status_code} {result.text}")
        return

    await context.bot.send_message(chat_id, text=json.dumps(result.json(),indent=2))

    await context.bot.send_message(chat_id, text="I'm a super bot, please talk to me!")


async def reload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    user_id=update.message.from_user.username
    user_name=update.message.from_user.first_name
    cmd = shlex.split(update.message.text)

    aceList.load()

    await send_promnt(context,chat_id)





async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def send_promnt(context,chat_id):
    await context.bot.send_message(chat_id, text="I'm a super bot, please talk to me!")




####

def exec_hls(ace_id,port,description,user_id,user_name):
    """
    To start new transmision
    """

    if description is None:
        description = aceList.get_by_id(ace_id)

    if port is None:
        fav_entry = fav.search(ace_id)
        port = fav_entry.get("port",3231)

    path = f"{ACELINKHOST}/hls/{port}/"
    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
                'Authorization': f"Bearer {ACELINKTOKEN}"}
    data = {
        'ace_id': ace_id,
        'description': description or ""
    }
    result = requests.put(path,headers=headers,json=data)

    if result.status_code > 299:
        raise HTTPError(f"Status code:{result.status_code}\n{result.text}")

    fav.save("hls", ace_id, port, description, user_id, user_name)

    output = result.json()

    if user_id in VIP_USERS or user_name in VIP_USERS:
        output['web']=f"https://boliche.ovh/{output['port']}"

    return output



def exec_check(port,user_id,user_name):
    """
    To check a port
    """

    path = f"{ACELINKHOST}/hls/{port}/"
    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
                'Authorization': f"Bearer {ACELINKTOKEN}"}
    result = requests.get(path,headers=headers)


    if result.status_code > 299:
        raise HTTPError(f"Status code:{result.status_code}\n{result.text}")

    output = result.json()

    if user_id in VIP_USERS or user_name in VIP_USERS:
        output['web']=f"https://boliche.ovh/{output['port']}"

    return output




def main():
    application = ApplicationBuilder().token(TOKEN).build()

    handler_list = [
        CommandHandler('start', start),
        CommandHandler('search', search),
        CommandHandler('hls', hls),
        CommandHandler('check', check),
        CommandHandler('kill', kill),
        CommandHandler('list', list),
        CommandHandler('ftv', fetv),
        CommandHandler('reload', reload),
        MessageHandler(filters.COMMAND, hls_auto),
        MessageHandler(filters.TEXT & (~filters.COMMAND), search_text)
    ]

    for handler in handler_list:
        application.add_handler(handler)

    aceList.load()


    application.run_polling()


if __name__ == '__main__':
    main()