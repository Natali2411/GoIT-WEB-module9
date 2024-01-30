import logging
import sys


logging.basicConfig()
logger = logging.getLogger("mongo")
ch = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)
