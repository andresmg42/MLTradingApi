from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import numpy as np
import io
from supabase import create_client
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["*"] en desarrollo si quieres permitir todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

class URLItem(BaseModel):
    url: str

@app.post('/plot')
async def generate_graph(item: URLItem):
    try:
        url = item.url
        response = (
            supabase.storage
            .from_("datasets")
            .download(url)
        )

        df = pd.read_csv(io.StringIO(response.decode('utf-8')))
        df = df.set_index('Date')
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
        df = df.sort_index()

        plt.style.use('ggplot')

        portfolio_cumulative_return = np.exp(np.log1p(df).cumsum()) - 1
        portfolio_cumulative_return[:'2023-09-29'].plot(figsize=(16, 6))

        plt.title('Unsupervised Learning Trading Strategy Returns Over Time')
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
        plt.ylabel('Return')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)