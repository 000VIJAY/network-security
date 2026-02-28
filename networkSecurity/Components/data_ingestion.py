import pymongo # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from networkSecurity.Exception.exception import NetworkSecurityException
from networkSecurity.Logging.logger import logger
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.artifact_entity import DataIngestionArtifact
import os
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
## Configuration of the data ingestion component

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
    
    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """Export the MongoDB collection as a pandas DataFrame."""
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client =  pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            records = list(collection.find()) # type: ignore
            df = pd.DataFrame(records) # type: ignore
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"], inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(f"Error occurred while exporting collection as dataframe: {str(e)}", str(e))
    
    def save_feature_store_file(self, df: pd.DataFrame):
        try:
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            df.to_csv(self.data_ingestion_config.feature_store_file_path, index=False)
            logger.info(f"Feature store file saved at: {self.data_ingestion_config.feature_store_file_path}")
        except Exception as e:
            raise NetworkSecurityException(f"Error occurred while saving feature store file: {str(e)}", str(e))
    
    def split_data_as_train_test_save(self, df: pd.DataFrame):
        try:
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ration, random_state=42)  # type: ignore
            
            logger.info(f"Data split into train and test sets with ratio: {self.data_ingestion_config.train_test_split_ration}")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            assert isinstance(train_df, pd.DataFrame), "train_df must be a pandas DataFrame"
            assert isinstance(test_df, pd.DataFrame), "test_df must be a pandas DataFrame"
            
            train_df.to_csv(self.data_ingestion_config.training_file_path,
                            index=False)
            test_df.to_csv(self.data_ingestion_config.testing_file_path, index=False)
            logger.info(f"Training and testing files saved at: {self.data_ingestion_config.training_file_path} and {self.data_ingestion_config.testing_file_path}")
            return train_df, test_df
        except Exception as e:
            raise NetworkSecurityException(f"Error occurred while splitting data into train and test sets: {str(e)}", str(e))
    
    def initiate_data_ingestion(self):
        try:
            # Load the dataset from MongoDB
            df = self.export_collection_as_dataframe()
            logger.info(f"Successfully exported collection as DataFrame with shape: {df.shape}")
            # Save the feature store file
            self.save_feature_store_file(df)
            
            self.split_data_as_train_test_save(df)
            dataingestionartifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
                )
            
            return dataingestionartifact
        
        except Exception as e:
            raise NetworkSecurityException(f"Error occurred during data ingestion: {str(e)}", str(e))