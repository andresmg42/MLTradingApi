
import pandas as pd


def sp500():
    
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    
    sp500['Symbol'] = sp500['Symbol'].str.replace('.', '-')
    
    symbols_list = sp500['Symbol'].unique().tolist()
    
    symbols_list=list(filter(lambda x: x not in ['SOLV', 'GEV', 'SW', 'VLTO'],symbols_list))

    return symbols_list

def down_jones():

    return [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'BRK-B', 'JPM', 'JNJ', 'V', 'PG',
        'MA', 'UNH', 'DIS', 'HD', 'VZ', 'NVDA', 'PYPL', 'BAC', 'ADBE', 'CMCSA',
        'NFLX', 'NKE', 'KO', 'PEP', 'MRK', 'PFE', 'XOM', 'CVX', 'WMT', 'T'
        ]

def nasdaq100():

    nasdaq100 = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100#External_links')[4]
    
    nasdaq100['Ticker'] = nasdaq100['Ticker'].str.replace('.', '-')
    
    symbols_list = nasdaq100['Ticker'].dropna().unique()
    
    symbols_list = [ticker for ticker in symbols_list.tolist() if pd.notna(ticker) and ticker != '']

    return symbols_list

def tsxcomposite():

    tsx = pd.read_html('https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index')[3]
    
    tsx['Ticker'] = tsx['Ticker'].str.replace('.', '-')
    
    symbols_list = tsx['Ticker'].dropna().unique()
    
    symbols_list = [ticker for ticker in symbols_list.tolist() if pd.notna(ticker) and ticker != '']

    deslisted_list=['BBU-UN', 'CSH-UN', 'GRT-UN', 'CHP-UN', 'CRR-UN', 'DPM', 'AIF', 'BEP-UN', 
 'TSU', 'CRT-UN', 'FCR-UN', 'BBD-B', 'TECK-B', 'QBR-B', 'PKI', 'NVEI', 'CTC-A', 
 'PMZ-UN', 'ONEX', 'IIP-UN', 'PRMW', 'BDGI', 'AP-UN', 'POW', 'HR-UN', 'BNS', 'ACO-X', 
 'IPCO', 'RCI-B', 'TCL-A', 'ENGH', 'EMP-A', 'SRU-UN', 'CSU', 'BEI-UN', 'GIB-A', 'CEU', 'TA', 'CCA', 
 'KMP-UN', 'ATH', 'FTT', 'CCL-B', 'ATRL', 'REI-UN', 'CAR-UN', 'DIR-UN', 'BIP-UN', 'CS', 'NWH-UN',
'NVA', 'LIF', 'LB', 'MFI', 'SOBO','NPI', 'ARX', 'DSG', 'AYA', 'WPK', 'MTL', 'CU', 'IVN', 'ABX', 'MDA', 'AAV', 'EFN', 'HWX', 'MTY'
    ]

    symbols_list=list(filter(lambda x: x not in deslisted_list,symbols_list))

    return symbols_list

def ftse100():
    ftse100 = pd.read_html('https://en.wikipedia.org/wiki/FTSE_100_Index')[4]
    
    ftse100['Ticker'] = ftse100['Ticker'].str.replace('.', '-')
    
    symbols_list = ftse100['Ticker'].dropna().unique()
    
    symbols_list = [ticker for ticker in symbols_list.tolist() if pd.notna(ticker) and ticker != '']

    deslisted_list=['SSE', 'UU','PSH','LGEN', 'AV', 'AAF', 'STJ', 'CRDA', 'SMT', 'BATS',
                    'FRES', 'GLEN', 'DPLM', 'LLOY', 'ENT', 'SGE', 'PSON', 'BARC', 'HLMA', 'LSEG', 
                    'AUTO', 'PHNX', 'SDR', 'ITRK', 'ANTO','RR', 'PSH' 'LGEN', 'IMI', 'BT-A', 'CCH', 
                    'CPG', 'SBRY', 'HSBA', 'FCIT', 'ULVR', 'INF', 'BNZL', 'HWDN', 'BTRW', 'EXPN', 'MRO', 'MNDI']

    symbols_list=list(filter(lambda x: x not in deslisted_list,symbols_list))
    
    return symbols_list

    
def symbolsList(index):
    match index:
        case 's&p500': return sp500()

        case 'downjones': return down_jones() 

        case 'nasdaq100': return nasdaq100()

        case 'tsxcomposite': return tsxcomposite()

        case 'ftse100': return ftse100()
            

