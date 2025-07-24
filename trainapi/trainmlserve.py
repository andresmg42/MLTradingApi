
import requests
import time
from fastapi import FastAPI,Query
from ray import serve
from ml_parallel_pipeline import RollingOLSRegressionParallel
from symbols_list_distribution import symbolsList
import pandas as pd
from supabase import create_client
from pydantic import BaseModel
from io import BytesIO
from twitter_algorithm import TwitterSentimentAlgorithm
from storage3.exceptions import StorageException
import tempfile
from dotenv import load_dotenv
import io
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["*"] en desarrollo si quieres permitir todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    index:str
    start_date:str
    end_date:str
    batch_size:int



@serve.deployment
@serve.ingress(app)
class TrainAPI:

    def __init__(self):
        self.supabase=create_client(os.getenv('SUPABASE_URL'),os.getenv('SUPABASE_KEY'))
    
    @app.post("/yahoofinance")
    def store_portfolio_returns(self,item:Item):
        symbols_list=symbolsList(item.index)
        model=RollingOLSRegressionParallel(symbols_list,item.start_date,item.end_date)
        portfolio_returns=model.train_parallel_pipeline(item.batch_size)
        result=self.store_portfolio_supabase(portfolio_returns,f'train/{item.index}.csv')
        return result

    @app.get("/twitter")
    def store_twitter_portfolio(self):
        df=self.download_data('twitter-data/sentiment_data.csv')
        model=TwitterSentimentAlgorithm(df)
        portfolio_returns=model.twitter_pipeline(5)
        result=self.store_portfolio_supabase(portfolio_returns,'train/twitter.csv')
        return result

    def store_portfolio_supabase(self,portfolio_returns,path):
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
                temp_path = tmp.name
                portfolio_returns.to_csv(temp_path, index=True)
    
            
            with open(temp_path, "rb") as f:
                response = (
                    self.supabase.storage
                    .from_("datasets")
                    .upload(
                        file=f,
                        path=path,
                        file_options={"cache-control": "3600", "upsert": "true"}
                    )
                )
            return response
        except Exception as  e:
            print(f'error uploading file: {e}')

    def download_data(self,path):
    
        try:
            response=(
                    self.supabase.storage
                    .from_("datasets")
                    .download(path)
                )

            df=pd.read_csv(io.StringIO(response.decode('utf-8')))
                       
            return df
            
        except StorageException as e:
            if getattr(e,'error',None) and e.error.get("statusCode")==404:
                raise FileNotFoundError("train.csv not found in Supabase storage")
            else:
                raise Exception(f"Download failed: {e}")
    


if __name__=='__main__':

    serve.start(detached=True, http_options={'host':'0.0.0.0','port':8000})
    serve.run(TrainAPI.bind(), route_prefix='/train', blocking=True)



    
