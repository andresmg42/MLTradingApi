
import requests
from fastapi import FastAPI
from ray import serve
import pandas as pd
from pydantic import BaseModel
import yfinance as yf
import numpy as np
from supabase import  create_client
import uuid
import io
import tempfile
from dotenv import load_dotenv
import os
from storage3.utils import StorageException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()    
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["*"] en desarrollo si quieres permitir todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item_t(BaseModel):
    ticker:str
    start_date:str
    end_date:str
    index:str


@serve.deployment
@serve.ingress(app)
class InferenceAPI:

    def __init__(self):
        self.supabase=create_client(os.getenv('SUPABASE_URL'),os.getenv('SUPABASE_KEY'))

    @app.post('/')
    def get_portfolio_returns_to_visualize(self,item:Item_t):

        portfolio_df=self.download_data(item.index)
        
        data= yf.download(tickers=item.ticker,
                      start=item.start_date,
                      end=item.end_date, auto_adjust=False)
        data.columns = data.columns.droplevel(1)
    
        data_ret = np.log(data[['Adj Close']]).diff().dropna().rename({'Adj Close':f'{item.ticker} Buy&Hold'}, axis=1)
    
        portfolio_df =portfolio_df.merge(data_ret,
                                      left_index=True,
                                      right_index=True)

        response=self.store_portfolio_supabase(portfolio_df,item.ticker)
        return response

    def download_data(self,index):
    
        try:
            response=(
                    self.supabase.storage
                    .from_("datasets")
                    .download(f"train/{index}.csv")
                )

            df=pd.read_csv(io.StringIO(response.decode('utf-8')))
            df=df.set_index('Date')
            df.index=pd.to_datetime(df.index,format='%Y-%m-%d')
            df=df.sort_index()
                       
            return df
            
        except StorageException as e:
            if getattr(e,'error',None) and e.error.get("statusCode")==404:
                raise FileNotFoundError("train.csv not found in Supabase storage")
            else:
                raise Exception(f"Download failed: {e}")
    
    def store_portfolio_supabase(self,portfolio_returns,ticker):
        try:
            
            with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
                temp_path = tmp.name
                portfolio_returns.to_csv(temp_path, index=True)
    
            id= uuid.uuid4()
            with open(temp_path, "rb") as f:
                response = (
                    self.supabase.storage
                    .from_("datasets")
                    .upload(
                        file=f,
                        path=f"inference/inference_{ticker}_{id}.csv",
                        file_options={"cache-control": "3600", "upsert": "true"}
                    )
                )
            return response
        except Exception as  e:
            print(f'error uploading file: {e}')


if __name__=="__main__":

    serve.start(detached=True, http_options={'host':'0.0.0.0','port':8001})
    serve.run(InferenceAPI.bind(),route_prefix='/inference',blocking=True)
    