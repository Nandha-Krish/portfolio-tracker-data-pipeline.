import json
import yfinance as yf
import pymysql
import os
from datetime import datetime

# AWS Cloud Credentials
DB_HOST = 'banking-project-db.copo26e6ow47.us-east-1.rds.amazonaws.com'
DB_USER = 'root'             
DB_PASS = 'Clast14340fair!'
DB_NAME = 'portfolio_tracker'

def lambda_handler(event, context):
    tickers = ['AAPL', 'MSFT', 'JPM', 'V', 'TGT']
    today_date = datetime.today().strftime('%Y-%m-%d')
    price_data = []
    
    print("Fetching market data...")
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                close_price = round(hist['Close'].iloc[0], 2)
                price_data.append((ticker, today_date, close_price))
                print(f"Grabbed {ticker}: ${close_price}")
        except Exception as e:
            print(f"Could not fetch data for {ticker}: {e}")

    print("Connecting to the database...")
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO daily_prices (ticker, price_date, close_price)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE close_price = VALUES(close_price);
        """
        cursor.executemany(insert_query, price_data)
        connection.commit()
        
        success_msg = f'Successfully updated database with {len(price_data)} new closing prices.'
        print(success_msg)
        return {'statusCode': 200, 'body': json.dumps(success_msg)}
    except Exception as e:
        error_msg = f"Database Error: {e}"
        print(error_msg)
        return {'statusCode': 500, 'body': json.dumps(error_msg)}
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    lambda_handler(None, None)
