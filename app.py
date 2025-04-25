from src.DSproject.logger import logging
from src.DSproject.exception import CustomException
import sys
if __name__ == "__main__":
    logging.info("the execution started")

    try:
        a = 1/0

    except Exception as e:
        logging.info('custom exception')
        raise CustomException(e,sys)