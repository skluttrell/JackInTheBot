import logging.config

LOG_CONFIG = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'default_formatter': {
			'format': '[%(levelname)s: %(asctime)s] - %(message)s'
		}
	},
	'handlers': {
		'stream_handler': {
			'class': 'logging.StreamHandler',
			'formatter': 'default_formatter',
			'level': 'DEBUG'
		},
		'file_handler': {
			'class': 'logging.FileHandler',
			'formatter': 'default_formatter',
			'filename': 'errors.log',
			'level': 'WARNING'
		}
	},
	'loggers': {
		'default_logger': {
			'handlers': ['file_handler'],
			'propagate': True
		}
	}
}

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger('default_logger')
#logger.warning('test log')