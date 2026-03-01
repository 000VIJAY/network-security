
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networkSecurity.Exception.exception import NetworkSecurityException
from networkSecurity.Logging.logger import logger
from networkSecurity.Utils.main_utils.utils import save_numpy_array_data # type: ignore
from networkSecurity.entity.config_entity import DataTransformationConfig
from networkSecurity.Constants.training_pipeline import TARGET_COLUMN , DATA_TRANSFORMATION_IMPUTER_PARAMS
from networkSecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact)
from networkSecurity.Utils.main_utils.utils import save_object


class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            logger.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e    
        
    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e
    
    def get_data_transformer_object(self) -> Pipeline:
        """
        It initializes a KNNImputer with the parameters defined in the training_pipeline.py file
        and then creates a Pipeline object with the imputer as a step. The Pipeline object is then returned.
        
        Args:
            cls: DataTransformation
        
        Returns:
            A Pipeline object that contains a KNNImputer.
        """
        
        logger.info(f"Creating data transformer object.")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logger.info(f"Initialized KNNImputer with parameters: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            
            preprocessor:Pipeline = Pipeline(steps=[("imputer", imputer)])
            logger.info(f"Created data transformer pipeline with steps: {preprocessor.steps}")
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logger.info(f"Obtaining validated training and test file path.")
            train_df: pd.DataFrame = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path) 
            test_df: pd.DataFrame = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path) # type: ignore
            
            ## Removing target column from train and test dataframe
            ## training Dataframe
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)
            
            ## testing Dataframe
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)
            
            ## Applying KNN Imputer to handle missing values in input features
            preprocessing:Pipeline = self.get_data_transformer_object()

            transformed_input_train_feature = preprocessing.fit_transform(input_feature_train_df)
            transformed_input_test_feature = preprocessing.transform(input_feature_test_df) 
            
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
            
            ## save numpy array to file
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.preprocessor_object_file_path, preprocessing)
            
            ## saving at the best location from where i can directly use 
            save_object("final_models/preprocessor.pkl", preprocessing)
            logger.info(f"Saving transformed training and testing data to file.")
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocessor_object_file_path=self.data_transformation_config.preprocessor_object_file_path
            )
            
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e        