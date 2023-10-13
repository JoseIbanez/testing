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

def search(ace_id:str,user:str="vlan717"):

    with open(f"{DATA_PATH}/hls_cmd.log","r",encoding="utf8") as fd:

        for line in reversed(list(fd)):
            if ace_id in line and user in line:
                item = json.loads(line)
                if item.get('ace_id')==ace_id and item.get('user_id')==user:
                    break
        else:
            item = {}

    if item:
        logger.info("ace_id:%s found, port:%s",ace_id,item.get('port'))

    return item


