import logging

LOGGER_NAME: str = "AFA_Pipeline_Logger"

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

fh = logging.FileHandler("total.log", mode='w')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)