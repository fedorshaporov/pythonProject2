import pytest
import json
import pandas as pd
import datetime
from unittest.mock import patch, MagicMock
from src.views import (
    get_currency_rates,
    get_stock_prices,
    calculate_greeting,
    analyze_expenses,
    generate_json_response
)


data = {
    'Дата операции': ['2020-05-01 10:00:00', '2020-05-05 12:00:00'],  # Пример строковых дат
    'Номер карты': ['1234567890127197', '1234567890123456'],  # Проверьте первое значение
    'Сумма операции': [1000, 2000],
    'Сумма платежа': [1000, 2000],
    'Категория': ['Еда', 'Транспорт'],
    'Описание': ['Кафе', 'Такси']
}
df = pd.DataFrame(data)


@pytest.fixture
def mock_user_settings(tmp_path):
    """Создает временный user_settings.json файл."""
    user_settings = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }
    settings_file = tmp_path / "user_settings.json"
    with open(settings_file, 'w') as f:
        json.dump(user_settings, f)
    return str(settings_file)  # Возвращаем путь к файлу

def test_get_currency_rates(mocker):
    """Тест для функции get_currency_rates."""
    mock_response = {
        "Realtime Currency Exchange Rate": {
            "5. Exchange Rate": "75.00"
        }
    }
    mocker.patch('requests.get', return_value=MagicMock(json=lambda: mock_response))

    rates = get_currency_rates(["USD"])

    assert rates["USD"] == 75.00

def test_get_stock_prices(mocker):
    """Тест для функции get_stock_prices."""
    mock_response = {
        "Time Series (Daily)": {
            "2023-09-01": {"4. close": "150.00"},
            "2023-09-02": {"4. close": "155.00"}
        }
    }
    mocker.patch('requests.get', return_value=MagicMock(json=lambda: mock_response))

    stocks = get_stock_prices(["AAPL"])

    assert stocks["AAPL"] == 150.00

def test_calculate_greeting(monkeypatch):
    """Тест для функции calculate_greeting."""
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = datetime.datetime(2021, 3, 11, 10, 0, 0)


    monkeypatch.setattr(datetime, "datetime", datetime_mock)
    greeting = calculate_greeting()
    assert greeting == "Доброе утро"

def test_analyze_expenses():
    """Тест для функции analyze_expenses."""
    # Преобразуем данные для использования в тестах
    df_test = df.copy()
    df_test['Дата операции'] = pd.to_datetime(df_test['Дата операции'])

    result = analyze_expenses(df_test, "2020-05-05 12:00:00")

    assert len(result['cards']) == 1
    assert result['cards'][0]['last_digits'] == '3456'
    assert result['cards'][0]['total_spent'] == 2000.0
    assert result['cards'][0]['cashback'] == 20.0
    assert len(result['top_transactions']) == 1  # Поскольку у нас 2 транзакции


@patch('src.views.load_operations')
@patch('src.views.get_currency_rates')
@patch('src.views.get_stock_prices')
def test_generate_json_response(mock_get_stock_prices, mock_get_currency_rates, mock_load_operations, mock_user_settings):
    """Тест для функции generate_json_response."""

    # Установим моки
    mock_load_operations.return_value = df.copy()  # Используем ваши тестовые данные
    mock_get_currency_rates.return_value = {"USD": 75.0, "EUR": 83.0}
    mock_get_stock_prices.return_value = {"AAPL": 150.0, "AMZN": 3000.0}

    # Сгенерируем JSON ответ, передавая путь к временно созданному файлу настроек
    response = generate_json_response("2020-05-05 12:00:00", mock_user_settings)

    # Проверки
    assert "greeting" in response
    assert "cards" in response
    assert "top_transactions" in response
    assert "currency_rates" in response
    assert "stock_prices" in response

    assert len(response["cards"]) == 1
    assert response["cards"][0]["last_digits"] == "3456"  # Подгоните под ваши данные
    assert len(response["top_transactions"]) == 1
    assert response["currency_rates"] == [
        {"currency": "USD", "rate": 75.0},
        {"currency": "EUR", "rate": 83.0},
    ]
    assert response["stock_prices"] == [
        {"stock": "AAPL", "price": 150.0},
        {"stock": "AMZN", "price": 3000.0},
    ]

if __name__ == "__main__":
    pytest.main()
