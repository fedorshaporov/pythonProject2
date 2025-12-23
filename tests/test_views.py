import pytest
import json
import pandas as pd
from unittest.mock import patch, MagicMock
from src.views import (
    get_currency_rates,
    get_stock_prices,
    calculate_greeting,
    analyze_expenses,
    generate_json_response
)

# Тестовые данные
TEST_DATA = {
    "Дата операции": ["2020-05-01 12:00:00", "2020-05-05 15:00:00"],
    "Номер карты": [7197, 7197],
    "Сумма операции": [-160.89, -64.00],
    "Сумма платежа": [160.89, 64.00],
    "Категория": ["Супермаркеты", "Супермаркеты"],
    "Описание": ["Колхоз", "Лента"]
}

df = pd.DataFrame(TEST_DATA)

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
    return str(settings_file)

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
    monkeypatch.setattr("datetime.datetime", MagicMock(return_value=datetime(2023, 3, 20, 10, 0)))

    greeting = calculate_greeting()
    assert greeting == "Доброе утро"

def test_analyze_expenses():
    """Тест для функции analyze_expenses."""
    # Преобразуем данные для использования в тестах
    df_test = df.copy()
    df_test['Дата операции'] = pd.to_datetime(df_test['Дата операции'])

    result = analyze_expenses(df_test, "2020-05-05 12:00:00")

    assert len(result['cards']) == 1
    assert result['cards'][0]['last_digits'] == '7197'
    assert result['cards'][0]['total_spent'] == -224.89
    assert result['cards'][0]['cashback'] == -2.2489
    assert len(result['top_transactions']) == 2  # Поскольку у нас 2 транзакции

@patch('src.views.load_operations')
@patch('src.views.get_currency_rates')
@patch('src.views.get_stock_prices')
def test_generate_json_response(mock_get_stock_prices, mock_get_currency_rates, mock_load_operations):
    """Тест для функции generate_json_response."""
    # Установим моки
    mock_load_operations.return_value = df.copy()
    mock_get_currency_rates.return_value = {"USD": 75.0, "EUR": 83.0}
    mock_get_stock_prices.return_value = {"AAPL": 150.0, "AMZN": 3000.0}

    # Сгенерируем JSON ответ
    response = generate_json_response("2020-05-05 12:00:00")

    # Проверяем структуру ответа
    assert "greeting" in response
    assert "cards" in response
    assert "top_transactions" in response
    assert "currency_rates" in response
    assert "stock_prices" in response

    # Проверка содержимого
    assert len(response["cards"]) == 1
    assert response["cards"][0]["last_digits"] == "7197"
    assert len(response["top_transactions"]) == 2  # Должно быть 2 транзакции
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