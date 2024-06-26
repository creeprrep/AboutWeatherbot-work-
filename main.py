import telebot
import requests

API_TOKEN = '6640891121:AAH1DfOSErLkB7D9K-E3Z7uy75ZrbBE54ms'
WEATHERAPI_API_KEY = '70e4aff845b04f08a7b105711242406'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi I'm AboutWeatherBot \nJust tell me the name of your city and I'll tell you the weather.")

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city_name = message.text
    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_API_KEY}&q={city_name}'

    response = requests.get(url).json()

    if 'error' in response:
        bot.reply_to(message, "Sorry but I can't find it.")
        return

    current_weather = response['current']

    weather_description = current_weather['condition']['text']
    temperature = current_weather['temp_c']
    humidity = current_weather['humidity']
    city = response['location']['name']

    weather_report = (
        f"**Weather in {city}:**\n"
        f"Description: {weather_description}\n"
        f"Temperature: {temperature}°C\n"
    )

    bot.reply_to(message, weather_report, parse_mode='Markdown')

bot.polling()
