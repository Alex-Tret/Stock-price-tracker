import requests
from datetime import datetime, timedelta
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

def get_news():
    parameters_news = {
        "qInTitle": COMPANY_NAME,
        "apiKey": "70f130fa1cea4305b3f38182dc599ac6",
        "language": "en"

    }
    response_news = requests.get(url="https://newsapi.org/v2/everything", params=parameters_news)
    response_news.raise_for_status()

    data_news = response_news.json()['articles'][:3]

    formated_articles = [f"\n{STOCK} {up_down} {diff_percentage}\n" \
                         f"Headline: {article['title']}\n" \
                         f"Brief: {article['description']}\n" \
                         f"URL: {article['url']}" for article in data_news]

    for article in formated_articles:
        account_sid = 'AC65b82b0716b4fa6fe4e8c641c4e82044'
        auth_token = '3f8cbd6897ca2b8ad08301e3117141b6'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=article,
            from_='+14027692997',
            to='+380504142724'
        )

        print(message.status)

parameters_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "QOBHD7KPD1RGMDSB"
}

response_stock = requests.get(url="https://www.alphavantage.co/query", params=parameters_stock)
response_stock.raise_for_status()
data = response_stock.json()['Time Series (Daily)']

data_list = [value for (key, value) in data.items()]

# yesterday = str(datetime.now() - timedelta(days=1)).split()[0]
# before_yesterday = str(datetime.now() - timedelta(days=2)).split()[0]

yesterday_price_close = float(data_list[0]['4. close'])
before_yesterday_price_close = float(data_list[1]['4. close'])
diff_dollar = round(yesterday_price_close - before_yesterday_price_close, 2)
diff_percentage = abs(round(diff_dollar * 100 / yesterday_price_close, 2))

up_down=None
if diff_dollar > 0:
    up_down = "🔺"
else:
    up_down = "🔻"



if diff_percentage >= 0.5:
    get_news()








