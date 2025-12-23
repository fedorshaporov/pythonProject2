import json
import os
import time

import pandas as pd
import requests
from datetime import datetime
from src.utils import load_operations  # Функция для загрузки операций

API_KEY = 'JD0XXUZQH8WIG3Q8'


def get_currency_rates(currencies):
    """Получает курсы валют из Alpha Vantage API."""
    rates = {}
    for currency in currencies:
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency}&to_currency=RUB&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        if "Realtime Currency Exchange Rate" in data:
            rates[currency] = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        else:
            rates[currency] = None  # Если данные недоступны или произошла ошибка
        time.sleep(1)
    return rates


def get_stock_prices(stocks):
    """Получает текущие цены акций из Alpha Vantage API."""
    stock_prices = {}
    for stock in stocks:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()

        if "Time Series (Daily)" in data:
            # Получаем последнюю дату в данных
            last_refresh = sorted(data["Time Series (Daily)"].keys())[0]
            # Получаем цену закрытия за последний день
            stock_prices[stock] = float(data["Time Series (Daily)"][last_refresh]["4. close"])
        else:
            stock_prices[stock] = None  # Если данные недоступны
        time.sleep(1)

    return stock_prices


def calculate_greeting():
    """Возвращает приветствие в зависимости от времени суток."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def analyze_expenses(data, date_time):
    """Анализирует данные о транзакциях и возвращает нужные параметры."""
    start_date = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').replace(day=1)
    end_date = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    filtered_data = data[
        (data['Дата операции'] >= start_date) &
        (data['Дата операции'] <= end_date)
    ]
    filtered_data['Дата операции'] = pd.to_datetime(filtered_data['Дата операции'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')

    result = {
        "cards": [],
        "top_transactions": []
    }

    # Группируем по картам
    card_group = filtered_data.groupby('Номер карты')
    for card, group in card_group:
        total_spent = group['Сумма операции'].sum()
        cashback = total_spent / 100.0
        last_digits = str(card)[-4:]
        result['cards'].append({
            'last_digits': last_digits,
            'total_spent': float(total_spent),
            'cashback': float(cashback)
        })

    # Топ-5 транзакций
    top_transactions = filtered_data.nlargest(5, 'Сумма платежа')[['Дата операции', 'Сумма платежа', 'Категория', 'Описание']]
    result['top_transactions'] = top_transactions.to_dict(orient='records')

    return result


def generate_json_response(date_time):
    """Генерирует JSON-ответ с данными о расходах, курсах валют и ценах акций."""
    # Определяем базовую директорию проекта и путь к файлу
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', 'operations.xlsx')  # Создаем правильный путь

    # Загрузка операций
    data = load_operations(file_path)

    # Получение приветствия
    greeting = calculate_greeting()

    # Анализируем расходы
    expense_analysis = analyze_expenses(data, date_time)

    # Загружаем пользовательские настройки
    with open('../user_settings.json', 'r') as f:
        user_settings = json.load(f)

    # Получаем курсы валют и цены акций
    currency_rates = get_currency_rates(user_settings['user_currencies'])
    stock_prices = get_stock_prices(user_settings['user_stocks'])

    # Формируем окончательный ответ
    response = {
        "greeting": greeting,
        "cards": expense_analysis['cards'],
        "top_transactions": expense_analysis['top_transactions'],
        "currency_rates": [{"currency": currency, "rate": rate} for currency, rate in currency_rates.items()],
        "stock_prices": [{"stock": stock, "price": price} for stock, price in stock_prices.items()]
    }

    return response


print(generate_json_response("2021-12-31 00:00:00"))