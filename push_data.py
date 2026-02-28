import os
import json
import certifi
from dotenv import load_dotenv

import pymongo
import pandas as pd
from networkSecurity.Logging.logger import logger
from networkSecurity.Exception.exception import NetworkSecurityException

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise NetworkSecurityException("Failed to connect to MongoDB", str(e))
        
    def cv_to_json_convertor(self, file_path: str) -> list[dict[str, object]]:
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = list(json.loads(df.to_json(orient='records')))
            return records
        except Exception as e:
            logger.error(f"Failed to convert CSV to JSON: {str(e)}")
            raise NetworkSecurityException("Failed to convert CSV to JSON", str(e))
        
    def insert_data_to_mongodb(self, records, database, collection): # type: ignore
        try:
            self.database = database # type: ignore
            self.collection = collection # type: ignore
            self.records = records # type: ignore
            self.mongo_client =  pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database] # pyright: ignore[reportUnknownMemberType]
            self.collection = self.database[self.collection] # type: ignore
            self.collection.insert_many(self.records) # type: ignore
            logger.info(f"Successfully inserted data into MongoDB collection: {self.collection.name}") # type: ignore
            return (len(self.records)) # type: ignore
        except Exception as e:
            logger.error(f"Failed to insert data into MongoDB: {str(e)}")
            raise NetworkSecurityException("Failed to insert data into MongoDB", str(e))        
        
if __name__ == "__main__":
    FILE_PATH = "network_data/phisingData.csv"
    DATABASE = "Network_Security"
    Collection = "Network_Data"
    networkObj = NetworkDataExtract()
    try:
        records = networkObj.cv_to_json_convertor(FILE_PATH)
        no_of_records = len(records)
        inserted_count = networkObj.insert_data_to_mongodb(records, DATABASE, Collection)
        logger.info(f"Inserted {inserted_count} records into MongoDB collection: {Collection}")
    except Exception as e:
        NetworkSecurityException("An error occurred while processing the data", str(e))