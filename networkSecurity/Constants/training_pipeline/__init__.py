"""
Defining common constants for training pipeline
"""
TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "Network_Security"
ARTIFACT_DIR:str = "artifact"
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"



"""
Data Ingestion realated constants for training pipeline
"""

DATA_INGESTION_COLLECTION_NAME:str = "Network_Data"
DATA_INGESTION_DATABASE_NAME:str = "Network_Security"
DATA_INGESTION_DIRECTORY_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2