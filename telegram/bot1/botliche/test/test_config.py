import logging
import unittest
import logging

from botliche.common import configure_loger
from botliche.config import Config

logger = logging.getLogger(__name__)

configure_loger()

class TestConfig(unittest.TestCase):

    def test_config(self):

        config = Config()
        config.load()

        logger.info("config: %s",config.config)

        self.assertIsNotNone(config.config)



if __name__ == '__main__':
    unittest.main()
