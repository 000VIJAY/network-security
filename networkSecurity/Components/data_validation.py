from networkSecurity.Constants.training_pipeline import SCHEMA_FILE_PATH
from networkSecurity.Utils.main_utils.utils import read_yaml_file, write_yaml_file # type: ignore
from networkSecurity.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact
from networkSecurity.entity.config_entity import DataValidationConfig 
from networkSecurity.Exception.exception import NetworkSecurityException
from networkSecurity.Logging.logger import logger
import os, sys
import pandas as pd
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_validation_config:DataValidationConfig, data_ingestion_artifact:DataIngestionArtifact):
        try:
            logger.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH) # type: ignore
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e # type: ignore
    
    @staticmethod
    def read_data(file_path:str):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e # type: ignore
    
    def validate_number_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config['columns']) # type: ignore
            logger.info(f"Required number of columns: {number_of_columns}")
            logger.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e # type: ignore
        
    def validate_numeric_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            numeric_columns = self._schema_config['numerical_columns'] # type: ignore
            logger.info(f"Required numeric columns: {numeric_columns}")
            for column in numeric_columns: # type: ignore
                if column not in dataframe.columns:
                    logger.info(f"Column: {column} is not present in dataframe")
                    return False
                if not pd.api.types.is_numeric_dtype(pd.Series(dataframe[column])): # type: ignore
                    logger.info(f"Column: {column} is not numeric")
                    return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e # type: ignore    
    
    def detect_data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, threshold:float=0.5) -> bool:
        try:
                status = True
                drift_report = {}
                for column in base_df.columns:
                    base_data = base_df[column]
                    current_data = current_df[column]
                    ks_test_result = ks_2samp(base_data, current_data)
                    
                    if float(ks_test_result.pvalue) > threshold: # type: ignore
                        is_found = False
                    else:
                        is_found = True
                        status = False
                    drift_report.update({ # type: ignore
                        column:{
                        "p_value": float(ks_test_result.pvalue),   # type: ignore
                        "drift_status": is_found
                        } 
                    })
                drift_report_file_path = self.data_validation_config.drift_report_file_path
                os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
                write_yaml_file(drift_report_file_path, drift_report)
                logger.info(f"Drift Report: {drift_report}")
                return status
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e # type: ignore
        
    def initialize_data_validation_artifact(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            ## read the train and test file and validate them
            
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            self.validate_number_of_columns(train_df)
            self.validate_number_of_columns(test_df)
            ## validatte number of columns and other validation steps
            status = self.validate_number_of_columns(train_df)
            if not status:
                error_message = f"Train file: {train_file_path} does not have required number of columns"
                logger.error(error_message)
            
            status = self.validate_number_of_columns(test_df)
            if not status:
                error_message = f"Test file: {test_file_path} does not have required number of columns"
                logger.error(error_message)
            
            valid_numeric_columns_train = self.validate_numeric_columns(train_df)
            if not valid_numeric_columns_train:
                error_message = f"Train file: {train_file_path} does not have required numeric columns"
                logger.error(error_message)
            
            validate_numerical_columns_test = self.validate_numeric_columns(test_df)
            if not validate_numerical_columns_test:
                error_message = f"Test file: {test_file_path} does not have required numeric columns"
                logger.error(error_message)    
            
            ## lets check data drift and other validation steps
            
            status = self.detect_data_drift(train_df, test_df)
            
            if not status:
                error_message = f"Data drift detected between train and test file"
                logger.error(error_message)     
                   
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True) 
            
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False)   
           
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logger.info(f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e # type: ignore    