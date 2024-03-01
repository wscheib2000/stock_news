from dotenv import load_dotenv
import os
import requests
import datetime as dt


load_dotenv()
alphavantage_key = os.environ.get('ALPHAVANTAGE_KEY')
newsapi_key = os.environ.get('NEWSAPI_KEY')
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


def get_close(data: dict, days_in_past: int) -> float:
    return float(data['Time Series (Daily)'][str(dt.date.today()-dt.timedelta(days=days_in_past))]['4. close'])

alpha_stem = 'https://www.alphavantage.co/query'
params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': alphavantage_key
}
response = requests.get(alpha_stem, params)
response.raise_for_status()
yesterday_close = get_close(response.json(), 1)
two_days_ago_close = get_close(response.json(), 2)
pct_diff = 100*(yesterday_close-two_days_ago_close)/two_days_ago_close
if abs(pct_diff) >= 5:
    print('Get News')


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

