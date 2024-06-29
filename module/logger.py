import logging
from rich.logging import RichHandler

class PPOCRFilter(logging.Filter):
    def filter(self, record):
        return "ppocr" not in record.getMessage()

class Logger:
    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        return logger