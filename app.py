from src.DSproject.logger import logging
from src.DSproject.exception import CustomException
from src.DSproject.components.data_ingestion import DataIngestion
from src.DSproject.components.data_ingestion import DataIngestionConfig
from src.DSproject.components.data_transformation import DataTransformationConfig, DataTransformation

import sys
if __name__ == "__main__":
    logging.info("the execution started")

    try:
        data_ingestion = DataIngestion()
        train_data_path , test_data_path = data_ingestion.initiate_data_ingestion()

        data_transformation = DataTransformation()
        data_transformation.initiate_data_transformation(train_data_path , test_data_path)
    except Exception as e:
        logging.info('custom exception')
        raise CustomException(e,sys)