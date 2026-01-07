import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

API_KEY = os.getenv('API_KEY')  # Получаем ключ API из .env


def get_currency_rates(currencies):
    """Получает курсы валют из Alpha Vantage API."""
    rates = {}
    for currency in currencies:
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency={currency}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        if "Realtime Currency Exchange Rate" in data:
            rates[currency] = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        else:
            rates[currency] = None  # Обработка ошибок, если API возвращает ошибку

    return rates


def get_stock_prices(stocks):
    """Получает текущие цены акций из Alpha Vantage API."""
    stock_prices = {}
    for stock in stocks:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()

        # Проверяем, что данные корректные
        if "Time Series (Daily)" in data:
            # Получаем последнюю дату
            last_refresh = sorted(data["Time Series (Daily)"].keys())[0]
            # Получаем цену закрытия за последний день
            stock_prices[stock] = float(data["Time Series (Daily)"][last_refresh]["4. close"])
        else:
            stock_prices[stock] = None  # Если данные недоступны или произошла ошибка

    return stock_prices
