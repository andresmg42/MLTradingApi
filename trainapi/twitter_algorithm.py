
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
import ray
import argparse


@ray.remote(memory=600*1024*1024)
def download_fresh_prices(stock_list):

    prices_df = yf.download(tickers=stock_list,
                                start='2021-01-01',
                                end='2023-03-01',auto_adjust=False)
        
    return prices_df 


class TwitterSentimentAlgorithm():
    def __init__(self,df):
        
        self.df=df

    def load_data(self):
        
        sentiment_df=self.df
        
        sentiment_df['date']=pd.to_datetime(sentiment_df['date'])
        
        sentiment_df = sentiment_df.set_index(['date', 'symbol'])

        sentiment_df['engagement_ratio'] = sentiment_df['twitterComments']/sentiment_df['twitterLikes']
        
        sentiment_df = sentiment_df[(sentiment_df['twitterLikes']>20)&(sentiment_df['twitterComments']>10)]
        
        return sentiment_df

    def aggragated(self,sentiment_df):
        
        aggragated_df = (sentiment_df.reset_index('symbol').groupby([pd.Grouper(freq='M'), 'symbol'])
                    [['engagement_ratio']].mean())

        aggragated_df['rank'] = (aggragated_df.groupby(level=0)['engagement_ratio']
                         .transform(lambda x: x.rank(ascending=False)))

        return aggragated_df

    def select_top_5_stocks(self,aggragated_df):

        filtered_df = aggragated_df[aggragated_df['rank']<6].copy()

        filtered_df = filtered_df.reset_index(level=1)
        
        filtered_df.index = filtered_df.index+pd.DateOffset(1)
        
        filtered_df = filtered_df.reset_index().set_index(['date', 'symbol'])
        
        return filtered_df

    def extract_stocks_start_month(self,filtered_df):
        dates = filtered_df.index.get_level_values('date').unique().tolist()

        fixed_dates = {}
        
        for d in dates:
            
            fixed_dates[d.strftime('%Y-%m-%d')] = filtered_df.xs(d, level=0).index.tolist()
            
        return fixed_dates


    def download_fresh_prices_p(self,sentiment_df,batch_size):
        stocks_list = sentiment_df.index.get_level_values('symbol').unique().tolist()
        
        batches=np.array_split(stocks_list,batch_size)

        futures=[download_fresh_prices.remote(batch.tolist()) for batch in batches]

        df_results=ray.get(futures)

        df_results=pd.concat(df_results, axis=1)

        return df_results

      

    def calculate_portfolio_returns(self,prices_df,fixed_dates):
        returns_df = np.log(prices_df['Adj Close']).diff().dropna(axis=0,how='all')

        portfolio_df = pd.DataFrame()
        
        for start_date in fixed_dates.keys():
            
            end_date = (pd.to_datetime(start_date)+pd.offsets.MonthEnd()).strftime('%Y-%m-%d')
            
            cols = fixed_dates[start_date]
            
            temp_df = returns_df[start_date:end_date][cols].mean(axis=1).to_frame('portfolio_return')
            
            portfolio_df = pd.concat([portfolio_df, temp_df], axis=0)
    
        return portfolio_df

    
    

    def twitter_pipeline(self,batch_size):

        sentiment_df=self.load_data()

        aggragated_df=self.aggragated(sentiment_df)

        filtered_df=self.select_top_5_stocks(aggragated_df)

        fixed_dates=self.extract_stocks_start_month(filtered_df)

        prices_df=self.download_fresh_prices_p(sentiment_df,batch_size)

        portfolio_df=self.calculate_portfolio_returns(prices_df,fixed_dates)

        return portfolio_df

if __name__=='__main__':

    parser=argparse.ArgumentParser(description='Process some arguments')
    parser.add_argument('--path','-p',type=str,required=True,help='sentiment_data.csv path')

    args=parser.parse_args()

    tws=TwitterSentimentAlgorithm(args.path)

    results=tws.twitter_pipeline(5)

    print(results)
    
    
