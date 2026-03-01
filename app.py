from dotenv import load_dotenv
import os
import sys

import pymongo

from networkSecurity.Constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from networkSecurity.Utils.ml_utils.model.estimator import NetworkModel

mongo_uri = os.getenv("MONGO_DB_URL")

from fastapi import FastAPI , File, Response, UploadFile,Request
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
import pandas as pd
from networkSecurity.Pipeline.training_pipeline import TrainingPipeline
from networkSecurity.Exception.exception import NetworkSecurityException    
from networkSecurity.Utils.main_utils.utils import load_object
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")


client = pymongo.MongoClient(mongo_uri)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful!!")
    except Exception as e:
        raise NetworkSecurityException(str(e), str(e)) from e

@app.post("/predict")
async def predict(request:Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor_path = os.path.join("final_models", "preprocessor.pkl")
        preprocessor = load_object(preprocessor_path)
        network_model_path = os.path.join("final_models", "model.pkl")
        final_model = load_object(network_model_path)
        
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        
        print(df.iloc[0])
        
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicated_column'] = y_pred
        print(df['predicated_column'])
        
        df.to_csv("predication_output/predicted_output.csv", index=False)
        
        table_html = df.to_html(classes="table table-striped", index=False)
        return templates.TemplateResponse("predict.html", {"request": request, "table_html": table_html})
    except Exception as e:
        raise NetworkSecurityException(str(e), str(e)) from e

    
if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
    
    
    