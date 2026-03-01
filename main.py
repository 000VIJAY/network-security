from networkSecurity.Components.data_transformation import DataTransformation
from networkSecurity.Components.data_validation import DataValidation
from networkSecurity.Components.model_trainer import ModelTrainer
from networkSecurity.Logging.logger import logger

from networkSecurity.Components.data_ingestion import DataIngestion
from networkSecurity.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig, ModelTrainerConfig, TrainingPipelineConfig

if __name__ == "__main__":
    data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
    data_ingestion = DataIngestion(data_ingestion_config)
    logger.info("Starting data ingestion")
    data_ingestion.initiate_data_ingestion()
    logger.info("Data ingestion completed")
    
    
    data_validation_config = DataValidationConfig(TrainingPipelineConfig())
    data_validation = DataValidation(data_validation_config, data_ingestion.initiate_data_ingestion())
    
    data_validation.initialize_data_validation_artifact()
    logger.info("Data validation completed")
    
    logger.info("Starting data transformation")
    data_transformation_config = DataTransformationConfig(TrainingPipelineConfig())
    
    data_transformation = DataTransformation(data_validation.initialize_data_validation_artifact(), data_transformation_config)
    data_transformation.initiate_data_transformation()
    
    logger.info("Data transformation completed")
    
    logger.info("Starting model training")
    model_trainer_config = ModelTrainerConfig(TrainingPipelineConfig())
    model_trainer = ModelTrainer(model_trainer_config, data_transformation.initiate_data_transformation())
    model_trainer.initiate_model_trainer()
    logger.info("Model training completed")
