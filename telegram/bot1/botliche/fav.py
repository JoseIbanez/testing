from datetime import datetime,timezone
import os 
import logging
import json

logger = logging.getLogger(__name__)

DATA_PATH = os.environ.get("DATA_PATH", "/home/ibanez/Projects/testing/telegram/bot1/sample-data")


def save(cmd, ace_id,port,description,user_id,user_name):

    item = {
        "cmd": cmd,
        "ace_id": ace_id,
        "port": port,
        "description": description,
        "user_id": user_id,
        "user_name": user_name,
        "date": datetime.now(timezone.utc).isoformat()

    }

    with open(f"{DATA_PATH}/hls_cmd.log","+a",encoding="utf8") as fd:
        json.dump(item,fd)
        fd.write("\n")

    return

def search(ace_id):

    with open(f"{DATA_PATH}/hls_cmd.log","r",encoding="utf8") as fd:
         
        item = None
        for line in (fd.readlines() [-200:]):

            print(line)
            if ace_id in line:
                item = json.loads(line)


    logger.info("ace_id:%s found %s",ace_id,item)

    return item


