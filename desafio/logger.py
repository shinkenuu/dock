import logging

_logger = None


# flake8: noqa: C901
def get_logger():
    global _logger

    if _logger:
        return _logger

    _logger = logging.getLogger("desafio")

    _logger.setLevel(
        logging.DEBUG
    )  # Change according to environment (DEV / STAGE / PROD)
    stream_handler = logging.StreamHandler()

    logging_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

    stream_handler.setFormatter(logging.Formatter(logging_format))

    _logger.addHandler(stream_handler)
    _logger.propagate = False

    return _logger
