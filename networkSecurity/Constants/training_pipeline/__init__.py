"""
Defining common constants for training pipeline
"""
import os
import numpy as np


TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "Network_Security"
ARTIFACT_DIR:str = "artifact"
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
SCHEMA_FILE_PATH:str = os.path.join("data_schema", "schema.yaml")
PROCESSING_OBJECT_FILE_NAME = "preprocessor.pkl"


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

"""Data Transformation realated constants for training pipeline
"""

DATA_TRANSFORMATION_DIRECTORY_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_PREPROCESSING_OBJECT_DIR:str = "preprocessing_object"

## knn imputer params
DATA_TRANSFORMATION_IMPUTER_PARAMS = {
    "missing_values": np.nan,  # Type: float
    "n_neighbors": 5,          # Type: int
    "weights": "uniform",      # Type: str
    "metric": "nan_euclidean", # Type: str
    "copy": True,              # Type: bool
    "add_indicator": False,    # Type: bool
    "keep_empty_features": False  # Type: bool
}
