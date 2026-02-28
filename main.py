from networkSecurity.Components.data_validation import DataValidation
from networkSecurity.Logging.logger import logger

from networkSecurity.Components.data_ingestion import DataIngestion
from networkSecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, TrainingPipelineConfig

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
    
