import logging, os, time


def get_logger(loglevel, directory='logs'):
    """ Retrieve logger object.
    :param loglevel: (string) see https://docs.python.org/2/library/logging.html#logging.Logger.critical
    :param directory: (string) local/project folder where you want the logs to end up.

    :return: (Logger) logger
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Setup Loggers (Verbose for illustration purposes)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    level = logging.getLevelName(loglevel.upper())
    logger = logging.getLogger("dtc-breakdown-logger")
    logger.setLevel(level)
    logger.handlers = []  # Delete old handlers

    # Setup logger to console
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Setup logger to file
    filename = directory + '/' + 'dtc-breakdown_' + time.strftime("%Y-%m-%d") + '.log'
    filehandler = logging.FileHandler(filename)
    filehandler.setLevel(level)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return (logger)
