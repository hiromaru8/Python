import logging.config


def set_logger():
    logging.config.fileConfig('data/log_conf.ini')
    logger = logging.getLogger('sample')

    return logger


if __name__ == "__main__":

    logger = set_logger()
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('エラーが発生しました')
    logger.critical('criticalエラーが発生しました')

