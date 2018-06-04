# -*- coding:utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import logging


def get_logger(name, _level=logging.DEBUG,
               _format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
               _data_format="%y-%m-%d %H:%M:%S"):
    logger = logging.getLogger(name)
    logger.setLevel(_level)
    if not len(logger.handlers):
        formatter = logging.Formatter(fmt=_format,
                                      datefmt=_data_format)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(_level)

        file_handler = logging.FileHandler(filename='log/%s.log' % name)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(_level)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger
