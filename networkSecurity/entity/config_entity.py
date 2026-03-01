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
        
class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.timestamp = training_pipeline_config.timestamp
        self.pipeline_name = training_pipeline_config.pipeline_name
        self.artifact_dir = training_pipeline_config.artifact_dir
        self.data_validation_dir = os.path.join(
            self.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIRECTORY_NAME)
        
        self.validated_dir = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALIDATED_DIR)
        
        self.valid_train_file_path = os.path.join(
            self.validated_dir,
            training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path = os.path.join(
            self.validated_dir,
            training_pipeline.TEST_FILE_NAME)
        
        self.invalid_dir = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR)
        
        self.invalid_train_file_path = os.path.join(
            self.invalid_dir,
            training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path = os.path.join(
            self.invalid_dir,
            training_pipeline.TEST_FILE_NAME)
        
        self.drift_report_dir = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR)
        
        self.drift_report_file_path = os.path.join(
            self.drift_report_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        
class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.timestamp = training_pipeline_config.timestamp
        self.pipeline_name = training_pipeline_config.pipeline_name
        self.artifact_dir = training_pipeline_config.artifact_dir      
        self.datatransformation_dir = os.path.join(
            self.artifact_dir,  
            training_pipeline.DATA_TRANSFORMATION_DIRECTORY_NAME)
        
        self.transformed_train_file_path:str= os.path.join(self.datatransformation_dir,
                                                           training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy")
        )
        self.transformed_test_file_path:str= os.path.join(self.datatransformation_dir,
                                                          training_pipeline.TEST_FILE_NAME.replace("csv", "npy")
        )
        self.preprocessor_object_file_path:str= os.path.join(self.datatransformation_dir,
                                                             training_pipeline.PROCESSING_OBJECT_FILE_NAME,
        )

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.timestamp = training_pipeline_config.timestamp
        self.pipeline_name = training_pipeline_config.pipeline_name
        self.artifact_dir = training_pipeline_config.artifact_dir      
        self.model_trainer_dir:str = os.path.join(
            self.artifact_dir,  
            training_pipeline.MODEL_TRAINER_DIRECTORY_NAME)     
        
        self.trained_model_file_path:str = os.path.join(
            self.model_trainer_dir,
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_FILE_NAME)
        
        self.expected_score:float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold:float = training_pipeline.MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD