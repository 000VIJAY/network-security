from networkSecurity.Exception.exception import NetworkSecurityException
from sklearn.metrics import precision_score, recall_score, f1_score

from networkSecurity.entity.artifact_entity import ClassificationMetricArtifact

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact: # type: ignore
    try:
        precision:float = precision_score(y_true, y_pred, average='weighted') # type: ignore
        recall:float = recall_score(y_true, y_pred, average='weighted') # type: ignore
        f1:float = f1_score(y_true, y_pred, average='weighted') # type: ignore
        
        classification_report = ClassificationMetricArtifact(
            precision_score=precision,
            recall_score=recall,
            f1_score=f1)
        
        return classification_report
    except Exception as e:
        raise NetworkSecurityException(str(e), str(e)) from e