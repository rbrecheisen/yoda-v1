import logging

formatter = logging.Formatter(
    '%(asctime)s - %(name)s:%(lineno)s - [%(levelname)s] %(funcName)s() %(message)s')

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
