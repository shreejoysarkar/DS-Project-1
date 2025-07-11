import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
import dagshub
import mlflow
import numpy as np
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)

from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.DSproject.exception import CustomException
from src.DSproject.logger import logging
from src.DSproject.utils import save_object,evaluate_models
 
@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def eval_metrics(self,actual,pred):
        rmse = np.sqrt(mean_squared_error(actual,pred))
        mae = mean_absolute_error(actual,pred)
        r2 = r2_score(actual,pred)
        return rmse, mae, r2

    def initiate_model_trainer(self,train_array, test_array):
        try:
            logging.info('split training and test input data')

            X_train, y_train, X_test, y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )


            models= {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor":XGBRegressor(),
                "CatBoosting Regressor":CatBoostRegressor(verbose=False),
                "AdaBoost Regressor" : AdaBoostRegressor(),
            }

            params = {
                "Decision Tree" :{
                    'criterion':['squared_error','friedman_mse','absolute_error','poisson'],
                    # 'splitter' :['best','random'],
                    #  'max_features' :['sqrt','log2'],

                },
                "Random Forest":{
                    #'criterion':['squared_error','friedman_mse','absolute_error','poisson'],
                    #'max_features':['sqrt','log2'],
                    'n_estimators':[8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':{'squared_error','huber','absolute_error','quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[ 0.6, 0.7, 0.75, 0.8, 0.85,0.9],
                    #'criterion':['squared_error','friedman_mse'],
                    #'max_features':['auto','sqrt','log2'],
                    'n_estimators':[8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators':[8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    "depth":[6,8,10],
                    "learning_rate":[0.01,0.05,.001],
                    'iterations':[30,50,100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    #'loss':['linear','square','exponential'],
                    'n_estimators':[8,16,32,64,128,256]
                }
            }

            model_report : dict = evaluate_models(X_train,y_train,X_test,y_test, models, params)

            # to get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]




            print("this is the best model")
            print(best_model_name)


            model_names = list(params.keys())

            actual_model = ""

            for model in model_names:
                if best_model_name == model:
                    actual_model = actual_model + model

            best_params = params[actual_model]

            dagshub.init(repo_owner='shreejoysarkar', repo_name='DS-Project-1', mlflow=True)

            # mlflow 
            import mlflow

            with mlflow.start_run():
                mlflow.log_param('parameter name', 'value')
                mlflow.log_metric('metric name', 1)
                predicted_qualities = best_model.predict(X_test)

                (rmse, mae, r2) = self.eval_metrics(y_test, predicted_qualities)
 
           



             
        
            if best_model_score<0.6:
                raise CustomException("No Best model found")
        
            logging.info("Best found model on both trainning and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = best_model
                )
            
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            return r2_square


        except Exception as e:
            raise CustomException(e,sys)