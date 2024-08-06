import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/components/data_transformation.py')))
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_ob_file_path = os.path.join('artifacts', "preprocessor.pkl")

class DataTransforamtion:
    def __init__(self):
        self.data_transforamtion_config= DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        this function is responsible for data transformation
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity", 
                "parental_level_of_education", 
                "lunch", 
                "test_preparation_course"
            ]
            # create a pipeline for missing values
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")) ,
                    ("scaler", StandardScaler())
                ]
            )
            cat_pipeline = Pipeline(
                steps =[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]

            )
            logging.info(f"numerical columns: {numerical_columns}")
            logging.info(f"categorical columns:{categorical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns), 
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df= pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("read train and test data")

            logging.info("obtaining preprocessing pbject")

            preprocessing_obj= self.get_data_transformer_object()


            target_column_name= "math_score"
            numerical_columns= ["writing_score", "reading_score"]

            input_feature_train_df = train_df.drop(columns = [target_column_name], axis = 1)
            target_feature_train_df= train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"applying preprocessing object on trainijng dataframe and esting adtaframe."
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Log the shapes of the arrays
            logging.info(f"input_feature_train_arr shape: {input_feature_train_arr.shape}")  # Highlighted
            logging.info(f"target_feature_train_df shape: {target_feature_train_df.shape}")  # Highlighted
            logging.info(f"input_feature_test_arr shape: {input_feature_test_arr.shape}")    # Highlighted
            logging.info(f"target_feature_test_df shape: {target_feature_test_df.shape}")    # Highlighted

            
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"saved preprocessing object")

            save_object(
                file_path=self.data_transforamtion_config.preprocessor_ob_file_path,
                obj= preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transforamtion_config.preprocessor_ob_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)