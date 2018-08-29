# import traceback
import logging

logger = logging.getLogger(__name__)


class FatalError(Exception):
    def __init__(self, message, tb=None):
        self.message = message
        self.tb = tb

    def log(self, return_with=0):
        logger.error(self.message)

        if self.tb:
            logger.debug(
                'traceback:\n{}'.format(
                    self.tb.strip()
                )
            )

        return 0
