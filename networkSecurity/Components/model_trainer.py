import os

from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
    ExtraTreesClassifier
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

from networkSecurity.Utils.ml_utils import model
from networkSecurity.Utils.ml_utils.metric.classification_metric import get_classification_score
from networkSecurity.Utils.ml_utils.model.estimator import NetworkModel
from networkSecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networkSecurity.entity.config_entity import DataTransformationConfig , ModelTrainerConfig
from networkSecurity.entity.config_entity import ModelTrainerConfig

from networkSecurity.Exception.exception import NetworkSecurityException
from networkSecurity.Logging.logger import logger
from networkSecurity.Utils.main_utils.utils import evaluate_models, save_object, load_object, load_numpy_array_data

class ModelTrainer:
    def __init__ (self, model_trainer_config:ModelTrainerConfig,
                  data_transformation_artifact:DataTransformationArtifact):
        try:
            logger.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e
    
    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models ={
                "RandomForestClassifier": RandomForestClassifier(verbose=1),
                "AdaBoostClassifier": AdaBoostClassifier(),
                "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1),
                "ExtraTreesClassifier": ExtraTreesClassifier(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "LogisticRegression": LogisticRegression(verbose=1)
            }
            
            params = {
                "DecisionTreeClassifier": {
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },
                "RandomForestClassifier": {
                    'n_estimators': [100, 200],
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [None, 10, 20],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2]
                },
                "AdaBoostClassifier": {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.01, 0.1, 1]
                },
                "GradientBoostingClassifier": {
                    'n_estimators': [100, 200],
                    'learning_rate': [0.01, 0.1, 1],
                    'max_depth': [3, 5, 7]
                },
                "ExtraTreesClassifier": {
                    'n_estimators': [100, 200],
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [None, 10, 20],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2]
                },
                "LogisticRegression": {
                    'C': [0.01, 0.1, 1, 10],
                    'solver': ['liblinear', 'lbfgs']
                }
            }
            
            model_report:dict = evaluate_models(X_train, y_train, X_test, y_test, models, params)

            best_model_score = max(sorted(model_report.values())) # type: ignore
            
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)   
            ]  
            best_model = models[best_model_name]
            y_train_pred = best_model.predict(X_train)
            
            classification_train_metric = get_classification_score(y_true = y_train, y_pred = y_train_pred)
            
            ## Track the mlflow metric for train dataset
            
            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_score(y_true = y_test, y_pred = y_test_pred)
            
            preprocessor = load_object(file_path=self.data_transformation_artifact.preprocessor_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            
            
            os.makedirs(model_dir_path, exist_ok=True)
            network_model =NetworkModel(preprocessor=preprocessor, model=best_model)
            
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)
            
            ## modeel trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            
            logger.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(str(e), str(e)) from e
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
            try:
                train_file_path = self.data_transformation_artifact.transformed_train_file_path
                test_file_path = self.data_transformation_artifact.transformed_test_file_path
                
                ## loading training and test arrays
                train_array = load_numpy_array_data(train_file_path)
                test_array = load_numpy_array_data(test_file_path)
                
                X_train, y_train = train_array[:,:-1], train_array[:,-1]
                X_test, y_test = test_array[:,:-1], test_array[:,-1]
                
                model =self.train_model(X_train, y_train, X_test, y_test)
                
                return model
            except Exception as e:
                raise NetworkSecurityException(str(e), str(e)) from e