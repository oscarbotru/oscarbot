import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'formatters': {
        'default': {
            'format': '%(name)s - %(levelname)s - %(asctime)s - %(funcName)s: %(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },

    },
    'loggers': {
        'oscarbot': {
            'handlers': ['console'],
            'level': logging.DEBUG,
            'propagate': False,
        },
    },

}

logging.config.dictConfig(LOGGING_CONFIG)

log = logging.getLogger('oscarbot')
