import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "N1XJ4T11HTH2KOVC"
NEWS_API_KEY = "e51a419aabdd4dbb86a91796f52d07d3"

TWILIO_ACCOUNT_SID = "AC90c7d4acef77cf488f93cfb59992bc3f"
TWILIO_AUTH_TOKEN = "889a36807c3729a921cf6a8e5440625d"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
stockData = response.json()["Time Series (Daily)"]
dataList = [value for (key, value) in stockData.items()]
dataList = dataList[:2]
yesterday_price = dataList[0]["4. close"]
# Get the day before yesterday's closing stock price
day_before_yesterday_price = dataList[1]["4. close"]
# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
price_difference = float(day_before_yesterday_price) - float(yesterday_price)

up_down = None
if price_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = round((abs(price_difference) / float(yesterday_price)) * 100)
# If TODO4 percentage is greater than 5 then print("Get News").

# STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if percentage_difference >= 0:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = response.json()["articles"]

    # TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    # STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    # TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{percentage_difference}% \n Headline: {article['title']}. \n Brief: {article['description']}"
        for article in three_articles
    ]
    # TODO 9. - Send each article as a separate message via Twilio.
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for articles in formatted_articles:
        message = client.messages.create(
            from_="+12562865270",
            body=articles,
            to="+917351391114",
        )

# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
