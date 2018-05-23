# -*- coding:utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import logging


class NovaLog(object):
    def __init__(self, name, level=logging.DEBUG):
        path = name + '.log'
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(level)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    log = NovaLog('weixin', logging.DEBUG)
    log.debug('一个debug信息')
    log.info('一个info信息')
    log.warning('一个warning信息')
    log.error('一个error信息')
    log.critical('一个致命critical信息')
