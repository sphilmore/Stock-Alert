import os
import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API= os.environ.get('api_stock')
parameters ={
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API
}
response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
stock_data = data["Time Series (Daily)"]
stock_list_data = [value['4. close'] for value in stock_data.values()]
yesterday_stock_price=float(stock_list_data[0])
day_before_yesterday = float(stock_list_data[1])
difference = (yesterday_stock_price - day_before_yesterday)
up_down =None
if difference >0:
    up_down = "⬆"
else:
    up_down = "⬇"
percentage_difference = round((difference/yesterday_stock_price) *100)
if abs(percentage_difference) >0:
    print("Get News")
parameters_news ={
    "q": COMPANY_NAME,
    'apikey': os.environ.get('KEYS')
}
account_sid= os.environ.get('Account_Sid')
auth_token = os.environ.get('Auth_Token')
news_response = requests.get(url=NEWS_ENDPOINT, params=parameters_news)
news_response.raise_for_status()
news_data =news_response.json()['articles'][:3]
article_list = [f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline:{stuff['title']}.\nBrief: {stuff['description']}" for stuff in news_data]
for articles in article_list:
        client = Client(account_sid, auth_token)
        message = client.messages \
        .create(
        body= articles,
        from_='+19897621014',
        to='+12158239955'
    )
        print(message.sid)

