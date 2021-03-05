"""Logger methods
"""

import superposer
import logging


def set_up_logger(logger_name="superposer"):
    """Set up logger of the application

    Args:
        logger_name (str): Name of the logger to be used

    Returns:
        logging.logger: Application log.
    """
    frm = "[%(asctime)-15s]  %(message)s"
    logging.basicConfig(
        level=logging.DEBUG, format=frm, datefmt="%a, %d %b %Y %H:%M:%S"
    )

    logging.getLogger().disabled = True

    return logging.getLogger(logger_name)


def log_settings(logger, args):
    """Compose initial message about application settings.

    Args:
        logger (logging.Logger): Application logger
        args (argparse.Namespace): Application arguments.
    """
    logger.info(f"Running {logger.name} pipeline v. {superposer.__version__}")
    logger.info("Settings:")

    for k, v in vars(args).items():
        logger.info(f"  {k:25s}{v}")
