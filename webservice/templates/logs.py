import logging.config

LOGGING_CONFIG = {
    'version': 1,
    "disable_existing_loggers": True,

    'loggers': {
        'console': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },

        'mail': {
            'level': 'DEBUG',
            'handlers': ['mail'],
        },

        "uvicorn": {"handlers": ["console"], "level": "INFO"},
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'info',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'mail': {
            'level': 'ERROR',
            'formatter': 'error',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': 'localhost',
            'fromaddr': 'monitoring@domain.com',
            'toaddrs': ['dev@domain.com', 'qa@domain.com'],
            'subject': 'Critical error with application name'
        }
    },

    'formatters': {
        'info': {
            'format': '%(asctime)s | %(levelname)s | %(name)s (%(module)s) | %(lineno)s | %(message)s',
        },
        'error': {
            'format': '%(asctime)s | %(levelname)s | %(name)s  (%(module)s) | %(lineno)s | %(message)s',
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)

# Logs Initialization
console = logging.getLogger('console')
mail = logging.getLogger('mail')
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)