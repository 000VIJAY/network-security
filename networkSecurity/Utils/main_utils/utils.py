
import os

from networkSecurity.Exception.exception import NetworkSecurityException

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