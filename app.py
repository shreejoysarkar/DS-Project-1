from src.DSproject.logger import logging
from src.DSproject.exception import CustomException
from src.DSproject.components.data_ingestion import DataIngestion
from src.DSproject.components.data_ingestion import DataIngestionConfig

import sys
if __name__ == "__main__":
    logging.info("the execution started")

    try:
        data_ingestion = DataIngestion()
        data_ingestion.initiate_data_ingestion()
        
    except Exception as e:
        logging.info('custom exception')
        raise CustomException(e,sys)