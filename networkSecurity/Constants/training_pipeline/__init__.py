"""
Defining common constants for training pipeline
"""
import os


TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "Network_Security"
ARTIFACT_DIR:str = "artifact"
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
SCHEMA_FILE_PATH:str = os.path.join("data_schema", "schema.yaml")



"""
Data Ingestion realated constants for training pipeline
"""

DATA_INGESTION_COLLECTION_NAME:str = "Network_Data"
DATA_INGESTION_DATABASE_NAME:str = "Network_Security"
DATA_INGESTION_DIRECTORY_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

"""
Data Validation realated constants for training pipeline
"""

DATA_VALIDATION_DIRECTORY_NAME:str = "data_validation"
DATA_VALIDATION_VALIDATED_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"