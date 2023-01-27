# Importing the yfinance package
import yfinance as yf
import pandas as pd

# Set the start and end date
start_date = '2023-01-05'
end_date = '2023-01-27'
#set the interval of the stock data
interval = "1d" # "1h", "1d", "1wk"
# Set the ticker
ticker = 'AAPL'
#set data_type -> 'Adj Close', 'Volume'
data_type = 'Adj Close'

def create_csv_from_ticker(ticker, start_date, end_date, interval, data_type):
    # Get the data
    df = pd.DataFrame(yf.download(ticker, start_date, end_date, interval=interval, rounding=2)[data_type])   
    #write dataframe to csv
    if (interval == "1h"):
        df.to_csv('data/{symbol}_{d_type}_hourly.csv'.format(symbol=ticker, d_type=data_type))
    elif (interval == "1d"):
        df.to_csv('data/{symbol}_{d_type}_daily.csv'.format(symbol=ticker, d_type=data_type))
    elif (interval == "1wk"):
        df.to_csv('data/{symbol}_{d_type}_weekly.csv'.format(symbol=ticker, d_type=data_type))
    else:
        df.to_csv('data/{symbol}_{d_type}.csv'.format(symbol=ticker, d_type=data_type))

create_csv_from_ticker(ticker=ticker, start_date=start_date, end_date=end_date, interval=interval, data_type=data_type)