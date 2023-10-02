import requests
from twilio.rest import Client

OWN_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"

api_key = "f06077ff57ef50c5c5701e9d51456356"

account_sid = "AC90c7d4acef77cf488f93cfb59992bc3f"
auth_token = "889a36807c3729a921cf6a8e5440625d"

weather_params = {
    "lat": 18.969049,
    "lon": 72.821182,
    "appid": api_key,
    "exclude": "current,minutely,daily,alerts",
}

response = requests.get(OWN_Endpoint, params=weather_params)
response.raise_for_status()

weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hourly_data in weather_slice:
    condition_code = hourly_data["weather"][0]["id"]
    if int(condition_code) < 600:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It is going to rain, bring an ☔",
        from_="+12562865270",
        to="+917351391114",
    )
    print(message.status)
