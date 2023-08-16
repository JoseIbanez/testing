from datetime import datetime
import logging
from botliche.common import configure_loger

logger = logging.getLogger(__name__)

class FavoriteChannel:
    name = None
    count = 0
    port = None
    ace_id = None
    cmd = None
    userList = []

    def __repr__(self):

        return f"{self.name} {self.cmd} ({self.ace_id})"

class FavoriteList:

    def __init__(self):
        self.list:list[FavoriteChannel] = []
    
    def load(self):
        pass

    def save(self):
        pass

    def update(self,port,ace_id,description,user):
        fav = FavoriteChannel()
        fav.ace_id = ace_id
        fav.port = port
        fav.name = description
        fav.user = user
