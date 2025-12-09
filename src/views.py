from src.utils import load_operations
from src.business_logic import analyze_expenses, calculate_greeting
from src.api_integration import get_currency_rates, get_stock_prices
import json


def generate_json_response(date_time):
    """Генерирует JSON-ответ с данными о расходах, курсах валют и ценах акций."""
    # Загрузка операций
    file_path = 'data/operations.xlsx'
    data = load_operations(file_path)

    # Получение приветствия
    greeting = calculate_greeting()

    # Анализируем расходы
    expense_analysis = analyze_expenses(data, date_time)

    # Получение валют и акций из user_settings.json
    with open('user_settings.json', 'r') as f:
        user_settings = json.load(f)

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

    return json.dumps(response, ensure_ascii=False)
