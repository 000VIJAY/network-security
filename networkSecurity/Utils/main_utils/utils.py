
import os
import dill

import numpy as np

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