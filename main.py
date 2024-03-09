from dotenv import load_dotenv
import os
import requests
import datetime as dt
import smtplib


load_dotenv()
ALPHAVANTAGE_KEY = os.environ.get('ALPHAVANTAGE_KEY')
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')
EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('MY_PASSWORD')
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


def get_close(data: dict, days_in_past: int) -> float:
    return float(data['Time Series (Daily)'][str(dt.date.today()-dt.timedelta(days=days_in_past))]['4. close'])

alpha_stem = 'https://www.alphavantage.co/query'
alpha_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': ALPHAVANTAGE_KEY
}
news_stem = 'https://newsapi.org/v2/everything'
news_params = {
    'q': COMPANY_NAME,
    'apiKey': NEWSAPI_KEY
}

response = requests.get(alpha_stem, params=alpha_params)
response.raise_for_status()
stock_data = response.json()

yesterday_close = get_close(stock_data, 1)
two_days_ago_close = get_close(stock_data, 2)
pct_diff = 100*(yesterday_close-two_days_ago_close)/yesterday_close

if abs(pct_diff) >= 5:
    response = requests.get(news_stem, params=news_params)
    response.raise_for_status()
    top_3 = response.json()['articles'][:3]
    
    for article in top_3:
        # Send email
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()

            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=f'Subject:{STOCK}: {"🔺" if pct_diff > 0 else "🔻"}{round(pct_diff)}%\n\n\nHeadline: {article["title"]}\nBrief: {article["description"]}'.encode('utf-8')
            )