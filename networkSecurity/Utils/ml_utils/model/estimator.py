from networkSecurity.Exception.exception import NetworkSecurityException
from networkSecurity.Logging.logger import logger

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            logger.info(f"Initializing NetworkModel with preprocessor and model.")
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e
        
    def predict(self, X):
        try:
            X_transformed = self.preprocessor.transform(X)
            return self.model.predict(X_transformed)
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e