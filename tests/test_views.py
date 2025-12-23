import pytest
import json
from src.views import generate_json_response
import pandas as pd

# Тестовые данные
TEST_DATA = {
    "Дата операции": ["2020-05-01 12:00:00", "2020-05-05 15:00:00"],
    "Номер карты": [7197, 7197],
    "Сумма операции": [-160.89, -64.00],
    "Сумма платежа": [160.89, 64.00],
    "Категория": ["Супермаркеты", "Супермаркеты"],
    "Описание": ["Колхоз", "Лента"]
}


@pytest.fixture
def mock_excel_data(tmp_path):
    """Создает временный Excel файл с тестовыми данными."""
    df = pd.DataFrame(TEST_DATA)
    test_file = tmp_path / "operations.xlsx"
    df.to_excel(test_file, index=False)
    return str(test_file)


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


def test_generate_json_response(mock_excel_data, mock_user_settings, monkeypatch):
    """Тест для функции generate_json_response."""
    # Заменяем путь к Excel файлу
    monkeypatch.setattr("src.views.load_operations", lambda x: pd.read_excel(mock_excel_data))

    # Задаем входные данные
    date_time = "2020-05-05 12:00:00"

    # Получаем JSON-ответ
    json_response = generate_json_response(date_time)

    # Проверяем, что ответ не пустой
    assert json_response is not None

    # Проверяем структуру JSON
    response_data = json.loads(json_response)

    assert "greeting" in response_data
    assert "cards" in response_data
    assert "top_transactions" in response_data
    assert "currency_rates" in response_data
    assert "stock_prices" in response_data

    # Проверка содержимого
    assert response_data["greeting"] in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]
    assert len(response_data["cards"]) == 1
    assert response_data["cards"][0]["last_digits"] == "7197"
    assert response_data["cards"][0]["total_spent"] == -224.89  # Сумма за два события
    assert response_data["cards"][0]["cashback"] == -2.2489  # Кэшбэк для -224.89

    # Проверяем, что возврат транзакций соответствует ожиданиям
    assert len(response_data["top_transactions"]) == 1  # Топ-5 из двух, соответственно 1 в тесте

    # Проверьте, что курсы валют и цены акций недоступны или корректны
    assert isinstance(response_data["currency_rates"], list)
    assert isinstance(response_data["stock_prices"], list)


if __name__ == "__main__":
    pytest.main()