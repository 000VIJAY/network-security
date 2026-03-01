
import os
import dill

import numpy as np
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from networkSecurity.Exception.exception import NetworkSecurityException
from networkSecurity.Logging.logger import logger

def read_yaml_file(file_path:str) -> dict: # type: ignore
    import yaml
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(str(e), str(e)) from e

def write_yaml_file (file_path:str, data:dict, replace:bool = False) -> None: # type: ignore
    import yaml
    try:
        if replace :
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)        
        with open(file_path, 'w') as yaml_file:
            yaml.dump(data, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(str(e), str(e)) from e

def save_numpy_array_data(file_path:str, array:np.array): # type: ignore
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(str(e), str(e)) from e   
    
def save_object(file_path:str, obj:object) -> None:
    """
    file_path: str location of file to save
    obj: object to save
    """
    try:
        logger.info("Entering the save_object method of Main Utils class")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise NetworkSecurityException(str(e), str(e)) from e  
    
def load_object(file_path:str) -> object:
    """
    file_path: str location of file to load
    return: object loaded from file
    """
    try:
        logger.info("Entering the load_object method of Main Utils class")
        if not os.path.exists(file_path):
            raise NetworkSecurityException(f"The file: {file_path} is not found", f"The file: {file_path} is not found")
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(str(e), str(e)) from e       
    
def evaluate_models(X_train, y_train, X_test, y_test, models:dict, params:dict) -> dict:
    try:
        logger.info("Entering the evaluate_models method of Main Utils class")
        model_report = {}
        for model_name, model in models.items():
            logger.info(f"Evaluating model: {model_name}")
            param = params[model_name]
            gs = GridSearchCV(model, param, cv=3)
            
            gs.fit(X_train, y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            
            model_report[model_name] = test_model_score
        return model_report
    except Exception as e:
        raise NetworkSecurityException(str(e), str(e)) from e
    
def load_numpy_array_data(file_path:str) -> np.array: # type: ignore
    """
    Load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        if not os.path.exists(file_path):
            raise NetworkSecurityException(f"The file: {file_path} is not found", f"The file: {file_path} is not found")
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj, allow_pickle=True)
    except Exception as e:
        raise NetworkSecurityException(str(e), str(e)) from e    