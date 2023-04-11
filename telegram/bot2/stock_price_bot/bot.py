#!/usr/bin/env python

import logging
import os
import time
import json
import shlex
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
#from ptbcontrib.ptb_sqlalchemy_jobstore import PTBSQLAlchemyJobStore
from requests.exceptions import HTTPError,ConnectionError

from stock_price_bot.lib.common import configure_loger
from stock_price_bot.lib.yfinance_lib import get_symbol_info
from stock_price_bot.lib.psql_link import Psql

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


configure_loger()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Add alarm job
    """

    chat_id = update.effective_message.chat_id
    user_id = update.message.from_user.id

    try:

        remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(alarm, 60, chat_id=chat_id, user_id=user_id, name=str(chat_id))

        text = "Alarm successfully set!"
        await context.bot.send_message(chat_id, text=text)

    except (IndexError, ValueError):
        await context.bot.send_message(chat_id, text="Usage: /start")



async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Stop alarm job
    """
    chat_id = update.message.chat_id

    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Alarm successfully cancelled!" if job_removed else "You have no active alarm."
    await context.bot.send_message(chat_id, text=text)


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Remove job with given name. Returns whether job was removed.
    """
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    cmd = shlex.split(update.message.text)

    if len(cmd) < 2:
        await context.bot.send_message(chat_id, text="wrong cmd, try /s <symbol>")
        return

    symbol_id=cmd[1].upper()
    result = get_symbol_info(symbol_id)

    await context.bot.send_message(chat_id, text=f"{result}")

    db = Psql()
    db.update_symbol(result)
    db.add_watcher(str(user_id),symbol_id)

    await send_promnt(context,chat_id)


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    cmd = shlex.split(update.message.text)

    if len(cmd) < 2:
        await context.bot.send_message(chat_id, text="wrong cmd, try /d <symbol>")
        return

    symbol_id=cmd[1].upper()

    db = Psql()
    db.del_watcher(str(user_id),symbol_id)
    db.close()

    await send_promnt(context,chat_id)

async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = context.job.user_id
    chat_id = context.job.chat_id

    db = Psql()
    s_list = db.get_symbol_changed(str(user_id))

    for symbol_id in s_list:
        result = get_symbol_info(symbol_id)
        db.update_symbol(result)
        db.done_watcher(str(user_id),symbol_id)
        await context.bot.send_message(chat_id, text=f"{result}")

    db.close()


async def send_promnt(context: ContextTypes.DEFAULT_TYPE,chat_id):
    await context.bot.send_message(chat_id, text="I'm a super bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)



def main():

    configure_loger()

    application = ApplicationBuilder().token(TOKEN).build()

    #DB_URI = "postgresql://bot:bopass@localhost:5432/sp"

    #application.job_queue.scheduler.add_jobstore(
    #    PTBSQLAlchemyJobStore(
    #        application=application,
    #        url=DB_URI,
    #    )
    #)


    handler_list = [
        CommandHandler('s', search),
        CommandHandler('d', delete),
        CommandHandler('start', start),
        CommandHandler('stop', stop),
        MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    ]

    for handler in handler_list:
        application.add_handler(handler)
 
    application.run_polling()




if __name__ == '__main__':
    main()