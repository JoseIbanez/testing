
import logging
import itertools
import os
import re
from pathlib import Path
import logging
import yaml

logger = logging.getLogger(__name__)

DATA_PATH = os.environ.get("DATA_PATH", "/home/ibanez/Projects/testing/telegram/bot1/sample-data")


class Config:

    def __init__(self):

        self.config = None


    def load(self):

        self.config = yaml.safe_load(Path(DATA_PATH,'config.yml').read_text())


    def get(self,key:str,default=None):

        return self.config.get(key,default)
