import logging


def setup_logging(
        level: int | str = logging.INFO,
        *,
        httpx_level: int = logging.WARNING,
        httpcore_level: int = logging.INFO,
        openai_level: int = logging.INFO,
        botocore_level: int = logging.INFO,
        format_string: str | None = None):
    """
    Basic logging setup; this is a greatly abbreviated form of what we use for rich logging
    in the Permanence AI Coder product. Python logging does require *some* setup with use,
    though in simple cases you can just use logging.BasicConfig()
    """

    rootlogger = logging.getLogger()
    rootlogger.setLevel(level)
    handler = logging.StreamHandler()
    format_string = format_string or '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    defaults = {}

    handler.setFormatter(
        logging.Formatter(
            fmt=format_string,
            datefmt='%Y-%m-%dT%H:%M:%S%z',
            defaults=defaults))
    rootlogger.addHandler(handler)

    logging.getLogger('httpx').setLevel(httpx_level)
    logging.getLogger('httpcore').setLevel(httpcore_level)
    logging.getLogger('openai').setLevel(openai_level)
    logging.getLogger('botocore').setLevel(botocore_level)
    logging.getLogger('aiobotocore').setLevel(botocore_level)


setup_logging()
_framework_log = logging.getLogger('permai.util')

# your code should mostly use log.info
log = logging.getLogger('permai')
