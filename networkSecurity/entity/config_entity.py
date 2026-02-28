from datetime import datetime
import os

from networkSecurity.Constants import training_pipeline

class TrainingPipelineConfig:
    def __init__(self, timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")):
        self.timestamp = timestamp
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)
        

class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.timestamp = training_pipeline_config.timestamp
        self.pipeline_name = training_pipeline_config.pipeline_name
        self.artifact_dir = training_pipeline_config.artifact_dir
        self.data_ingestion_dir = os.path.join(
            self.artifact_dir,
            training_pipeline.DATA_INGESTION_DIRECTORY_NAME)
        
        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME)
        
        self.training_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME)
        
        self.testing_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ration = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        