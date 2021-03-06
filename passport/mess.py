"""Utils."""
import datetime
import functools
import itertools
import logging
import logging.handlers
import threading
import time
from typing import Callable


get_current_time = lambda: time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


def set_logger(log_file_path: str, console_level=logging.INFO, file_level=logging.INFO):
    """Initialize logging module.

    :param log_file_path: Path of the log file.
    :type log_file_path: str.
    """
    prefix_format = '[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s'
    date_format = '%Y %b %d %H:%M:%S'
    rotation_time = datetime.time(hour=4)
    logging.basicConfig(
        level=console_level,
        format=prefix_format,
        datefmt=date_format,
    )
    file_hanfler = logging.handlers.TimedRotatingFileHandler(
        filename=log_file_path,
        when='midnight',
        interval=1,
        backupCount=10,
        atTime=rotation_time,
        encoding='utf8'
    )
    file_hanfler.setLevel(file_level)
    formatter = logging.Formatter(fmt=prefix_format, datefmt=date_format)
    file_hanfler.setFormatter(formatter)
    logging.getLogger(name=None).addHandler(file_hanfler)
    logging.info("Start ....")
