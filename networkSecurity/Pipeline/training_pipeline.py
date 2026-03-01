from networkSecurity.Components.data_transformation import DataTransformation
from networkSecurity.Components.data_validation import DataValidation
from networkSecurity.Components.model_trainer import ModelTrainer
from networkSecurity.Exception.exception import NetworkSecurityException
from networkSecurity.Logging.logger import logger

from networkSecurity.Components.data_ingestion import DataIngestion
from networkSecurity.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact, ModelTrainerArtifact
from networkSecurity.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig)

class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
            logger.info(f"{'>>'*20} Training Pipeline {'<<'*20}")
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config)
            logger.info("Starting data ingestion")
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logger.info("Data ingestion completed")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e    
    
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_validation_config, data_ingestion_artifact)
            logger.info("Starting data validation")
            data_validation_artifact = data_validation.initialize_data_validation_artifact()
            logger.info("Data validation completed")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e
        
    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logger.info("Starting data transformation")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logger.info("Data transformation completed")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e
        
    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logger.info("Starting model training")
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logger.info("Model training completed")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e  
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            logger.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e    
          