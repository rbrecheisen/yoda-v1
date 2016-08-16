import logging


formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
