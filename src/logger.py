import logging
from logging.config import dictConfig

from src.config import config


def create_logger():
    logger = logging.getLogger('ggscorelogger')
    use_console = config.USE_CONSOLE
    handlers = {}
    if use_console:
        handlers['console'] = {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': 'ext://sys.stdout',
        }
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'console': {
                'format': (
                    '%(levelname)s::%(asctime)s:%(name)s.%(funcName)s\n'
                    '%(message)s\n'
                ),
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': handlers,
        'loggers': {
            'ggscorelogger': {
                'level': 'DEBUG',
                'handlers': (
                    ['console'][not use_console:]
                ),
            },
        },
        'disable_existing_loggers': False,
    })
    return logger
