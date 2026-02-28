from networkSecurity.Components.data_ingestion import DataIngestion
from networkSecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

if __name__ == "__main__":
    data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
    data_ingestion = DataIngestion(data_ingestion_config)
    df = data_ingestion.export_collection_as_dataframe()
    data_ingestion.save_feature_store_file(df)
    train_df, test_df = data_ingestion.split_data_as_train_test_save(df)
