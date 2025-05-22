import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.DSproject.exception import CustomException
from src.DSproject.logger import logging
import os




@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts','preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def get_data_transfromer_object(self):

        try:
            pass
        except Exception as e:
            